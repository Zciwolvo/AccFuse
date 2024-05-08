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
certPath="../certs/ing/" # path of the downloaded certificates and keys
httpHost="https://api.sandbox.ing.com"

# httpMethod value must be in lower case
httpMethod="get"
reqPath="/v3/accounts"

# Digest value for an empty body
digest="SHA-256=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU="

# Generated value of the customer access token. Please note that the customer access token expires in 15 minutes
caccessToken="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoidHN0LTRjOGI1Mzk3LTFhYjgtNDFhOC1hNTViLWE3MTk5MTJiODNkMiIsImN0eSI6IkpXVCJ9..1EO3KX5Z5d9uLXrmacAHdA.eDK0kVCLVbjXiZAwI0BYGwDxkAAnEKlR3e7l1S-6xdV_MTTI-YJRvl_HzTSNLxL9QNAV9FWNnJRnDrw0xf4wrnoensSbSG1pVqctBjO-qmEK5m2IPwUvVESRrKhXdBoztOZAVKm4N2pIGexcMiBzimbb6dSUhwKKswWGlZMnzLkaRylIv9fSIO5-DTiqpElF2fq6cZm_TaqqbCh6wV8D4e6Ga7mQdOb5tDgOPms57jrt9ARpa6k_1o-qOCW30dgRZkOV6r4dA9vhPge1YRGszXtMiQg4RnItBzSfburKJCBANZYny6W5rTQWySyDqimmVjQngCVy06uPeQjilQ9gcKomTSxOA28wfQI_jboy6gO6zYzRZnnieYo_IFnpAnaS55diQMH0G1052XN72Zfeoct1qeXkN7X3xlGL2w0CeKvBijADuGwHFwKg-d5J5MtVkCbunk4LaOhHG4vDT9l2IZI85t4M_3tzKrhXxRDbOFygOK6HarMVQt0g7gOshl_DUjf0ab96v2eCYKga-RGNQsl9A9vmIWUP-DlfB5pE2lo37EwuKcaXF4-Va3eeSx86JIEPD_YM2ANDgwoj7phky1YuhUOkeQyjepKdG1u62YAC7HigoDUG9RnvMbCFZsoTY3daNGqCOtJDXsm1SWTOoeKGyzvxLsz_c-jU9tOIMUeikP8aDuQG0CMd8UyHF9fSArBMttrNPhT3j2Ta_0J2Ckh2KAyee-RwVvvBUyWapoF2OQABWIzlje_7mJWwwjM_9fAUaSHVTqNzFRsF1qFwEgkx6zB3LA50qdn2uGTIgkgt6UK7VMmHyz_xhEK0lfzqD0gekCE39HVYMU44w3BXCJHrHnoqsZyey2rvUSsRIesE8e7jegeIdPWfuN-bInCy5gd0HDXBx1xGLzxAoZnE7WomW7hWUeclUjNbcbYmVil1IpFZ9is3Ekks2a9pqABQGtDgD0ioOK1U-7ubyfjfcif5-Rfc1SGBan__8Rwub6pqgiKhoXge2o1md2zt8jLHlazyUslTOY_bfvhu2PFBfr6v4x5ChLE3Dv6A54GTiXcmp1Tc3tP7a4jHKLi9aB8wOHoRzHqWxefF5v7E3zIXxcztaYK3rOQJ45uafdNNyHjCHo3BKOpdbO0sFHhZtWixLvk_spK3TZ8j9D3BykuWKh_68YchIa0tzaqhzF56MVk1GWWAzRtfrP4u9yn1TM-gMbj6388PfgLKN3aG3WT1WnDMzc-NuZupTRI2oWyrIOHpWGRlafYW5EWEPO852nYqaq7K4hauMFMv0Dznq6r_5t0S7ez_UeE4jgUHAWFf7haC_NnB4po-sjBPPOhg8NIXJ8-cv_DJPlk9ZewQ-R_hM95NfM0iCfXmquNZ_K8bjp0uhOJWhRkjnYv5P2Df13UflzhoQesSM9NjqQlSPNxYhE2DPolbmdD_TIM9m4aciJBXN_UPYZoHK00o6Ifyob3FMG-Ck4hRTy9d_8Aw3T3PAvOTRXQP86fnR9JE_8HvfbRQOA7O4Z1wbUrZtnysmUGyGp7de4epdOQ-_TQ65qjeOBLqFWPQsgCjdsMpwSSn1UigTdERxtUActaI1Pss_EEiSOaa0ZGEyU2ai7CjLAnHX1N-V5Fw4l1sEtK-lneKB13PcXOI0H2Pjol2E5X2uLFtn9GSU90wwwa5ERE5KIaiDfNU47gh-W6aBYe_wCZw4z4bl7Jhpgae-m33d4gYorId9mtDD2bnWVkwBZCNMczCt1-WYnyV4exSoKddq4-gDc3QHPGyW6kRFKmCQPZoYzfXqu5Rqur375sDxkySCgUCTlWb429UzFqp5WuPjCdAijSKxF7dic3tTBowuuc0RP5EJWs96vTtwLxxuDf_WNPg73m9TYhUM5HoW-7eUBmp2zjtLPFu3tJ2tKpXNwtf6Ipe1tdGzrDoiKpC_JQLwsS1Y0R3XP3v8agRJAJogYFlkEsP2hwuMHybnyx_7l_Uu77hRrat7DQTS5RPpiv7I3o6E-DL09o96lZGkBnRLw9X_7NpvWINKw96MGYoebJ5cAtPXwEpL5RD8vTTWodbk6Dm3pTSrsJgQJURpuWCx4YIrSEchMWmtIuBr3tMHZJCUszW75-563ZNNjFt4t62UgVAky2T9o0hAJXkZX8Q2Jdtb5Kr3uPtYu2pFOfsbHXqxorZusHlxfx4NfWxKtniyUek_pibIJuWr9fupF_LmEr8lc1Lf-MPyZy8CouIg3ivIUCFz33CBet-4y7LC9Hdfb64F_wgvubVreLI3hzoxguCnmVUSI50ZqiLFLr82MGU_kJk7xxDNgn7tMvToC0on4m4l8fDmg6jl5T3rOluOXaBCDcMutLSgMDLGtH2eUO-ZXG-eKnuQu7OYlmnxE40VRZb84sZrcslDJA92kcX4rEPu0WCYggAD4v4iEpgMKFINcYNxl_wcFPJoZ_6dQWWi9WvRW8jlkqEIKlPqRcsNrmWyZ9xs88U7sMxQZSo-MmE8gVMzkugIjjqXE5ixsn9jOVgwAYt4MSN5IBVUvpNFdxhir1fyI_O31jU-xfhVuVKqft9nVXulYK3zDeNBd1C9eJRuNAhL_u7t4WVBvJzx7lL9BVKvvvjm7b0uQpM0M1KKTp_oa-6wVqfjmwlIGVwdDffqqROH-b4uhYkNn6xEJ76CIjEJGRu-EoCgomY_c_LvKtq5ZoJTu-b3LIoxzBKCnW4eyB6FRnO_uUqDcTc13DXtGCCsQDcSJ9gI3hp-C4Fi9w8NyqA8V9OPfoGu-9GPQx4jHajMJEDKh7uJXY1QvxJ0vFwGto7SRqP6_5mWWZWeU7wqKoxpw8cH2KMBdn3t9kT-ZAkXnduQDV3R0vdS2cbto3OCZgOaeVCqkZ-4UvU7umPgvmThN01cgrru412tQbC9Xxl083Csw3nE22KvYB3tKHlkspJTO4lPA4SgZhvVPTeE3WiYgu3IEe_EgxfczUVytXKcqAkpAVwbmms6DqSpr3rJcmNZMlQdJcKSsguPe0P.1AJf2B4wUgyA2PtR0ohCdYtdEHZJqRiXEV4DkkoiqTU"

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
