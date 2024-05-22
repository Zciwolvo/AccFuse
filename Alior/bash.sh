#!/bin/bash

# Define variables
url="https://gateway.developer.aliorbank.pl/openapipl/sb/v3_0.1/auth/v3_0.1/authorize"
x_jws_signature=""
x_request_id=$(uuidgen)
x_ibm_client_id="c2e796fa0e15ac21fb441b1cc833846b"
x_ibm_client_secret="e00d0c0a7e7a3925c30bb284e1bd7e92"
user_agent="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"
ip_address="000.000.0.0"
send_date=$(date -u +"%Y-%m-%dT%H:%M:%S.%3NZ")
tpp_id="myId"
redirect_uri="https://www.igorgawlowicz.pl/get_data"
state="your state"
consent_id="MYTPP-b3ae3d34"
scope_time_limit="2019-09-01T04:45:48"

# Define JSON data
data=$(cat <<EOF
{
    "requestHeader": {
        "requestId": "$x_request_id",
        "userAgent": "$user_agent",
        "ipAddress": "$ip_address",
        "sendDate": "$send_date",
        "tppId": "$tpp_id",
        "isCompanyContext": false,
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
        "consentId": "$consent_id",
        "scopeTimeLimit": "$scope_time_limit",
        "throttlingPolicy": "psd2Regulatory"
    },
    "redirect_uri": "$redirect_uri",
    "state": "$state"
}
EOF
)

# Print the JSON data for debugging
echo "JSON Data:"
echo "$data"

# Make the POST request using curl
response=$(curl -s -w "\n%{http_code}\n" -X POST "$url" \
    -H "X-JWS-SIGNATURE: $x_jws_signature" \
    -H "X-REQUEST-ID: $x_request_id" \
    -H "X-IBM-Client-Id: $x_ibm_client_id" \
    -H "X-IBM-Client-Secret: $x_ibm_client_secret" \
    -H "Content-Type: application/json" \
    -d "$data")

# Extract response body and status code
response_body=$(echo "$response" | sed '$d')
http_status=$(echo "$response" | tail -n1)

# Print the response status code and content
echo "Response Status Code: $http_status"
echo "Response Content: $response_body"
