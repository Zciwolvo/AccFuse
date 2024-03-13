from datetime import datetime
import json
import INGAPI
import webbrowser

# Instantiate the INGAPI class
ing_api = INGAPI.INGAPI(host="https://api.sandbox.ing.com", client_id="5ca1ab1e-c0ca-c01a-cafe-154deadbea75")

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

gen_url = INGAPI.INGAPI(host="https://api.sandbox.ing.com", client_id="5ca1ab1e-c0ca-c01a-cafe-154deadbea75")

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

ctoken_gen = INGAPI.INGAPI(host="https://api.sandbox.ing.com", client_id="5ca1ab1e-c0ca-c01a-cafe-154deadbea75")

payload = f"grant_type=authorization_code&code={authorization_code}"

ctoken_response = ctoken_gen.query(
    method="post",
    body=payload,
    token=access_token,
    endpoint="/oauth2/token"
)

response_ctoken_data = json.loads(ctoken_response.text)['access_token']


gen_acc = INGAPI.INGAPI(host="https://api.sandbox.ing.com", client_id="5ca1ab1e-c0ca-c01a-cafe-154deadbea75")

payload = "grant_type=client_credentials"

acc_response = ctoken_gen.query(
    method="get",
    body=payload,
    token=response_ctoken_data,
    endpoint="/v3/accounts"
)

acc_data = json.loads(acc_response.text)
acc_id = acc_data['accounts'][0]['resourceId']
balance_url = acc_data['accounts'][0]['_links']['balances']['href']
transactions_url = acc_data['accounts'][0]['_links']['transactions']['href']
print(balance_url)
print(transactions_url)

gen_bal = INGAPI.INGAPI(host="https://api.sandbox.ing.com", client_id="5ca1ab1e-c0ca-c01a-cafe-154deadbea75")

current_accId = open("accId.txt", "w")
#test accId = 450ffbb8-9f11-4ec6-a1e1-df48aefc82ef (Belgium)

try:
    accId = current_accId.read()
    bal_response = ctoken_gen.query(
        method="get",
        body=payload,
        token=response_ctoken_data,
        endpoint=f"/v3/accounts/450ffbb8-9f11-4ec6-a1e1-df48aefc82ef/balances"
    )
except:
    current_accId.write(acc_id)
    bal_response = ctoken_gen.query(
        method="get",
        body=payload,
        token=response_ctoken_data,
        endpoint=f"/v3/accounts/{acc_id}/balances"
    )

bal_data = json.loads(bal_response.text)


gen_trans = INGAPI.INGAPI(host="https://api.sandbox.ing.com", client_id="5ca1ab1e-c0ca-c01a-cafe-154deadbea75")

try:
    accId = current_accId.read()
    trans_response = ctoken_gen.query(
        method="get",
        body=payload,
        token=response_ctoken_data,
        endpoint=f"/v3/accounts/450ffbb8-9f11-4ec6-a1e1-df48aefc82ef/transactions"
    )
except:
    current_accId.write(acc_id)
    trans_response = ctoken_gen.query(
        method="get",
        body=payload,
        token=response_ctoken_data,
        endpoint=f"/v3/accounts/{acc_id}/transactions"
    )

trans_data = json.loads(trans_response.text)
print(trans_data)
