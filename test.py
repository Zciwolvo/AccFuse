from datetime import datetime
import json
import INGAPI

# Instantiate the INGAPI class
ing_api = INGAPI.INGAPI(host="https://api.sandbox.ing.com", client_id="5ca1ab1e-c0ca-c01a-cafe-154deadbea75", endpoint="/oauth2/tokens")

# Endpoint and method
reqPath = "/oauth2/token"
httpMethod = "post"

# Payload for the request
payload = "grant_type=client_credentials"

# Get the current date in the required format
req_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

# Make the request using the INGAPI class
response = ing_api.query(
    endpoint=reqPath,
    method=httpMethod,
    body=payload
)

# Print the response
response_data = json.loads(response.text)

access_token = response_data['access_token']

gen_url = INGAPI.INGAPI(host="https://api.sandbox.ing.com", client_id="5ca1ab1e-c0ca-c01a-cafe-154deadbea75", endpoint="/oauth2/authorization-server-url?scope=payment-accounts%3Abalances%3Aview%20payment-accounts%3Atransactions%3Aview&redirect_uri=https://www.example.com&country_code=NL")

response_url = gen_url.query(
    method=httpMethod,
    body=payload,
    token=access_token,
    endpoint="/oauth2/authorization-server-url?scope=payment-accounts%3Abalances%3Aview%20payment-accounts%3Atransactions%3Aview&redirect_uri=https://www.example.com&country_code=NL"
)

response_url_data = json.loads(response_url.text)

print(response_url_data)

