import requests
import json


app_id = "faadd989-102d-4ba1-b9fd-c01d45c75849"

url = f'https://sandbox.auth.bnpparibasfortis.com/authenticate?client_id={app_id}&brand=bnppf'
payload = {
    "username": "0182676356",
    "password": "a944b95c-868f-49af-b3e5-6689fb353090",
    "next": ""
}

headers = {
    "Content-Type": "application/json"
}

# Make the POST request
response = requests.post(url, json=payload, headers=headers)

# Check the response
access_token = json.loads(response.text)['data']['access_token']


url = f'https://sandbox.auth.bnpparibasfortis.com/authorize?client_id={app_id}&state=api&brand=bnppf'
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}
payload = {
    "redirect_uri": "http://127.0.0.1:5000/get_code",
    "scope": "aisp",
    "response_type": "code",
    "accounts": "BE15054777401700"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)