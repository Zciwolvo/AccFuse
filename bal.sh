#!/bin/bash

###################################################################################
#                             CALL AIS BALANCE  					              #
###################################################################################
# This script calls the AIS API in sandbox and performs a get request to the-     #
# endpoint "v3/{account-id}/balances" for account balance. You must request       #
# customer access token to call this script.   									  #
# Please update the variables "accessToken" and "certPath".   					  #
###################################################################################

keyId="5ca1ab1e-c0ca-c01a-cafe-154deadbea75" # client_id as provided in the documentation
requestId="33a298e6-44c7-481f-94ae-fdc0321fcff3" # Request identifier 
certPath="./certs/" # path of the downloaded certificates and keys
httpHost="https://api.sandbox.ing.com"

# httpMethod value must be in lower case
httpMethod="get"
reqPath="/v3/accounts/45f76c68-7489-4f37-9609-23e6600f5de3/balances?currency=EUR"

# Digest value for an empty body
digest="SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="

# Generated value of the customer access token. Please note that the customer access token expires in 15 minutes
caccessToken="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoidHN0LTRjOGI1Mzk3LTFhYjgtNDFhOC1hNTViLWE3MTk5MTJiODNkMiIsImN0eSI6IkpXVCJ9..VzpY_mHkRoi_JHEI1Bm3Mw.XgHLj44a2NfKULtMbjrCGvi0WeGz_NAE8xRah1ewrRd2HyArbYg1O3EE9oundgYglP6OvSefe5spnZDP3Vgj4i-BnPIc2JZyjHdy8qEnLbfXifAwLi_ZVAumStYKXgiWqrqtue20-o9BAuD0r0a3FOMpGErAvGETYj-j9x6Dr8W5feVI3HevnrwYabM99uWuqQxOMBUBQPwglVmMg8mkbGc5vEwQDNNclqO5Ap-Mlm20KNIwcgWgmPBzLSeIhshM6QAYrm8YaVrty8gQc-855NvNQPrpWxB8dZtx0DvkIJqiKY4H3OTaWyAIBxsmO4jSYPO9r63PMtN8Kb1vV0lmabTKTwPB2R1sJevH4Q3QmlkQ6h7ozIRacS2wgTKimWyTfkvqjXHIJ6OYq0KIN4g9nKPfIncNMd8Q6IIEqnv1ZfubHldUdkh_xNeZJxwnpLWX6VHAKUG1YSVWCe-H444CC8e7GFBV3s_CNg07nqfqqqShSI8tj5R6W_4bovAm5MgYdbM9OoKhUM37nGQ4yncXSG5wEhTJBT1Pk5kF_qGC4JlQasKAjaiIdJ7gYb2HoEPOdK4roiFxrjBOKYbIlkPmyzIuz3G0Oz-SAH1WYVKkjyQIeaJd9MxAaKeb49DPt3xfbRiVUvduQvbSlqOVAoK67XIhNpknNtMUWJzESYEj811PtkIYdm4_5HCwu55c11akNsag6hunfqUJfON5O9FAuBdgvZvy23cSbPwv0oWzcF6b2_VYmgCw_oXHhDxX9Y5vhaWyQvGExhkoHhKlXcosxhmYPt5IlwynJ3JzE_k0dUxaY5RiOHrNuRiaRbopFLoA_tcme0JAc1QkuGWlPVuUENARD7DbJ3cXJXOm257AkVeAVejCJiDpVYHvdpV27UXIyyoOZyZ7QF6jvdNJ1PGFgd8zm7ob6-B66qGCPJy3YFyv5cgx3mEYW5emhounAOfAZ9f5pEx8-abAh-Gj8lixoN5KBwxO0go8QMcq58cLFmtzWrsMYRl9YfXQ9ixf7rBd7H5-w4rXf6hdKNdhiOoghR7SdSpBK8a5INsQDm1kQkr6-jxIsD259286NjaoYE19aJ0RkiXVLmDp2r-FZFTNemt81g3YQqIbZiRirArYfRVOuuLpY7wNNPPUBQf4_1Cb8WA49q-6VezzdfI-urxtwGzf1Yy2BdLWWyLoe2Tf12jJHorgX4CVgin7zOuhUECuTxzBbOA9R4WKl-FcXTA-_Mb4ijW2q7rOuKhEajd7TUA0u8ygRXMdCCT7thZwEG5QRCIPPc50jvXZmrtFmP5aGuHnyry2c49zp0kyKMswF2b5Q0Wvw_gGytOp-FdAksCeINObL0L8QoYf_qsucF5hCtm3FzRbmoxB9oyyZZul0vJWxRYcMuk-Tn48tvLvt6gBGEJcGLztbVRZt-NWQifGQYvkggIHCEPLmeTUtAkWr1oA5pfxbvjZjlcrwBXbdiY5rgncbiohxdtkt9GiNdfvRecIwN-EmWzm_ZOjGkmA7h7z9HimveFx6tIIUm3KMidzI6D58Xw4L17ZpMwKln97YbIALexg-cdfe6YuVXBuSiwxIgxmKY6YExnaqSBhBdRrqjPI3isqpdDxLnZoSj6ZFxU4XpuALR18Nx9iOaIvLqMjwvIsmUaLoA9V_LWIoYiXlvqXr3tTKe90fWhq5sf9vnX4I7pTXb0Pq3Z4E4im0ZU3fMEf3uEI8fp1wN-IJzy54tZPvkpH5apX23zccHPde6SR2PUAh3Th5rQJtgubrYVXsmcHBtpe1f9ou9JYyMkcYtGpb3rjbIMHfSg79dto7_T43BjpCl4cyNjPHeQVMI9rXjkyO80ywBGvKnHbPd9-GQd3xYxXhJv-4HTi22xIy6YLEwiXH0AFukwlaInR5TIKR15a-vwy2O_FOWguNfn0NRaCWfG-1ARhO4vREcdrisiYKbRlGOsLemjA6a37EodLGbNIY_A10XTXNZejzoji7Z6zA3vY5E6UDbvJ-Rq8XD5wOiOah7SAUy67FKfRwDCpST5KhuKXsvBAfZYlsbD8catgaz-7bE1FySlY3yrImEc5GPilFYxljzMYGe-XvMBEb5sXfCM9v6j5Dwy36v6jBi8_h5RWsF9T6Lij5EvvlGwTTn-jNT8v93TT4gB4Bs8VxgnsRMeGHtqi01xrjEmt5o0HIsk-Ir2xOGnf61mG3oOPNh-YOWe71GZehShw1PpssBApZsqoGAr09A04Xek3UnXxOd2fc6bPu2ilPCYUvygQLPwEJGo-IuL-sTW4ABwSDYGO9nQEq5aioqY2GQYd6bL4zpfK9HgRE0_1KmHnnFm0b_w4IdiLhpZexBtcKowq9nVISj8NKO2PNbM33EasTYCpYWETDvx-TOLpeGZm09iKu_wpKU1h-0XOAfSKYGkw-1UVxrq-rppOnhok5tCP005H-A2wi-R3AtXs94yOuyb4Mk1SdnsuUkQltQ3mggJqMH8N7q_p4mDReO2Fbwsz8jP_Ton5klfVvUNoL-OqlXCJ7fjROWgv1ERMTR8xYk11KLU-_pOrG9yqblmiqf9L34oPKbk2e-eZMM3QbEfYa8OvXER2lVdHVJCyrUC8ZY39_9ax-Ae3FyFnoJLGCGToUuGvAjXU6AIlEoe358WOZjEkQnPmamxRiBLtglRv-6L4juyXMwWr36RNriS6cVRLkvlaC_7oTEAIiht0Vj5kWKlbdtmT0AcMMeMTustewFJXAQ56d4I7_S2T25VvFZl4eHBWZ-gAtUBWTWHXj5heHr68zKI7HgcZGzXQbdpwdsZ1daHYUjcOUjegKWRDsKdGEI_NtESLUKwbmLkqzPXywNDkPZ_RhpcuHHTENWm1f9pvy1ZbTULCfzdnuoYprOc7nr20k9aVgn4osq_PQcyNz6pHwv23ET8Q6B-WNBlq3BrRBSwyDd1bITHRKStKK7Ldo1kiFU-c_wvln-YflZOp8bZoRg_Kwbajete0HegWqX2lDWOEdkSBRCwY3Lr5vWIw.dt_APmQsdhv7y7Psy45npKNKA8zM6hqTer9bD6IzJEQ"

reqDate=$(LC_TIME=en_US.UTF-8 date -u "+%a, %d %b %Y %H:%M:%S GMT")

# signingString must be declared exactly as shown below in separate lines
signingString="(request-target): $httpMethod $reqPath
date: $reqDate
digest: $digest"

# signingString must be declared exactly as shown below in separate lines
signature=`printf %s "$signingString" | openssl dgst -sha256 -sign "${certPath}example_client_signing.key" | openssl base64 -A`

# Curl request method must be in uppercase e.g "POST", "GET"
curl -i -X GET "${httpHost}$reqPath" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "Digest: ${digest}" \
-H "Date: ${reqDate}" \
--user-agent "openbanking-get-started/1.0.0 bash" \
-H "Authorization: Bearer ${caccessToken}" \
-H "X-Request-ID:${requestId}" \
-H "Signature: keyId=\"$keyId\",algorithm=\"rsa-sha256\",headers=\"(request-target) date digest\",signature=\"$signature\"" \
--cert "${certPath}example_client_tls.cer" \
--key "${certPath}example_client_tls.key"