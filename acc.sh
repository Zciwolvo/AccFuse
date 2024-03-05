#!/bin/bash

###################################################################################
#                             CALL AIS ACCOUNTS 					              #
###################################################################################
# This script calls the AIS API in sandbox and performs a post request to the-    #
# endpoint "v3/accounts" for account details. You must request customer access-   #
# token to call this script.													  #
# Please update the variables "accessToken" and "certPath".   					  #
###################################################################################


keyId="5ca1ab1e-c0ca-c01a-cafe-154deadbea75" # client_id as provided in the documentation
requestId="33a298e6-44c7-481f-94ae-fdc0321fcff3" # Request identifier
certPath="./certs/" # path of the downloaded certificates and keys
httpHost="https://api.sandbox.ing.com"

# httpMethod value must be in lower case
httpMethod="get"
reqPath="/v3/accounts/181fdfd4-5838-4768-b803-91ae2192f906/balances?currency=EUR"

# Digest value for an empty body
digest="SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="

# Generated value of the customer access token. Please note that the customer access token expires in 15 minutes
caccessToken="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoidHN0LTRjOGI1Mzk3LTFhYjgtNDFhOC1hNTViLWE3MTk5MTJiODNkMiIsImN0eSI6IkpXVCJ9..AM-BJx8yVztiKaDmiNeHdQ.8gy-rpAG2buY9YcmoLOssBbDm9N61CxMAnMdFcQgk4ehuN4JynNrCFgBHMsmNZrVWReC5Yxbijg2Ih-_p5Hkc_TdV9dRH5ffmCqo49BPWR4XboV5f06w1dhaV4WU5SHvAyzFMwJ6PsevVih7MEeR_tRkqUHkwvE30SeHimhBp-cIggPM9xtyaHfzMiHQebjvl9FpQ8E1j2-ZFH2cNWEYitMM_2qW0GbWGNYVEQRnSWdvRMNxHU79yz6hzmnJ5zPiEswr4etqFXBo5MEMgb7ZeHVIkoR6nWxLxj9KeAMlIa8m7ZDTcBgg1Xvj3xwS1K7vRarOzN7dJU4MqOIouoSOiSczVf118vT3egcIxY5FfkJOYpmMBjb_zziGEgEBCrei15907KWjIiSqYo067_5sjtOgd5pp4osetYk_Zvo1WbIegOK0QYMnmXMe3C0RLNmeaHvM0FsZa20qpFMHPDtjNT00hrtAH8Eh4CtAcclEwMd9lddMfeKJR16l9pMg50iqgJC2XBC6zIrPj7y528LXYIR6vik8NDjq40crC1cIffA2QX2Sv9dwpV9IcnrEjUK6sna6PNhqAvITZlght0PvfTQpr-lxT8ivrwBsjGoyuL_-yN9aIy1h02pPzJcP6Fn5BmICQ0-9E6H1Ez6iKjWxVdLBqLrB7f53jdR2e9rvVPWojFeroiPEjHWG4s327qrsbO7g4VlCXsMF7mnuopvo9s6JCVIKUl21wZvn0DLA4Nqbpof0qQP8ZcX_oziL8Mwq8IIAsiKdDPXsvmNZJ59D4_a269asv4xLp98aqCV7nIDzCdIRczyal7KmifI61cf-W2kKiPY7PelL5Q9qGC9s5y7phKGIqgolFzX28UpSgn-cCwp9YH4T5S02hUDDCUU-mB-iolBjAaOnC2Tvjw6VSFD7yG4PX5xSlOhwdq47LgCPYUKv243Zr8CYP3g5oiggp0Gjm4Q9WXNK01wOPXL09YOAkMMa6_edJlzhgIgsP8WCZFnVayQXX1Vkd3k1DSZS9pHAj7j-VNz6XvhEXRCI1czlZKN8HjTSmNR8OS-IPfY5IoYi9XO5cV9wQ01fQuK8h7BMRG1s7nKWtskOBH4yCk1BpUL3CKcilTN_Ld38KiP2yeKcux8vVdwR-XPM-C6EVOudMGSiwvVJZNcbUY7J7ydW9YShe2E_vpDdI4rbOjyGOpQCaZxxunpk6feFulwZtJZITgepw0RDP67yykHKd38A0JE0Uuy7_cF9Sbmas_ksC6uWZZIDIVD9nxtq03NthloK4bGZF0_Dw_p-tmQxMlPR5TGm6c4EeAGyclWxzQ-HpsmroaDxOAhB9xg3acLjl1ZlKPYX3NI50PQx2yj1ztfoKUS8bJ0lPtIxZ_MI6EKaM5OkeiImpFVChfAd3NUA4ckcnXLemMu-a6CvYuXzZ1869bxULjJ5jpqoPfsGkFFfrguaVJ7yQTfw5yaGtTOVhh1e8zg3mnecyE1NA7nWtGt8rXcUPAXU_pKekV3waiOyr8pFXbdc6R7VgKHCkisVDEu-hmKqpQ85cniFja4W48xvm5Til9sGkiAXxd_0GKkKwjyz_JMehGh5k91KOBsHa3WyGF-kLp-McDFUspptJS6XSE7VxXNviP80PvN-xJi5odQHJnM8HI5Ene5p2MF25pv6RfsvaioHSwcL3azqZEirh3cLSN5qA1RjkTTEK-NL0wvsue2n51MRiMUQoLphNgPQCKQQmYNjDBEh836u0bftGu5CJpJSrQjhJd0gNVTz64w8jjQIAMZ9sprzNE70oDVbNz7bXeOoqICjlS5gb7v6G7A8pcax7Xx-6FWO7UhWmJEnTbfVXdVkXGiYT6ER9mSPQYvLwGQVKmlxe_ANv7ky7KLVOXMZRFQc79c8YAX6HnhXjX5yvfoaNQFTAiML6TFTNTJ3mqIOMMPrQh0VVviiAZhvJfGNTDBExd1rD8QU3HvUqbPcgd8XGg2m_vnQBGmybeg8Kix7JY6s7Cdqzxg5qAemnKhKHTVY5__YzDFQ3gljEauvK0B1oJ5y-FCp7ubP8a1GT_sOILHCn04tX2oOTCMyDxMUuJFWL_nReC-E4Og_Qx9WrmCNd7_zzdKfCnSr_qC2TzVmaGmkFbJD1y8JPTJdHBNAsnAIJRB-hPVriNhPQhrpd2grlHK3gs9UNIfZ4mlsWWX84-XyJ5L5M98AWpgFmr_ejN_5c-CM25DxKxBU1UMh28Q4XohQvHnzpc846Ctp6D3GpJ_tOCmXdCzYQldc5RcsyNEeCJZtKq8bjiWDOVE_MavnpCYEV6Ed2Q0lKT4G0QTY-f3Q3uCWKMoaK8b5WllH1yF47uOuWeWBwgukQhCNz0ZHb2ypKoWWIHoRMCOGdXhDV222aXudmHcKA6oT8pS-uoofx7Ck0jlujTHM_2trLEI4EkT3C6GshQxCgLmVc3D14jXTUDvkU3BIlT5bGYIDecMRE7H79vsnRksEzr7EXTOhsntanLiYnrpo7-91u2oprvcHjElgKrnMN72NH3MEvlhHyqkOFueTA3anTsCxhuKacJZw6_vwGr0HnEzRhbWAzn8JG8ZTu4y8rFiCnoCkNTa7brNmU6F7CWI9YzzM9xS1bI7QBFHtnLgRFbRFrEl3rJ0Vr0rmWK4gZXFhd82WjVGAoZD590DuqsVNK1vCbhn_-rFu79UAl3yw2Tw-kqJjeyqWwwXriHg-O-FAc6ypdNGJtleH7kokrdW8ebtN8oKn7h1X8X97oemT41a2n2oqSh8soRwtDbIVE99Pnf74wrKESZNKfi2xrVk2iyfons_NmPFXRuU0BvzERIL31yZxzvWRYAyWPXsQXFGqy2jo06msmaUP4VC3wJ0F2ryJ7FWLg5hDR6d3hhpUNiB_zFePBvk7fJfKI6ezb6st0ao6p4kiLgu0ADyHyJGDK_8rY4iG-2Pzh2-v3Y1RHugwSPS2WjO-jO07yFPN87YEnsiStCiOPnIA5gk7F8Ohmvb5ebtX3e4zHd1E.c4n9qRKclO1yYz9xGGZHCzgjPvx8GCCSSlXIPzLMZIU"

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
