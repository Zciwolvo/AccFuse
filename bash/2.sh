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
certPath="../certs/ing/" # path of the downloaded certificates and keys
httpHost="https://api.sandbox.ing.com"

# httpMethod must be in lower code
httpMethod="get"
reqPath="/oauth2/authorization-server-url?scope=payment-accounts%3Abalances%3Aview%20payment-accounts%3Atransactions%3Aview&redirect_uri=https://www.example.com&country_code=NL"

# Digest value for an empty body
payload="grant_type=client_credentials"
payloadDigest=`echo -n "$payload" | openssl dgst -binary -sha256 | openssl base64`
digest=SHA-256=$payloadDigest


# Generated value of the application access token. Please note that the access token expires in 15 minutes
accessToken="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoidHN0LTRjOGI1Mzk3LTFhYjgtNDFhOC1hNTViLWE3MTk5MTJiODNkMiIsImN0eSI6IkpXVCJ9..ryw_JA-leaBthNQk0pYBpA.yrHR9nQisWpT_9SCBniRPP3k9nYk25IVygY2PCVGhUxhwnRKcRJqkpuDY6fgRxQC-OKk4XSJb7CWJ38W2pAdPYESbUJ-vqVC-iiSinLlNoRzrc-CewtXXHXfslOgYA0BzT64PvYlJ43h1Pj5VNOtixfwU4c5610zIagNf1Pl4K8WlXM7dAAXfJkha31MIq_-lPnhisjuOQF2oi1wQGjF3aiT3mnGEelxeSs1g9qG9W75HdB-jHpp44IcW7lkfG6lo0OWy8zSIPVwhHXtNeUw2fR6FGmCEeXmBkGiKKgg1rvgBL0aKl2DDKCo5HUqZBYBDHw1Vf0II9k7HQdJjKMzPr4_Fgn33_U__yrHAFDMIFiJ-4WZ3Ym4FnPi6TprvbpI69hj36f4fW4WXs2eYrfPypn8AYA0gGVOU3XBJwwVl2lk4wkrAR3SzCOuSxr2cmbjYjd4Cxdx_itjI7LSE0IQJH9JOaHDFvUthMF-WuVhQ2icEZ2QYXKI6wNIviAUiagKJiho3362jmF26oImVTbg0owzEGk3XHLQxwXZr2tv8y6KULf79I6PyhVBajWXeuUujcBGrHCdfywmlHtDuKfUEPM1VDeydCTANQF2rSKF81Y-66anHG18VKGs1ofN2pGZAQrQeN_J5QzRzf5sa2sE-r2FQUQKe5SBR510Y0hG9KbvYhulHfkQn73M2dS_3_v1XjSvYMwRjrgSX54l6_WY5Zu1SBp1W85uEwl02dBO0B-weygimEJ23ldn9nmwPAhRcGv1qCrFAfIvBd-YywiWAHb6Dbeeo3vPImLYxVrEdMq6my4h4kVGTy8MehFXoNeClj5Dk6VpEtimoWL_fDNjZOKxEEZL2n-Hp_xF1vO6uJWlvRFMrgeqe1S7jZoIllvQ8MhP4QEtD5Agxzuw8PfssNbHlqyeabOeEtPzRZeqHbG_GoBB7sacJbwkqV0yN-kX4c6jT-_MgSNhAjR9AOjCpNCrUkg0-kzydg8TIBUr0cAMQx-3lJ-PZ4SR77Qr5T0H7WCzNaNAXWIzcMBgIYm857BoRXaOObe1M2kJh8Jx7WHCXUPe3J4UzajSqzas1SFH6JojYFb1XftaeTts1HxiGYw7VTImQaR6SRhrCRpCQvnk1EoTuQffBuVBv7YnYOPNqo8GQipP47WGsYrhVymqZ3iIXIxR0QGHIpgOAZdH7D1EHoMlj6aZV34oEuIYZ-y5-Eyb6Ot1WA2RD0H1Ei6DlCgve7wYJgm5fAx_V3OGbGSLnzkilrIZ_JsKPu-NgkVgaAohjtBDLqsvKl6LUQZNUKhNfTQ62MhS0Q7OjEFlvUbLHAYo5li8RX4jx9tMF5XZz018ANiujQKHCcay_cviqRvg61S-8K3rLyfxtxwFyd37VxZpYaOV6JwazAK8fX2cONXy1yJVc7LEEnwtpqT-554fjnNM6R7A0E42u2XytApO_tPdlg989q-l_ZSg4L5Ee_-2b8JeDfKuqBiM_UgoLjfvSqH-Ms4RjFnqiClAvXrJyXRECS2RGBDrbMeWDQRUVeEc-Gbyj0Nz9jF-6FOgvjJjqRYovUXELt4YDLRtVFWoVOZYZI_wohPEhRwaMed9HZLEGp311k0QyZRy_8AkqPrYnjAGN4gE0Wemz9wY7l-omUgKGf9iKXMQ7gclSFOsecRNIu_ZO3KqWZtTCG5Sk0x2QZuZLTpBazKQCvWRTQRKDviK-Qyb9AeJDR7Vm_ThpkETjtTodr1AUNFTJfqHKn-upRjRLD_TtWNHQoQu0MYzQOEeKec71Vhs9ouMhEepL9N2ffxlaKT1X2g0VpNpqXTxlylN70jNfT54WVp-MKS4nLLx0fN1jAd4aZ7W8Y4Pc_j9MxPr_oahdcSoBSd4vyD8mdEe33JvkDcXlHh9F1n9p8PJLpcixpT8hGanJFxVxFc5QuIS7ZW2RQcMLCXtbnx9Mx1vU-f6M0cLlWQSFjN7Qe7zzgYFlVF-7AmEvInNxUC48K0h_51Lz0NMQywFmE-pxafvTu9SLlTtPHOJB2m7Drxj1w39LiddLkWoXX1zp6FDafMFJq1yHh_gS2VsOm58NtvdG8XLiPxWgtnggsZTl27zG_mb13U0UD55O6Atya9_lwafsy3bjytrNxLoxqZYSfKyC64BMzyuyGaQBRx4VI-UcoWrz4BOfPXwlK1milt6MbQuh-4LcPK2_mOcEzFXPSOkHHEty_SD000noAd9BS6ePrnc0siATaTyJtJP4WQeN6Upami2kNzLpnbq1QO-vNw2nTg24c2zDRoyjw1m_XrRToybP9UrTw-ftEiAN_dUsBsc5Z0sX78ouvtk8PYIugoyAK1dwWKrzO7GwpfeJ7K3zjzkNdabqTfwYiQ1YakBpUqX2fRlyQw8UzxjtvoP8Okxlr59lSNfPWnX-IN7iryALRfoQHtJb79MlmqAJD3tROtr5kIKfZ1QJb5q_bGOjUwfGyI3ZLI6DvihUpCqD0_72yzLuSROI5UiA2qM9i0Wnvv08y9tDEZrk8MO0KvNgiMxi9PN0Kplp2LZK_nKMHXP6CrWw-Gttto0S0ZdFAu2YyF0hFbEGwj1DQprdrykqr9eAtr3u5zfC0LdD7U.r6W7f5LzlF8hr24oQpZE4lNwrgxZZv-ASdK692iyE0A"

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
