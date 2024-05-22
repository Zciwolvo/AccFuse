import requests
import json
import uuid
from datetime import datetime
from jwcrypto import jwk, jws
from jwcrypto.common import json_encode

# Define variables
client = "c2e796fa0e15ac21fb441b1cc833846b"
secret = "e00d0c0a7e7a3925c30bb284e1bd7e92"

# Define the request data
data = {
    "requestHeader": {
        "requestId": str(uuid.uuid1()),
        "userAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0",
        "ipAddress": "000.000.0.0",
        "sendDate": datetime.utcnow().isoformat()[:-3] + 'Z',
        "tppId": "myId",
        "isCompanyContext": False,
        "psuIdentifierType": "string",
        "psuIdentifierValue": "string"
    },
    "response_type": "code",
    "client_id": "1b3456d3-bc33-4190-80c8-623bb9a0b12d",
    "scope": "ais-accounts",
    "scope_details": {
        "privilegeList": [
            {
                "accountNumber": "",
                "ais-accounts:getAccounts": {"scopeUsageLimit": "multiple"}
            }
        ],
        "scopeGroupType": "ais-accounts",
        "consentId": "MYTPP-b3ae3d34",
        "scopeTimeLimit": "2029-09-01T04:45:48",
        "throttlingPolicy": "psd2Regulatory"
    },
    "redirect_uri": "https://www.igorgawlowicz.pl/get_data",
    "state": "code"
}

# Convert data to JSON format
data_json = json.dumps(data)

# Load your private key (replace with your actual private key)
private_key_pem = """-----BEGIN PRIVATE KEY-----
MIIEuwIBADANBgkqhkiG9w0BAQEFAASCBKUwggShAgEAAoIBAQC0rDf5aflHPm1w
EO2zqm7ABzV7geVc79dQcqOHFLURFrw8uNN8Rx6a+Q83V2rNYTp7RbSt/LqH4q1e
S2Qa5vFcV2oTpPIBXATGI1A3t/5eDnhjrvhZ4B+mvsfYMwSRgo7/fVj4KFFUq9AW
bcPe2wEI3KujeSd2uOb8Wenvz9JkAajT8l6fe2exZX6wmqpnk6KqvzBs9ST4Miaw
P+Crtj2MH4NdqxBoLWes9y2CzzgLbifIxKotg7ougIZtXDR1zQW+2szRde+M3sd2
paXWheO2KcH1qHY4VYs1TmRKUkb8FCx3lzGJZa8i4ZflQbuyAPtalO2wHXKUuvre
4jFexawPAgMBAAECgf8OHWZCFgVji30BRFFNuALu/aEwBPXmTNaFcm9UHkoHC7+o
/seG7gd2E/8cU7gEU5Q+DTQQY64u74ab10f60hAJJssivcAqWwYEdL3PnJBCyN6e
6wx7+QaAAGecfF/e/lQtoZ1RxdSUyNd46RpkTrfF+XdvTgfHPqrNDDk6gwHszhKj
wYAfXGdXv9ZV6CnmVqrqw3URBHLK0w1NYBcBCyoFdz9K/k4fzyP+N7T/TgW9Zzw1
Wy/R45liy95WAXld8YNCXNSSZiHPnwfS8+pOS101HaWy6vdZ8A0j/yvHyxI7LSTN
RyGy4CTjsB1YZi5zvvk/dtVmmD1YpqquioMtx6ECgYEAxDfePH1WFi8RKbRcKpQD
ymZnTqVybidGZtmBr+mUZRDGJcXjYVsdgXQxBPrARzkB575VCoVPlgLbCo9ryDc8
N06hi21/dASaGHrACz/cClfXffsaBHsLzmwracQIvI99oVAJ8MXWlcQz/DfimwhJ
cu4hIiwPymXz2OYFGCdyhCMCgYEA67ffI7C4LubFOkxRtYBVYcuf4/Sihg1tvjes
XxoGF6Z8U+GAByUy6MD9MpS1FqaS+DYQ9wDVLXNiOixZQRLSWKUE6KEHEnHTguKC
inphRiT6hlm5IX6ElWIe/WBYPU/RvqIntEN3gsc6W0BlL13Ye7Ol86T4qPAtXbY0
NmbI0SUCgYB6faXufQ/QqXE9Z6phqiTzpRm4ru/QdBQvAHlFJ7vLm70Wt4JKtGam
+bHgOejujVfzI45TEwWrz/yNixrt0g11OVD/iUuXUYgg4AAjBaqHim6r5qVHRskI
A97WF9qcW7dBjIWoGNjshZ8uRHTh8zpm1OE6Q+dXom2naXCks3t5oQKBgQCrfO7i
6UtmG8/7FNERKdd0OY8Oacjfm99uVtSZr7Yk+KNU5yacjCyYdub+KIAChZdA6xy2
hq2QznP0/JTGqenMQenrUFNz0MnfW+k608P3Iyn8GkR8oK3WfDctgS1RFcPzW8dk
9vx4cXb8MkIrDqxTeqROOIQLbAilN8yOk4Kf3QKBgBGc3pv0pQi/TZiSUPb9mjxf
fkJON18lf2lwqdJz7L5kZiYxPGCuYucFNrGwHkSXWi1zqsxN64toBHydtYzfsN3Z
DfOsyO8a146CkWkECItVS3ivZTPeyRja6tgnH+gmu4oNddi/oVCFaeMZw6U+4TXV
DfRetxJdcQguH9T/kH+y
-----END PRIVATE KEY-----
"""

key = jwk.JWK.from_pem(private_key_pem.encode())

# Create JWS token
jws_token = jws.JWS(data_json.encode())
jws_token.add_signature(key, None, json_encode({"alg": "RS256"}))

# Get the JWS signature in detached form
jws_signature = jws_token.serialize(compact=True).split('.')[2]

# Define the request headers
headers = {
    'X-JWS-SIGNATURE': jws_signature,
    'X-REQUEST-ID': data["requestHeader"]["requestId"],
    'X-IBM-Client-Id': client,
    'X-IBM-Client-Secret': secret,
    'Content-Type': 'application/json'
}

# Make the POST request
url = 'https://gateway.developer.aliorbank.pl/openapipl/sb/v3_0.1/auth/v3_0.1/authorize'
response = requests.post(url, headers=headers, data=data_json)

# Print the response status code and content
print("Response Status Code:", response.status_code)
print("Response Content:", response.text)
