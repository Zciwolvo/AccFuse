import requests
import json

# Replace with your actual Client ID and Redirect URI
client_id = "aebe0c6d-5ece-4485-abbd-d87635f8ddf4"
redirect_uri = "http://127.0.0.1:5000/get_code"

# Construct the URL with string formatting
url = f"https://api-sandbox.commerzbank.com/auth/realms/sandbox/protocol/openid-connect/auth?" \
      f"response_type=code&client_id={client_id}&redirect_uri={redirect_uri}"

# Send the GET request
response = requests.get(url)
print(url)

# Check for successful response (200 status code)
if response.status_code == 200:
    print("Request successful!")
else:
    print(f"Request failed: {response.status_code}")
    print(response.text)  # Print the response body for debugging
