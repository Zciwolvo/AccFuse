from datetime import datetime
import json
import INGAPI
import webbrowser

# Instantiate the INGAPI class
ing_api = INGAPI.INGAPI(host="https://api.sandbox.ing.com", client_id="5ca1ab1e-c0ca-c01a-cafe-154deadbea75", endpoint="/oauth2/tokens")

# Endpoint and method
reqPath = "/oauth2/token"

# Payload for the request
payload = "grant_type=client_credentials"

# Get the current date in the required format
req_date = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

# Make the request using the INGAPI class
response = ing_api.query(
    endpoint=reqPath,
    method="post",
    body=payload
)

# Print the response
response_data = json.loads(response.text)

access_token = response_data['access_token']

gen_url = INGAPI.INGAPI(host="https://api.sandbox.ing.com", client_id="5ca1ab1e-c0ca-c01a-cafe-154deadbea75", endpoint="/oauth2/authorization-server-url?scope=payment-accounts%3Abalances%3Aview%20payment-accounts%3Atransactions%3Aview&redirect_uri=http://127.0.0.1:5000/get_code")

response_url = gen_url.query(
    method="get",
    body=payload,
    token=access_token,
    endpoint="/oauth2/authorization-server-url?scope=payment-accounts%3Abalances%3Aview%20payment-accounts%3Atransactions%3Aview&redirect_uri=http://127.0.0.1:5000/get_code"
)

response_url_data = json.loads(response_url.text)['location']

account_id = response_url_data[43:79]

response_url_data += r"?client_id=5ca1ab1e-c0ca-c01a-cafe-154deadbea75&state=ANY_ARBITRARY_VALUE&scope=payment-accounts%3Abalances%3Aview+payment-accounts%3Atransactions%3Aview&redirect_uri=http://127.0.0.1:5000/get_code&response_type=code"


webbrowser.open_new(response_url_data)

authorization_code = input("provide authorization code: ")

ctoken_gen = INGAPI.INGAPI(host="https://api.sandbox.ing.com", client_id="5ca1ab1e-c0ca-c01a-cafe-154deadbea75", endpoint="/oauth2/token")

payload = f"grant_type=authorization_code&code={authorization_code}"

ctoken_response = ctoken_gen.query(
    method="post",
    body=payload,
    token=access_token,
    endpoint="/oauth2/token"
)

response_ctoken_data = json.loads(ctoken_response.text)['access_token']


gen_acc = INGAPI.INGAPI(host="https://api.sandbox.ing.com", client_id="5ca1ab1e-c0ca-c01a-cafe-154deadbea75", endpoint=f"/v3/accounts/{account_id}/balances?currency=EUR")

payload = "grant_type=client_credentials"

acc_response = ctoken_gen.query(
    method="get",
    body=payload,
    token=response_ctoken_data,
    endpoint="/v3/accounts/181fdfd4-5838-4768-b803-91ae2192f906/balances?currency=EUR"
)

acc_data = json.loads(acc_response.text)
print(acc_data)