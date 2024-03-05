#!/bin/bash

###################################################################################
#                             REQUEST URL TO ING AUTHORIZATION APP                #
###################################################################################
# This script calls the endpoint "oauth2/authorization-server-url" to request     #
# an authorization code for requesting customer access token. In this script      #
# we pass "payment-account:balance:view" and "payment-accounts:transactions:view" #
# scope tokens to consume AIS API. You must request an application access token   #
# to run this script. Please update the variables "accessToken" and "certPath".   #
###################################################################################

    
keyId="5ca1ab1e-c0ca-c01a-cafe-154deadbea75" # client_id as provided in the documentation
certPath="./certs/" # path of the downloaded certificates and keys
httpHost="https://api.sandbox.ing.com"

# httpMethod must be in lower code
httpMethod="get"
reqPath="/oauth2/authorization-server-url?scope=payment-accounts%3Abalances%3Aview%20payment-accounts%3Atransactions%3Aview&redirect_uri=https://www.example.com&country_code=NL"

# Digest value for an empty body
payload="grant_type=client_credentials"
payloadDigest=`echo -n "$payload" | openssl dgst -binary -sha256 | openssl base64`
digest=SHA-256=$payloadDigest


# Generated value of the application access token. Please note that the access token expires in 15 minutes
accessToken="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoidHN0LTRjOGI1Mzk3LTFhYjgtNDFhOC1hNTViLWE3MTk5MTJiODNkMiIsImN0eSI6IkpXVCJ9..wO0MD-F2odjPVjmazH37UA.iaubeb34wOND0NLhqafDoib5ecqt5CrWref44A1IHxTQJO82Q5VaSyvyAgDfc6b-y77sLrEbix31K_ZXJGfiwgmEVaa2rNIphGAHTLqdrM-ynp7nzlB6VQDfW2b4SOnL8sKusOVaAj5Xb1kkfrnrqAA_f_ejy2nTiXS1dfFAI-RF0CUp6D7S4_O1gT1ZX9BojmqVOCLFPGrrav08lHik17umKvazSwnhLhBWI-5_lqmo9oLTaFYzm7nL_jKDPltIjvrHvfTVkVD8YcYAjv2OpfUEBl1XKG8qLL95hYsakVGkKgNVzAudo67SrWXsZJ4Nd_VGUS5Eg-69-7Fv3FcSpcKunLXi42mGr92sysoQJz-ucXu-8Ca4PPWfnDSn72pjgds_9uxBukQVrZgiMZRUoqWwh4U_JCd32KpITD5MIeAo-yQ2DQTlPRVHZFyEZzFltlPVhLwF1OHFT3Gjye8gMx7xJ14tV-EAKJkIw1AWk5CMEBDdlc4ewx2rZZjxCfoD0gy7t6lT2oculfAiOELP88Tle_Ij3pw0mC-IqRHhxX5Bmctaq63JWgdKqoSVJphJZMIeq2jd3_t4Kh3CsdOYTRVsg7XfaNcYS9EQYFKKrtck2ZzWOCF5B_ikkLRnCxneC5iXZ3x6X7nQ-Kq-W7_gP9_di-IPJYWDQwFD3HnS1MhZIajHvY8da7cCSszIz8uP0DSNsvWad95LMUWV9Ng4tttfYQeJJEFhYXfVWNrIeXt3mc427CDPeYrNXlxH7uuZ22oUnswj08qTjG-1hiZkbdUAemIUmIpYY51B8L1hdE-siOOlch4o8rl-VhIqXPP4PJeRvLnNllrfZlG4YSSAlmSRnfFQWE9EAVqzojZ5gr0w4Z7cnlI7PmKwpaWx33TLsoN1Bom8QZqTjPnNmJxFjw6i-TtJ1epXWnv_3kpI-aY_cATWgU5yHzSeJfVulDKuJU1U_hk-FYaDAvMCTl-W07deg0MgcxF6-w5hBcKdvxN2fF-DGdTyPI2kTrmA8yujprEEYKtAzQpo388JWTTyOnZsPJ2GkOBvBFyY2JTBGjKZPum1SJj6wNSQ3VU0t03JMbdzG6-PS5uv4I0es3_WPnaJHZJBh45LJC6cWMzCXZeG3vuDKTRb4IkSsC5LhNDBw4ePmLZ9vvK2Pz_bbsvA-XPNVrYKu8higt3ej0PCSTHmFjt5k6den1FRjFeiSoTTVysGCx5FrACn31htN4mV0H7EhpWC0-_WQoAay2JF83hvYI9MG2_Dh107EKfzPKzYYyV2ubsT2K7Buz2c3H8QW2HJV-W2RC_625VwZRBGH0M_mAT67ObX8HJQR-mAMbofsn-SH5Kqv53F9m3HQHFRZuKCgc92Rwt5_RiEaLQ0m5T-IIkvHcPTfWnITdGt24GPJQwI2y6T0WZ2FBea0zxJX4GtEiHREuYQEiSpLPtthTUrCEsVrNP_8k59KdJPFRqbM2Y4fiLY5cUkhfpy-YNTNO2P0NT8kA9FrMQX8V11LZH19SZrPL8EFWMTxJZEwNSNqP-dJtnIsBcv9iO7XzzcBJ6uoc3skg-uywJ1J7n3Fqy4v2ud0s_Jq1qP4CABXAC9-cceGD4Pcwz1_Wwxhu4Nd3Hj-ZFePONxLG1hekO5M0fsAkVjeBGRKsqx3gErYHgU_8qgBbysCBd9TLfR5qTUVqgKkCrpSxxTy0-j0uuE_2bcMdbtu1KBCPcw26B6_d0m2SZ6870UtmldW-TPRvPJfKeDm7wzmvWnxiMuykPNne4dn0TiFrWnfIYb-rrVHroF3BeeUUfDMwIXV0FHJZbKw1y9ymr6sK-WW0XN5eLwbhH2Swud6Ki2qi1JZy-bNdPyh4TOiQvZpm0ywSJ_XKyPgFkb6YgTRuy3ETlQcUz1FuZU-Sy7H6r7G_Ob7nLFiF8bpi-IESmcCR3VnswRfr9LnkQDMdN9uSa7bidNoDN-ByoyczrOlAQ9GlJXYhP78oMe7U_llciuEV-VjlX1ItBZyi7Vr97-cJncxC8GsxI_RFTGOZRBYq1i9O1rjvF87MMBGi255fVewLqZ_7GPl5czSrsL5Gp-JHwrtx04YbbP-TCiC6kgao_cxpjdpWYxxg1-LuWJ7MXiYG0zoDhdUTKhOBzYjRL5NnA04c6wna6iAIb5rQGVYtYqokUse3OiwTYFR8VZTRg-dYWeyvk5sdxAOy1fnItONcEZ3U0suV7qn1D-ijUJMv30BoRSKQ-JC8dJKvlHh-c3BcNmZSRP7X-zMEqsg0Bq3MjqFyrPnf8XG45IuLh-RtoS4HBw4JmZpNKHWLhG-x6STrpxoWE8iVyKhv4ANT2j78ByrGh8QooOS6L8R920nqtac56bWFAKpd5oc_k315UTIc5e5W2qD5TL1zjoHB68GEimxr2FxY0V0gk4-4M1JGUioTEQwBnkxYgfKV52y2_ZSmYuz4HDU67qo1sxCQsZ95xVXMS1KFsiug_imb1LnmLSqggf3VV7H4ajOnbxwr715ZxT88icR8u1NdsoJQ1-OJCNEn14Vzuhp7axifkcc8XXqFKjob24Jf9TPfuWMRKZ134wFklMeGLJRJaeqlurKUxXyr85clThQ3g.ymdKS9lHIK4Dld0iNFy0Gcafqz_RFQl6hDp_KucuBic"

reqDate=$(LC_TIME=en_US.UTF-8 date -u "+%a, %d %b %Y %H:%M:%S GMT")

# signingString must be declared exactly as shown below in separate lines
signingString="(request-target): $httpMethod $reqPath
date: $reqDate
digest: $digest"

signature=`printf %s "$signingString" | openssl dgst -sha256 -sign "${certPath}example_client_signing.key" | openssl base64 -A`

# Curl request method must be in uppercase e.g "POST", "GET"
curl -i -X GET "${httpHost}${reqPath}" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "Digest: ${digest}" \
-H "Date: ${reqDate}" \
--user-agent "openbanking-get-started/1.0.0 bash" \
-H "Authorization: Bearer ${accessToken}" \
-H "Signature: keyId=\"$keyId\",algorithm=\"rsa-sha256\",headers=\"(request-target) date digest\",signature=\"$signature\"" \
-d "${payload}" \
--cert "${certPath}example_client_tls.cer" \
--key "${certPath}example_client_tls.key"
