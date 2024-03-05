#!/bin/bash

###################################################################################
#                             CALL PIS API  					                  #
###################################################################################
# This script calls the PIS API in sandbox and performs a post request to the-    #
# endpoint "v1/payments/sepa-credit-transfers You must request and application	  #
# access token to call this script.   									          #
# Please update the variables "accessToken" and "certPath".   					  #
###################################################################################


keyId="5ca1ab1e-c0ca-c01a-cafe-154deadbea75"
certPath="./certs/"
httpHost="https://api.sandbox.ing.com"

# httpMethod value must be in lower case
httpMethod="post"
reqPath="/v1/payments/sepa-credit-transfers"

# Generated value of application access token. Please note that the access token expires in 15 minutes

accessToken="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoidHN0LTRjOGI1Mzk3LTFhYjgtNDFhOC1hNTViLWE3MTk5MTJiODNkMiIsImN0eSI6IkpXVCJ9..18yyBeU7FzZwNalt3pmLcA.Qe_NrKO5n2YciQbxg0NWbehM8oIuiAuW8eCMXFa2BUe4UF1vlb6ToCWjkZQnwasJqgFBsq_FuXzkjhNh9u7z2jdXXUZunSPoH6Ff40L0Yb9f9IDMKTxFIF-MUjh_kno3ZK_RmgJG3cBrQC1sqeemnmXwroONqc34-Bo3dvLT4ZXiRJAgtyRm43NlkagT-uKNK7PLV7JBk6xeoq7wFS4phkFqcm4QBvO5vRy-sbTrWsRtJLMfSNxwBwOLOMJZJtktw0TF0vSgjoZ9XetO5zrfbdDbiBlyfR2Oul_l-8ZAdT08YMsPiZciX04bt9KNwtfb-RhnfRAn_Ga8Uf4RLwVR5vWl9YgIxbTGPAilmhIXYbpNNo2DBmG8VX4QB5eIyWG-Or5NXDsh2IiNotJTuIomXWmmag1fwZp6yfn4uVDYih0fGDLWgsMribvqpocZ9_7Jp3gAgt4PL3MUy1SqnMgDh6B2p1wOvGPOA6wEIqZN79vZWIUIDmMo6qbABbJ73X3lQWWDQ2l-46X9H9_G290izWRQliNiFnzt-AIysMKQZ1h0M0AVCdW9v9guXL0A4VOWYPyiL1dPqznyx0P2PmtlxkwUgRd2esd5opet3hzTaEpjlCGthXuyObciWKwCYQ-24eufpqhcSzkxr-oVHJdwBdz4YHg9gapJtZIA9Ir7rroEAHYkSjC1LdtHSoUm6A_OTis9YPQ1RlsqVXCded0z_29pAe_VvFUBGgqA_A2Qc8Rd-tuGxbg25ZfxAqZc3zGuZJBycR1De6h8F0V983Ra-OLFoPq5AGXSWy3oEUebHznH2uATtILQXlDwLdM46WQYyrVD_soc9KAo97OyokmqRhae12-osbx6fH7TWzTIvwSlwJzQSt3BVI5oBgx7bVG4RMl9kjKpni_pakfSf_8qKnRLhqAC8tel99tgvsszCPZVGI78exYPqHDb1jNE2SMxOb2DReEB5_KxuDcIeVoWg3bzSzFththrQ-fDAL_gN8fdFRigac2z2OnuP8jeBY-t-Si6zVJJD94-gsJZVc5OjHBOpYlMZvWguglA6GE3JyRsUE3rcJKPkjXJpPzBPrRg4ilMuxJSAyyU2fz-vJB_KxrMlLeN499cWB7-k9GTVHUuiYg7Wx1R5PY42CY01MHnERCpMsIDEvS142vfpc-zJbBxok5eWp-BHFiUlNW5DgO-KTJt50XzAFQwec1x80GZ6xB0_0ElOulY9FJwlsJPRZT9It6Br2eCKAorXPH_5gPctngA3UyN36bBvKNpeL0dd77i_GGkrDx2xw-BAIGTB2flBYX_E4Lj2iTbzxNY9-tAs-o1hjGgWMHBlQpJYh4Gjx8TZPgeh07xqTl3whqtyUED6giN8e8Q0y5QPCuGWXoLgJFw9cULYxYYC5pBBnuR7zGd2tMJIFCbW9_FdMR9i_KRyNYbgFLtv6ef_tjt6mrKnFzrLttReM0NVuTw3H1HN6d5H1NNecQOz3j4ZVt5BBpzpPI-JY9RWppcn32R2JRx3A-qBI7Z9F1bN_1OR1u97PNuD9r-3Ql8fAiYbuSYwUeBQjfdrz9x3LVN8oV6VzdTQeVwrIkpYD4v2BZpEmduxjj_JK4ccZbs5_yFhBTfZhNCYKa2kiAT9B8W6z1hGsKXukhweZmukgukZk74uhHYC87EwLBgYnXabv4xuOGJ_Yzzpo_NICGu91UbmNXax_1z8Ihj9B42H9ev47QrtqpwHjBDAOSzZg-EF5fIIVCvzJzBTVt03-xpoChwgPMtROcQozflzJZWNitJ9g6vvCBIbbnNts7KERf6UbNJqCMGFUzPPkSBQrgNXWjCDaAPoZh1moK3P80m29NymxkC-goZaujPkzz3CluP6nxSxnDZRc2tXaIBc1ILqFhcHwYOHFXnrp-klg3s5iwwuojOpfHME8GR__0XxuQequnG3y6fmlsTGvx4lrGAuGnNzfEkFQLcAxLulik1cA1eUnPyPqmzz7Zn0NHvo5a9JzRJaDnls4F4k2JTjWgawlYcOrO7Zue5KMFdhZ2kdQTixjdvJXEGlqws_wAyAk1968Oy8NYpgx_4yVQrDWsI8ototiDJiRY76jX6FnWtxxL1b-6Yqu-ql4J5wAhUzK7fBCp75ALmtcD9skiSz5NuV73d0_r0pxqSJzsWqLreBnSqEkTjDQsxJOBlS6ttrlN-L-DqtVUbvLyND577BjoqSs46PvHjmBeDM4y5YOc1kHC7bZ8tcq1pV17WkNeuv0f1K4TTGXNXVTCYoAJgOuu8qpyDLmP0A14WOcRX0O27w-CTdGRFQCt20QUcHaswfi4JuGcrKJ_ZyyZ5qwcV94srL5a-CEAka65uocRGgBG-tXXogz-seNCRvWpcVzmwMNLl5M0IvqqBvD8IKbH9I4Y4sw7ID1eXqU_9Du69MeiA2lgq73c16bn0jSdw5O1_vbZzO5oN51ESaIVyP_j48tivqFUO51g58ZIcbNSRyh6SblY3LP0Ij94YOVCSeOQNT6cA8KP84EawysNwRAcqzDVU7eHJ_uCKq_wev6OXzCkaoMy7JbTt_OH4sHrU7gi7kG-hhlYkjJNF_PQS9Z-kE97J1eY6GTLW40s.B2eLkng_TQwf5X-mRkFpsu1zLhxQLsjhoYvsGgg0_hA"

