import requests
import re
import uuid

class BankAPI:
    def __init__(self, bank_config):
        """
        Initializes the BankAPI with bank-specific configuration.
        bank_config is a dictionary containing bank-specific URLs, client ID, and other parameters.
        """
        self.bank_config = bank_config
        self.client_id = bank_config["client_id"]
        self.client_secret = bank_config["client_secret"]
        self.brand = bank_config["brand"]
        self.x_request_id = str(uuid.uuid4())
        self.transaction_data = []
        self.balance_data = []

    def get_access_token(self, user, password):
        url = f"{self.bank_config['auth_base_url']}/authenticate?client_id={self.client_id}&brand={self.brand}"
        payload = {
            "username": user,
            "password": password,
            "next": "",
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200 and response.headers["content-type"].strip().startswith("application/json"):
            data = response.json()
            return data["data"]["access_token"]
        else:
            return None

    def get_ibans(self, access_token):
        url = f"{self.bank_config['api_base_url']}/accounts?brand={self.brand}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Request-ID": self.x_request_id,
            "Signature": "Only for PROD", 
            "Accept": "*/*",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return [account["accountId"]["iban"] for account in data["accounts"]]
        else:
            print("Failed to retrieve accounts:", response.status_code, response.text)
            return []

    def get_authorization_code(self, access_token, ibans):
        url = f"{self.bank_config['auth_base_url']}/authorize?client_id={self.client_id}&state=api&brand={self.brand}"
        payload = {
            "redirect_uri": self.bank_config["redirect_uri"],
            "scope": "aisp",
            "response_type": "code",
            "accounts": ",".join(ibans),
        }
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            match = re.search(r'code=([^&]+)', response.text)
            return match.group(1) if match else None
        else:
            print("Authorization failed:", response.status_code, response.text)
            return None

    def get_new_access_token(self, authorization_code):
        url = f"{self.bank_config['auth_base_url']}/token"
        payload = {
            "grant_type": "authorization_code",
            "redirect_uri": self.bank_config["redirect_uri"],
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "scope": "aisp",
            "code": authorization_code,
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data["access_token"]
        else:
            print("Token exchange failed:", response.status_code, response.text)
            return None

    def get_transaction_data(self, iban, access_token):
        url = f"{self.bank_config['api_base_url']}/accounts/{iban}EUR/transactions?brand={self.brand}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Signature": "Only for PROD",
            "X-Request-ID": self.x_request_id,
            "Accept": "*/*",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to retrieve transactions:", response.status_code, response.text)
            return None

    def get_balance_data(self, iban, access_token):
        url = f"{self.bank_config['api_base_url']}/accounts/{iban}EUR/balances?brand={self.brand}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Signature": "Only for PROD",
            "X-Request-ID": self.x_request_id,
            "Accept": "*/*",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to retrieve balance:", response.status_code, response.text)
            return None

    def get_account_data(self, access_token):
        url = f"https://sandbox.api.bnpparibasfortis.com/psd2/v3/accounts?brand={self.brand}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Signature": "Only for PROD",
            "X-Request-ID": self.x_request_id,
            "Accept": "*/*",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print("Failed to retrieve accounts:", response.status_code, response.text)
            return ""

    def fetch_account_data(self, access_token):
        """Fetch account, transaction, and balance data."""
        ibans = self.get_ibans(access_token)
        account_data = self.get_account_data(access_token)
        transaction_data = []
        balance_data = []

        for iban in ibans:
            transaction = self.get_transaction_data(iban, access_token)
            balance = self.get_balance_data(iban, access_token)
            if transaction:
                transaction_data.append(transaction)
            if balance:
                balance_data.append(balance)

        return {
            "account": account_data,
            "transactions": transaction_data,
            "balances": balance_data,
        }
