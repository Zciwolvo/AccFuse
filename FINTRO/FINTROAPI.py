import requests
import re  # Import regular expressions for parsing HTML
import webbrowser  # Import webbrowser module
import uuid

from FINTRO_requests import get_access_token, get_authorization_code, get_balance_data, get_ibans, get_new_access_token, get_transaction_data, get_account_data

app_id = "faadd989-102d-4ba1-b9fd-c01d45c75849"
client_secret = "6270e8b2f3a78b447271e02c67e7a37e7ae52d7a86f137335c6ec825bdba3ecc5c55b33ba132db8e97215aeca0046ee2"

user = "3477246131"
password = "c2c69166-e803-46e3-905c-c052c829b2e9"
accounts = ""
x_request = str(uuid.uuid4())
transaction_data = []
balance_data = []

# Authentication request
url_auth = f"https://sandbox.auth.bnpparibasfortis.com/authenticate?client_id={app_id}&brand=fintro"
payload_auth = {
    "username": user,
    "password": password,
    "next": "",
}
headers_auth = {"Content-Type": "application/json"}

access_token = get_access_token(url_auth, payload_auth, headers_auth)

url = "https://sandbox.api.bnpparibasfortis.com/psd2/v3/accounts?brand=fintro"
headers = {
    "Authorization": f"Bearer {access_token}",
    "Signature": "Only for PROD",
    "X-Request-ID": str(uuid.uuid4()),
    "Accept": "*/*",
}

account_data = get_account_data(url, headers)
iban_list = get_ibans(url, headers)
accounts = ",".join(iban_list)

# Authorization request
url_authorize = f"https://sandbox.auth.bnpparibasfortis.com/authorize?client_id={app_id}&state=api&brand=fintro"
headers_authorize = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}
payload_authorize = {
    "redirect_uri": "https://www.igorgawlowicz.pl/get_data",
    "scope": "aisp",
    "response_type": "code",
    "accounts": accounts,
}


authorization_code = get_authorization_code(url_authorize, payload_authorize, headers_authorize)

# Open the authorization URL in the user's default browser
NBP_url = f"https://sandbox.auth.bnpparibasfortis.com/cardsAuthorizeConfirm?code={authorization_code}&redirectTo=https://www.igorgawlowicz.pl/get_data&state=api&appName=AccFuse&cards=N"
webbrowser.open(NBP_url)

# Here, your program execution would pause as the user interacts with the browser

# Simulate waiting for user input (replace with actual user interaction)
user_input = input("Press Enter after completing authorization and copying the code: ")

# Third request - Token exchange using extracted authorization code
url_token = "https://sandbox.auth.bnpparibasfortis.com/token"
payload_token = {
    "grant_type": "authorization_code",
    "redirect_uri": "https://www.igorgawlowicz.pl/get_data",
    "client_id": app_id,
    "client_secret": client_secret,
    "scope": "aisp",
    "code": user_input,  # Use the extracted code here
}
headers_token = {"Content-Type": "application/json"}

new_access_token = get_new_access_token(url_token, payload_token, headers_token)

# Check for successful token exchange (200 status code)
if new_access_token:

    for iban in iban_list:
        # Fourth request - Retrieve transactions
        url_transactions = f"https://sandbox.api.bnpparibasfortis.com/psd2/v3/accounts/{iban}EUR/transactions?brand=fintro"

        transaction = get_transaction_data(iban, new_access_token, x_request)
        transaction_data.append(transaction)

    for iban in iban_list:
        url_balances = f"https://sandbox.api.bnpparibasfortis.com/psd2/v3/accounts/{iban}EUR/balances?brand=fintro"

        balance = get_balance_data(iban, new_access_token, x_request)
        balance_data.append(balance)
else:
    print("Token exchange failed")

print("==========ACCOUNT DATA=============")
print(account_data)
print("==========TRANSACTION DATA=============")
print(transaction_data)
print("==========BALANCE DATA=================")
print(balance_data)