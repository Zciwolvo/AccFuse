import requests
import re
import uuid
import webbrowser

class BankAPI:
    def __init__(self, bank_config):
        """
        Initializes the BankAPI with bank-specific configuration.
        bank_config is a dictionary containing bank-specific URLs, client ID, and other parameters.
        """
        self.bank_config = bank_config
        self.client_id = bank_config["client_id"]
        self.client_secret = bank_config["client_secret"]
        self.user = bank_config["user"]
        self.password = bank_config["password"]
        self.brand = bank_config["brand"]
        self.x_request_id = str(uuid.uuid4())
        self.transaction_data = []
        self.balance_data = []

    def get_access_token(self):
        url = f"{self.bank_config['auth_base_url']}/authenticate?client_id={self.client_id}&brand={self.brand}"
        payload = {
            "username": self.user,
            "password": self.password,
            "next": "",
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            return data["data"]["access_token"]
        else:
            print("Authentication failed:", response.status_code, response.text)
            exit()

    def get_ibans(self, access_token):
        url = f"{self.bank_config['api_base_url']}/accounts?brand={self.brand}"
        headers = {
            "Authorization": f"Bearer {access_token}",
            "X-Request-ID": self.x_request_id,
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
            "X-Request-ID": self.x_request_id,
            "Accept": "*/*",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to retrieve balance:", response.status_code, response.text)
            return None

    def fetch_account_data(self):
        access_token = self.get_access_token()
        ibans = self.get_ibans(access_token)
        authorization_code = self.get_authorization_code(access_token, ibans)
        webbrowser.open(f"{self.bank_config['auth_base_url']}/cardsAuthorizeConfirm?code={authorization_code}")

        input("Press Enter after completing authorization and copying the code: ")
        new_access_token = self.get_new_access_token(authorization_code)

        if new_access_token:
            for iban in ibans:
                transaction = self.get_transaction_data(iban, new_access_token)
                self.transaction_data.append(transaction)
                balance = self.get_balance_data(iban, new_access_token)
                self.balance_data.append(balance)
            return {"transactions": self.transaction_data, "balances": self.balance_data}
        else:
            print("Token exchange failed")
            return None

# Sample bank configuration
fintro_config = {
    "client_id": "faadd989-102d-4ba1-b9fd-c01d45c75849",
    "client_secret": "6270e8b2f3a78b447271e02c67e7a37e7ae52d7a86f137335c6ec825bdba3ecc5c55b33ba132db8e97215aeca0046ee2",
    "user": "3477246131",
    "password": "c2c69166-e803-46e3-905c-c052c829b2e9",
    "brand": "fintro",
    "auth_base_url": "https://sandbox.auth.bnpparibasfortis.com",
    "api_base_url": "https://sandbox.api.bnpparibasfortis.com/psd2/v3",
    "redirect_uri": "https://www.igorgawlowicz.pl/get_data"
}

# Instantiate and use the class for Fintro bank
fintro_api = BankAPI(fintro_config)
account_data = fintro_api.fetch_account_data()

print("==========TRANSACTION DATA=============")
print(account_data["transactions"])
print("==========BALANCE DATA=================")
print(account_data["balances"])
