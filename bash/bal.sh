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
reqPath="/v3/accounts/720b4484-8d43-47e5-9987-2001c1f19898/balances?currency=EUR"

# Digest value for an empty body
digest="SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="

# Generated value of the customer access token. Please note that the customer access token expires in 15 minutes
caccessToken="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoidHN0LTRjOGI1Mzk3LTFhYjgtNDFhOC1hNTViLWE3MTk5MTJiODNkMiIsImN0eSI6IkpXVCJ9..cDSxEZQx8NO9PDUTfc2MeA.DvjLWpNV9ov2hkAHC5LrBS-jaKVhE4aouipfwkfjA29bBAGPRiTP-5BSocezAt_gQGlG_buDrO5yDaRS0cXb63LelzoWxRyVDrxWeS7-Hfbu8lF92Ok9mkCNrCb3T1XVsCPzYk4lKavXzaycV9fzkl-2Z7xpHsiCPWWWTW8WIRnwCT_TsQNDGW49O9YSMOUdnUHS54Krt9z2KYy6PtBChN9oWl7jgT4NpORq3mtjtxPUQ_ZLuSV8qzULDYBhBsDTFQLCwk0n5jxbuaW5kSwnFh7AzqOhpaaTACg-cpYqdNwBthT3nocKvH57HAKbpIHkHHxji89iI2s5NRYleIGDi4GDYsIQ1D4lFf2Vj3v5Z4nypI_QU4Rc4MSi7vh_NG57QcvT5gpzFQxKla7i_yUI2xV_WmBQ-nv96OI2azWDYER1jGBgnEguhJOakLbarTH3txnAzOsFNHicnJUwbuhTIJRPECe1C1ybk3ottr7LAGlfMroErFEaLv_frHs341IfPZlb0rlOmIUu9qMweg_3BwH2WTap-Fdj9xqSMetWeYmlr6XAg7QXzPhVMEfGPwlSXxQICp4WHy4mXejLIZLBSI5ADxiLB2OqrXtLp70sd6QxCc81vqeF_LuDcbV0qHhTLpUInM8-39t9v5fvyqYR0bPyRH5Xw1fw5O0mFVucTV-LwCD_vqMY39pd4hRLEiIawiBJ2UU2tp8hwZs3UJjWVloalwaY89VcHuJn3xudY66j65K2MqJFkf-sIgHjMNg0YlTERjnUFRQEn4NQTRvkuS0bBfT4zE-8fjtnKmf-R3win6DBIZLEGQBtYrdU6ZMBiBv8ZVkyN9tSE7tczv8PCIN8UgFH7EVDIzAunRPr_Fdq-eW-ILF2WwjGURIqXa9cXfD-hTEKVZP49l-n4xPYY32WH8Cf1fNMmnUY1FG8Iidy-X9x5yKeq82cYyB02Ne0-8HSrZVEssW6LZfoLJvZcb6UJ9ZKGvXI_Ei1MsOdtcFVTM5nl8TwR_BcBk3U2oqNLIyby4MXRxn7DAh2bVKSsmqcS80icdaGdu8rTVSBu81uATQfROZcftZho412VvqOCRxcyHa8FxJXSPmN-Ig5MZYWq8QGSpm9VNMvrShR1uwq0byE2WTv44s29s0Zsur1A7U9cxtpLkxdwlJ0N9nH-FiW0X2PlNHfLrgNy5b4mNehN6PeLi1LfmO3Dc1m_SjAA2BLarBh0hjOYl9O5HRyQdV6vQojl6Hn_feS8dK7WGXMaUGcWzS7EQfRixAFqAB_iul4Oexngh2LCN0LZ2ELmtY9_Y-N8P4Tt2lHtPzgowGdnaBJR-fsPe4aApyy1KTG7Hx2UQTgu569fR_KJVhqK7wEcExIBSimv0pmcOb36a6sUHrYU7IG0KoEG0neaQ6D24xKXj00uRIyuMmLNbPna6CRaMFEF21PQl8Xh_iraEJABItAY7Bwff7UMjhRUhRS2tElxWskIXLnZiJKrQsj2OU_pBS0dzof9ISYSLp0ydnjMYlpVQAqQeba2RydlotL7WmiTyb0u0Y2E3ddgBzIYzUX3J0V9g6BmWLQqVUkE_c1ijacfIYnm3djbHtw2x0MMAqcp7HcXbK5Z90wR7PHbkJxnsR7LUE6nVFpVtJHhGDUo3TE3GlG4LwkmrMi4HYafIHYsIEh071EyO8732mM6O0xETafpYB-Xmb4mUURp-yF71iG5Asip4Y3pGGA8YdZripsWBS_gRmKnFYAWz8rnMzJTGmE7xa9MNHmxIL7h8uGq_lsdH0_3-Fdqu5FSzkPzT9d8JIg2fRQh9apJ-80SVMVY1OTbK5hiYNP1tz-tq40f4r0q-gmB_3fyWo7Xuk5TChTTeXFvKVFYx3t8q68T5GWVTdsAVx4jFc2FysKOlXFFYThQn9-3DkQBE_W3vwh3zbFHWOwUjDCosVChKA7oKhZapsq7KUVW_4G_eroUxXiukQ716MIqh7-B0y1m1P2EI0sx_8KILkCltLmry1UzNCfwAdDnmYW1wCWLiz1hVSk8KOtYx3TYXrOFdAMfTIbUnoz030a4Tdy8yWDonyxEv3gxzkLEhaJUZnpcmzqaQs_RXeYSXReAuTFXawt1YfFRnuudzEvfwNfs_XPyRPNd69riGRf7bkP9OS5pP-3b6AOuoLlCSxfV_K6E12-iIdTFj0w__E20BbwyDpPOeb54ykX5A6HRcuhRsRjg1poPjPReM3nP_QXntrEk22LFryoOjt-fIsrAphJEVU_LLN2o03nd_6NP8f8Dp4hcf617ofMJwapzBRvA0DCzZK6lBVzlh2Y_9Hr7hA5OzDr4SsKOVc269I9XWjEXk1FdPdTD1_DwDLNy2NgAk5VRTLFNuThbjckTaDs44m8Yi88rnWFRrV91g-ydtUzmMdNhN0NdUUmxunmmW9K8HA7FLqNlrtEcbUcQqyQh27HMTrNNruVux8o5X5YKB_nqH0dFb6FThWVKJp5tYiPXga_Y7t_6jasSAolAqGL7teXifZCc7cUU7cFlnk8O5T_cg1fXhmhXhf2V30ZC1ZkmxXIXkKsu5K18zFlt80bkwFpyf-RI-fn4OTCjngIA-GkM-YuLVpqDJ27bowS4fECAxa-Q-kntO0HL6zZwLiv43DZdI4dvx83aBXVfe5K244_6as3JZsPoC3O3cNU1eQ_67mSM2AMGWEFVmd_CoXkEzJVDcZ-nS0OegL1wiDvDQE4IqcsfqazvIwBSzbd-eRdIIdlYmEud_exg-NixDX8LUjUajiwAFw0eZ_kSNjDBJekRnYDw7TEObnGiDPcEm2jniX2bxbds7ToIdoo_Lh5oBmLqPwBQJ5N1JjL4UhhjK99fmgX9N6N3R91ZPbk2o-Z8DPD0FzMACQcDvpJBoSa2QNbQXJXDROHlcBDql65s1BkV87Sw8pikUL8VCVrDrjKCNgW014Nh0agQd9rJpA5uV13lDyxaZnqHAfKeHHhMvIfwUmq8Io89gqaTBMoxU54AuR-oAZ6co-c.V7J10UAn4wm6bW5QgaUPlB__Kdm3pwdhCTLalqUOJls"

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