payload='{"instructedAmount":{"amount":"1","currency":"EUR"},"creditorAccount":{"iban":"AT861921125678901234"},"creditorName":"Laura Musterfrau"}'

payloadDigest=`echo -n "$payload" | openssl dgst -binary -sha256 | openssl base64`
digest=SHA-256=$payloadDigest
echo "Digest: ${digest}"

reqDate=$(LC_TIME=en_US.UTF-8 date -u "+%a, %d %b %Y %H:%M:%S GMT")

reqId=`uuidgen`

signingString="(request-target): $httpMethod $reqPath
date: $reqDate
digest: $digest
x-request-id: $reqId"

# signingString must be declared exactly as shown below in separate lines
signature=`printf %s "$signingString" | openssl dgst -sha256 -sign "${certPath}example_client_signing.key" -passin "pass:changeit" | openssl base64 -A`

# Curl request method must be in uppercase e.g "POST", "GET"
curl -i -X POST "${httpHost}$reqPath" \
-H "Accept: application/json" \
-H "Content-Type: application/json" \
-H "Digest: ${digest}" \
-H "Date: ${reqDate}" \
--user-agent "openbanking-get-started/1.0.0 bash" \
-H "TPP-Redirect-URI: https://example.com/redirect" \
-H "PSU-IP-Address: 37.44.220.0" \
-H "X-Request-ID: ${reqId}" \
-H "Authorization: Bearer ${accessToken}" \
-H "Signature: keyId=\"$keyId\",algorithm=\"rsa-sha256\",headers=\"(request-target) date digest x-request-id\",signature=\"$signature\"" \
-d "${payload}" \
--cert "${certPath}example_client_tls.cer" \
--key "${certPath}example_client_tls.key"
