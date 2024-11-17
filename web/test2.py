import requests
import re
import uuid
import webbrowser


class BankAPI:
    def __init__(self, config):
        self.config = config
        self.access_token = None
        self.x_request_id = str(uuid.uuid4())
        self.transaction_data = []
        self.balance_data = []

    def get_access_token(self):
        url = f"{self.config['auth_base_url']}/authenticate?client_id={self.config['client_id']}&brand={self.config['brand']}"
        payload = {
            "username": self.config['user'],
            "password": self.config['password'],
            "next": "",
        }
        headers = {"Content-Type": "application/json"}
        response = requests.post(url, json=payload, headers=headers)
        if response.status_code == 200:
            data = response.json()
            self.access_token = data["data"]["access_token"]
            return self.access_token
        else:
            print("Authentication failed:", response.status_code, response.text)
            exit()

    def get_ibans(self):
        url = f"{self.config['api_base_url']}/accounts?brand={self.config['brand']}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
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

    def authorize_user(self, ibans):
        url = f"{self.config['auth_base_url']}/authorize?client_id={self.config['client_id']}&state=api&brand={self.config['brand']}"
        payload = {
            "redirect_uri": self.config["redirect_uri"],
            "scope": "aisp",
            "response_type": "code",
            "accounts": ",".join(ibans),
        }
        headers = {
            "Authorization": f"Bearer {self.access_token}",
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

    def exchange_token(self, authorization_code):
        url = f"{self.config['auth_base_url']}/token"
        payload = {
            "grant_type": "authorization_code",
            "redirect_uri": self.config["redirect_uri"],
            "client_id": self.config["client_id"],
            "client_secret": self.config["client_secret"],
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

    def fetch_data(self, iban, data_type):
        url = f"{self.config['api_base_url']}/accounts/{iban}EUR/{data_type}?brand={self.config['brand']}"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "X-Request-ID": self.x_request_id,
            "Accept": "*/*",
        }
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to retrieve {data_type}:", response.status_code, response.text)
            return None

    def process(self):
        self.get_access_token()
        ibans = self.get_ibans()

        auth_code = self.authorize_user(ibans)
        webbrowser.open(f"{self.config['auth_base_url']}/cardsAuthorizeConfirm?code={auth_code}&redirectTo={self.config['redirect_uri']}&state=api&appName=BankApp&cards=N")
        input("Press Enter after completing authorization and copying the code: ")

        self.access_token = self.exchange_token(auth_code)

        if self.access_token:
            for iban in ibans:
                transaction = self.fetch_data(iban, "transactions")
                self.transaction_data.append(transaction)
                balance = self.fetch_data(iban, "balances")
                self.balance_data.append(balance)

            return {
                "transactions": self.transaction_data,
                "balances": self.balance_data,
            }
        else:
            print("Failed to fetch data")
            return None


# Configuration for a specific bank
bank_config = {
    "client_id": "faadd989-102d-4ba1-b9fd-c01d45c75849",
    "client_secret": "6270e8b2f3a78b447271e02c67e7a37e7ae52d7a86f137335c6ec825bdba3ecc5c55b33ba132db8e97215aeca0046ee2",
    "user": "3477246131",
    "password": "c2c69166-e803-46e3-905c-c052c829b2e9",
    "brand": "fintro",
    "auth_base_url": "https://sandbox.auth.bnpparibasfortis.com",
    "api_base_url": "https://sandbox.api.bnpparibasfortis.com/psd2/v3",
    "redirect_uri": "https://www.igorgawlowicz.pl/get_data"
}


# Run the program
bank_api = BankAPI(bank_config)
account_data = bank_api.process()

print(account_data)
print("==========TRANSACTIONS==========")
print(account_data["transactions"])
print("==========BALANCES==============")
print(account_data["balances"])
