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
reqPath="/v3/accounts/bf28fe0b-e5c0-433d-ba8a-5121d50a0820/balances?currency=EUR"

# Digest value for an empty body
digest="SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="

# Generated value of the customer access token. Please note that the customer access token expires in 15 minutes
caccessToken="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoidHN0LTRjOGI1Mzk3LTFhYjgtNDFhOC1hNTViLWE3MTk5MTJiODNkMiIsImN0eSI6IkpXVCJ9..eVZPqNtNRvRxIbrUm3nvMQ.qVc3lgb0888CNNdft96YTaW_bSSWGdsBfcgujRWgxt45GisdIpmP3oYXIT_b8qQNmI5jN21h0qIIBa8VwEe231i7wZdIuICJ7DcifNOPFNtvc1lGErDpqq30mkEfYjp4PAfVmPJmyXa5Rn9y20N-9hLRPazf6HmwDnJWI8euzpY-V-Fwl8cSKBmUymJydpAExYnwKCb7Ew9QbCxdhAsT6gj2orbe5jrUWTqA9F7mw71Rmw-mlVn8v-BP9C8KguGHao7c-KJ_zvC2JJ8hr80IQcb4VeQYOfBnDsHZIxAPwMKhFKNCPnmq9IcV2S9LvR2LMQ8dqwdg5-5wrz_3nZhcJx3dI7D8B-QbOqUcfhcuxEFmdlqJxRtsPgZByO22muAcoFSJPYwXoOCPlusgRSMrK0sSj9IcyFSxWHrBWLaQ61gv7-Gvs3rov6dsdQO1nk3BvtL2uAbp_21iy-n90tIqjk9vwqAeFiS_8bDF4JMokPxxtKtw0Aaeo0uK4PFWo3ZrHp-T9Uf2m2FQpl38wKyN2u88jcLk2jg62UxPIO9dtFWNH0nrn9IeGY5COWFKIbBEBg2JECkXwlO5bFySSEBBBrfnnW_ACHC2Ft1B7A1TODX2CWXB-lBz_yYtwnJIKN9uXfeEspA19FmWyrnl1huaoqfOauK_JZqY6T0xE_XTl49t1_QsOC3cv1FSAJ-QaLqQqZQMmftVput0zgO0KwXi9JnwwyUfTHGXa7P49whQt6hUzg-V6ekd2shQFuBOySgGgkmr-63yZ86My31HrfZi4P8PO-eSleYjYS3Wr84IfCYWQ_lC-ea_5NWyoAWLsILFLCY6PzQ93U-Yiy6QryJXgySkmgBNc7bcrWS6PTahloUgqF-m3Vnsq7fOhcWGiuLNKq0aVjAajjOq-37S_Atq_t_MnQNJ_71-96AlK_7hmCstDAtNzn3LIHb_9d2XQ2scVbzpzcOhBMmjNwXmUAX7b1ODUxPlbF-di41M8C0I2yuxPvHJT5i9u3sgW-Qyy53QgGFMK-z7gla7EUZoVhTb6T1p6sbtLJTq5m7ne7ZDipOa1RztvTobn28CDmpy4PAeqQyOJaCoLTij69vWPsiOxJ2LqFAxbvEMMnjYyyXFa0BaRmkMwMXDjFsi1hgf60X4tLOgB5ta-J2XLrDIEngPebEDwTosvgqPYv3avk-_JsZDpWw1mxxtSxKIeakOMDvfE2aPwv59sh2EtpZD4ih62QlDRzczW7KwrdffGWsmDYtO1o67Km6rxX1zzahFB1WeUmKN83hsEOxA4GRXZCHzAGm493SUsFDjSVamam1SktvsneZILupUTkF8ZC9YNUVgdPzGiwsQbVGs3pK9ehb6mSwbtyMXPL7Bsnph8JBF48bPD1EmHmNg6X63toNmAIINtxLgils4JYXXqKswleYxXfXjO90J_P2JBPlVVezTkmGWjY1xTQCrsdiQpa7U4Vz9XA5uV51gogKt-YcjdJomyYEvhVmBNB9reicZizgIMInb0AlNJ3Z6pL6jQWVyniy4DF0L_mAemKtIqxWGvG4WuKm0VZv0Z2WmnrbZiYAtPGjbfJmx17OjK19gdTX9vDl0DwJMb3vtUGI-aLJBwgfuRCCfAJP7i_UVDHSwgS6_me9v8TaMs8uIugg4hutXcCeuD2zxn2wxBp6nfuO-7t1Asv8IiBg4_mHEh9EzFWTgQFlUCU3O7pPAQw7xRAA2aABN1DNx-kGVvLs9EkPH8WT1t5_W7rmSx4kjHLN2JCe0x7Rj1KOBxSmKnXoPbfbM2YNxb7S7Q1nlBIKc0ypHjQyN_OwNC4IXNrEktocMgkeSwpwmAnbcN4UuZUkyykICNgsBL9JdSmMF8fO93I-3qQNVKi4TNl7heMchTTXkljpHxwGem7EUNthdLC8G5-yRYNmdpL58DM__lcfQ0Whdz0QWLSOcVhwUF5eQMjSaDTG6u_2yKzTtiM6vkK2vEHJy9Hbfq08glmHtopCxzuIrTEk1NpFfkg2A7dG2ycgSiNMUKTaBsCIBohcLI1PIbcFCNFbOu0Le52OW8ew1qXOSD636GlFV8a_yen0MXRoakalLHPQvtp2zynlq_eq-LyuhGjEW6u6Dn574S8cef-95lVu5CEom1mKetNyn062LnUvEkZ-sFF_hh5xuT-AcdbE-ZzPpsS7f-q0JaxQ64-pTqIqxK5a_Nn0dTXq-ggt_xxelVyY0e6F7L5YGAhrx9CKtseY0LFHN7hepeG3Yigv0srayc57xKz1sy_a3ua4w6-GDUFbgvsqR025CKVkGBMKLBUuxRrRmgUGD0FAZWV4dMHV-NBhmmXAyJu_mWY4vBinl0GO63mEzMCIqq6ud86KCM5eqPXRwLsicMo7BsRc004YnsZtBKRtCSm5LFkjUhc_tMBvqu7u4yVCM1MwrTS6H_UM7yE-Mdb_cQw2hEgBY59DmTr8sSxvK4UEp1LToWZlDUWYNYxYkhTxTrIEp9SPNTg3P6L8H2LQI8LbqwF42sb2DHEbf0wH7aQjGb5K36uZhav6IhHm0hat5ztiXBO8Wi13tMVAMfeMZ6o-8Cqta9-HpNQJAnTLRYHxG5maNuTeMCqW-ZuJf9aP6wo9uHE25t77vVxBPRqZCgCNSAT63iHo5UULlathaMK4k4N5Eg7p1k1AdLVEpsMfB1n97RqSFTL4rmBPTshfD0P3uZad0g5mFBn6xCrsUYZWSP_FwPetRZnB0a3cjJFS72q5ypqawcjXzifisJspuah62HT8DrOJWRXpvUPrtYfKMDleRLa2jaLMF_kxjiexLleXfw5InqlCC7MlXHUoucDAMzRctpi6nclDvp-zBqs0viv5S6JvICF4ciiGYTiamy99ASzX1oWPFMyDNtsFXHVf5QBi40dRW6NZOlaphTPtsPTLdZcR-s0KPSfccBeTNhkQwXIJDdDi2i915B5JLoOWTjH7msKsJ3_KWmAHbpzmvq7G5uy67gBv7uj2Jemc6L_6ETtQNYTYb.aj2DqjU8Kb4FJk3ux97ox-aeBuSm8IU9uxQjMc8sQ1Y"

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
