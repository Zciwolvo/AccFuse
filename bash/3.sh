#!/bin/bash

###################################################################################
#                             REQUEST CUSTOMER ACCESS TOKEN                       #
###################################################################################
# This script requests customer access token based on authorization code using-   #
# the endpoint "oauth2/token". You must request an application access token to 	  #
# run this script. Please update the variables "accessToken", "certPath" and      #
# "authorization_code"      													  #
###################################################################################

keyId="5ca1ab1e-c0ca-c01a-cafe-154deadbea75" # client_id as provided in the documentation
certPath="./certs/"  # path of the downloaded certificates and keys
authorization_code="91b2fe900259ddbde8e3f68ff0b4017f8cf0bf98e6acddfe9ef9f732e7e8253af8f519f7c2bb4660abc67c25ac7ac7ad" # generated value of authorization code from the previous step.

# URL encoded value of http://api.example.com
redirect="http%3A%2f%2fapi.example.com%2f"

# Generated value of application access token. Please note that the access token expires in 15 minutes
accessToken="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoidHN0LTRjOGI1Mzk3LTFhYjgtNDFhOC1hNTViLWE3MTk5MTJiODNkMiIsImN0eSI6IkpXVCJ9..xht-VU19VhQoyZtd_TpFmA.Ku-UHMR00tbpPrS2vAtqeWr5TpMUB4E_0dXRSjx4qqjtiGyQtpaJ0PF1rvO80qUdWz3nnFnnkERvMP7VYYamolFwENQKPsGskeEZEqRYT4fSw6IP6xvOigIaOlX_nySr-ce1K_OrrVjWx-8hpuPY5T8Km7JiIYtZaYuPInlJCoZXZbPqrI5JkNqzpzkPL7JwB8LpssbYYZ3Xu2YAw285M7GVszXotUf7f6UAKwFIPw0uveRI8gUcMGhTaGn3P0_vcZhXXI4KkZEfH3waI6tSjT84hZt_VmwDQxdGRbmMZt65stTjxciU8kNsJYPBf_LShJOG8DihzuWOy5GEY_gpsNdX2EttxWm4s8MlfJquNwPlnOQV-B3BLZ4rESmkT7t986_tnAmio9vNaU2lYbRopyHRQm1P2unjx8BrhdGRLgDZkZUMOCoB0ZMz9rWzBgcBJxaSvuy1B9IDEri0w1i7CtSoSVOLM9WmEU9tC4L2eDdOxVxcamEvXzbJ80gWtwLG1ZEPknAtUvZ4rNdk3dTMv-2kdvQ2gTkXDrLuWmiIX1zGOs_liKOiqK8Zlt_UOOx65lATTb__TS1dP8v1Qi02GxC-2hDCpzOAFzkKpC8fDr8I6_JFnqZGlQYhdh4PC8vBIqyX4ZmYXFrojlLtlBbeCFLwRkbYOJvjX41a3jqpq14eWq3a7d8YABFwmVmV5oCwuoJE6zkN5NHnucS_QRAJZSQodKLdUGXGxkoTUahV3WHGsyHvJGX7djkoaR-fW738n19AKoUZHyvZBO1N78lCLlBzjte_zTANmAIQEReCTWfWvPBlsTd-U6leuNFxUfHTmZfAPCecNM0gAlQ_aYkS6xxAsdQjuL8Wjytfo48fkTaR2-rJ_gYujYW-gkywXCleDvMTGZJDa9DyZQiFZS71MHa43oQ_EAIkTvhkq_aqKeVIQjy5WukqtBiUsP8DmlqMuB3Z7SWUpJPNOfgVpbP3sq7-gCHX3EUZsPXMvVearcw62cF5ZqKM2uBW8wgNMvfxXBKZ9rVyILxA55opZhywhTvNg5Srzweb9SxwljjAe8XFiJV3r3yzexyX7gkaikcByEX_EAVCVrMa6Rvm9Dps4AB06HXYZ8EYKz0dQTBAIbnGeMsFuVC0Ryeo_vhWolGyIhOc7qAar2JrY5KG5_znj2qIQOVQp3nvlacy5w9Z4j8612oZNnQUHnpOih4Z0XwOUwapTh00eACLntvWy2SKLRHre_8BqLz06_wt9AyxkR9RwHvnRW9Do6pjFTlPEWN0OgGNdJ6cqfEZZjXKSv6fIDu7wxrohbzTdGE6XntZ4FoKL1EX9EUx_xI0H3LupoxWm0rdhJ0UJvfyfJ6WnfDahmotPe-jgEGCeduJgKP0YFzNFd6vwnlvgEe0dpc8GeGLnyoSj97_adQPMmOcMu0cDRrTSuOpemUQ9ggYGJNKX_CWsJk-64gZigmJb4DE4cJIqd0j0CVxqPWoaUDzrsKRTaY-J0yaUtrwGPAGfB0pe4tiRU_lXuB9dyaNr8HQheyiuHF78uXg-dadRdQms7Kn7_g87P1CLgvXTXcrVzxR_rBb_OvNgwUb_TgnU_V_NrjvAGWhBNbqntQIykzt4qqYt7acrDVhzSr7HNCe4pWlFCdW11JBTUNTCFvnGtNVCie8t2G2QCkVZtw-ghfu05L3Z1mXAE3IZnhqk0n8YGBRYHfwylt6zvkLz133AT6aANBibe-9VOQkIjrHBHgqXMpB7JGcNW39v3jik1ZU-Bn3h7G7g_Af52TzixixkBVzYhssz-uXyYuxImSzF9O54UHDbBieJgSDOqu31in6mJ5Zh5ph8ubKKifcXpukIp2Zj6PLaH6rrsaEEUl6IAgOnYnpJXCFCuVLlI0IVff57DMforHdnQSZP4fKslowCVVelaHZCBScpc_SsxJ1uzbB23xD6pfYrlkFZ02W0u7BXpGQYcQtVdxaz6rmpUUxt2apfCnODVtTgl-PjnNp-Oy9KS5ZFQOYcVifH1Y_rcPnrgLjPo2u8_nru2bsjueyJSMD7N0hQu1x4P7GVsd-u4osniocOJv4T9ECTO_Ivk3JRiysbEHrJRYLifQuI02-BBJMsnVCFyZ3IrbwdLcm2irRR93lKb4R3FLqZoT14eR2Bjp1DE8y_u3fb50phgoS0Hi1WnQxI2qIbuAHUNrbd9u_CObp-iaYaL9lTvG234F9uBzdMfY9naoO5n9xBUXZTmNGB_Nbsaf-nciEawiILlseX-bF0blWciSie2tN8EIzkQJ1j3TgWkn24VlWZ84VfT5F0iceWuU7F4WoiWE0FYHBbfbZYGdKqHCq1D5SiNcuytI9qXoneXg-1-UIRgWpDEsccfX_55KKCwYPnFwa5i17UKG4_ucEehqocwPV-ElyfBw6PTPKfyELHgW-gEB87TXuf2AE0ponGsjmG1n1BRrHNg2gWezKHA-fWR35Dp3y1Gay69DZKhCrSUfjTJUNTRxe1eL6EOuDXX-4B2dTyZBejYUWzXRZrJocsCA064uMslXsVGISate8EL-8gbPYhbAZ8OaHZu5vALkhCv740D11Lu7A5tgRapkYF-hNEj46sotBMR8.yYyOw10uyUOFqjrVXsBNu5d36ZdpLXWoc4leCcCOjts"

