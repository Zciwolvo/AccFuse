import requests
import json


app_id = "faadd989-102d-4ba1-b9fd-c01d45c75849&brand=bnppf"
# Define the URL and payload data
url = f'https://sandbox.auth.bnpparibasfortis.com/authenticate?client_id={app_id}&brand=bnppf'
payload = {
    "username": "0182676356",
    "password": "a944b95c-868f-49af-b3e5-6689fb353090",
    "next": ""
}

# Define additional headers if needed
headers = {
    "Content-Type": "application/json"
}

# Make the POST request
response = requests.post(url, json=payload, headers=headers)

# Check the response
access_token = json.loads(response.text)['data']['access_token']


url = f'https://sandbox.auth.bnpparibasfortis.com/authorize?client_id={app_id}&state=api&brand=bnppf'
payload = {
    "redirect_uri": "http://127.0.0.1:5000/get_code",
    "scope": "aisp",
    "response_type": "code",
    "accounts": "BE15054777401700"
}

# Define additional headers if needed
headers = {
    "Authorization": f"Bearer {access_token}",
    "client_id": app_id,
    "state": "api",
    "brand": "bnppf"
}

# Make the POST request
response = requests.post(url, json=payload, headers=headers)

# Check the response
print(response.text)