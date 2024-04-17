import requests
import re
import uuid


def get_access_token(url, payload, headers):
    """
    Sends a POST request to the specified URL with the provided payload and headers.
    Returns the access token from the JSON response if successful, otherwise exits the program.
    """
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["data"]["access_token"]
    else:
        print("Authentication failed:", response.status_code, response.text)
        exit()


def get_ibans(url, headers):
    """
    Sends a GET request to the specified URL with the provided headers.
    Extracts all IBANs from the accounts list in the JSON response and returns them as a comma-separated string.
    """
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        iban_list = [account["accountId"]["iban"] for account in data["accounts"]]
        return iban_list
    else:
        print("Failed to retrieve accounts:", response.status_code, response.text)
        return ""


def get_authorization_code(url, payload, headers):
    """
    Sends a POST request to the authorization URL with the provided payload and headers.
    Extracts the authorization code from the HTML response (assuming it's in HTML) and returns it.
    """
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        match = re.search(r'code=([^&]+)', response.text)
        if match:
            return match.group(1)
        else:
            print("Failed to extract authorization code from HTML")
            return None
    else:
        print("Authorization failed:", response.status_code, response.text)
        return None


def get_new_access_token(url, payload, headers):
    """
    Sends a POST request to the token URL with the provided payload and headers.
    Returns the new access token and refresh token from the JSON response if successful.
    """
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["access_token"]
    else:
        print("Token exchange failed:", response.status_code, response.text)
        return None


def get_transaction_data(iban, access_token, x_request):
    """
    Sends a GET request to retrieve transaction data for the specified IBAN using the access token.
    Appends the response data to the transaction_data list.
    """
    url = f"https://sandbox.api.bnpparibasfortis.com/psd2/v3/accounts/{iban}EUR/transactions?brand=bnppf"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Signature": "Only for PROD",
        "X-Request-ID": x_request,
        "Accept": "*/*",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve transactions:", response.status_code, response.text)


def get_balance_data(iban, access_token, x_request):
    """
    Sends a GET request to retrieve balance data for the specified IBAN using the access token.
    Appends the response data to the balance_data list.
    """
    url = f"https://sandbox.api.bnpparibasfortis.com/psd2/v3/accounts/{iban}EUR/balances?brand=bnppf"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Signature": "Only for PROD",
        "X-Request-ID": x_request,
        "Accept": "*/*",
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print("Failed to retrieve balance:", response.status_code, response.text)