# AUTHORIZATION CODE MUST BE PROVIDED AS A VALUE TO THE "code" PARAMETER IN THE PAYLOAD.
payload="grant_type=authorization_code&code=$authorization_code"
payloadDigest=`echo -n "$payload" | openssl dgst -binary -sha256 | openssl base64`
digest=SHA-256=$payloadDigest

reqDate=$(LC_TIME=en_US.UTF-8 date -u "+%a, %d %b %Y %H:%M:%S GMT")

httpHost="https://api.sandbox.ing.com"

# httpMethod value must be in lower case
httpMethod="post"
reqPath="/oauth2/token"

# signingString must be declared exactly as shown below in separate lines
signingString="(request-target): $httpMethod $reqPath
date: $reqDate
digest: $digest"

signature=`printf %s "$signingString" | openssl dgst -sha256 -sign "${certPath}example_client_signing.key" | openssl base64 -A`

# Curl request method must be in uppercase e.g "POST", "GET"
curl -i -X POST "${httpHost}${reqPath}" \
-H "Accept: application/json" \
-H "Content-Type: application/x-www-form-urlencoded" \
-H "Digest: ${digest}" \
-H "Date: ${reqDate}" \
--user-agent "openbanking-get-started/1.0.0 bash" \
-H "Authorization: Bearer ${accessToken}" \
-H "Signature: keyId=\"$keyId\",algorithm=\"rsa-sha256\",headers=\"(request-target) date digest\",signature=\"$signature\"" \
-d "${payload}" \
--cert "${certPath}example_client_tls.cer" \
--key "${certPath}example_client_tls.key"
