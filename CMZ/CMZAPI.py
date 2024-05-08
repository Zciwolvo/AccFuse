import requests
import json

# Replace with your actual Client ID and Redirect URI
client_id = "aebe0c6d-5ece-4485-abbd-d87635f8ddf4"
client_secret = "6f59d588-bbd4-4174-a3e3-a274035ace86"
api_host = "api-sandbox.commerzbank.com"

# Step 1: Request an access token
token_url = f"https://{api_host}/auth/realms/sandbox/protocol/openid-connect/token"
payload = {
    "grant_type": "client_credentials",
    "client_id": client_id,
    "client_secret": client_secret
}

response = requests.post(token_url, data=payload)
token_data = response.json()

if "access_token" in token_data:
    access_token = token_data["access_token"]
    print("Access token obtained successfully!")
else:
    print("Error obtaining access token:", token_data.get("error_description", "Unknown error"))


api_host = "api-sandbox.commerzbank.com"
url = f"https://{api_host}/accounts-api/v3/accounts/{client_id}"

# Set the headers
headers = {
    "Accept": "application/json",
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json; charset=UTF-8"
}

# Make the GET request
response = requests.get(url, headers=headers)

# Check the response
if response.status_code == 200:
    print("GET request successful!")
    print("Response:", response.json())
else:
    print("Error making GET request:", response.text)