#!/bin/bash


###############################################################################
#                             REQUEST APPLICATIION ACCESS TOKEN               #
###############################################################################
# This script requests application access token for the PSD2 APIs in the ING's#
# sandbox environment using example eIDAS certificates.     	 			  #
###############################################################################

## THE SCRIPT USES THE DOWNLOADED EXAMPLE EIDAS CERTIFICATES
keyId="SN=546212fb" # Serial number of the downloaded certificate in hexadecimal code
certPath="./certs/" # path of the downloaded certificates and keys
httpHost="https://api.sandbox.ing.com"

# httpMethod value must be in lower case
httpMethod="post"
reqPath="/oauth2/token"

# You can also provide scope parameter in the body E.g. "grant_type=client_credentials&scope=greetings%3Aview"
# scope is an optional parameter. If you don't provide a scope, the accessToken is returned for all available scopes
payload="grant_type=client_credentials"
payloadDigest=`echo -n "$payload" | openssl dgst -binary -sha256 | openssl base64`
digest=SHA-256=$payloadDigest

reqDate=$(LC_TIME=en_US.UTF-8 date -u "+%a, %d %b %Y %H:%M:%S GMT")

# signingString must be declared exactly as shown below in separate lines
signingString="(request-target): $httpMethod $reqPath
date: $reqDate
digest: $digest"

signature=`printf %s "$signingString" | openssl dgst -sha256 -sign "${certPath}example_client_signing.key" -passin "pass:123" | openssl base64 -A`

# Curl request method must be in uppercase e.g "POST", "GET"
curl -i -X POST "${httpHost}${reqPath}" \
-H 'Accept: application/json' \
-H 'Content-Type: application/x-www-form-urlencoded' \
-H "Digest: ${digest}" \
-H "Date: ${reqDate}" \
--user-agent "openbanking-get-started/1.0.0 bash" \
-H "TPP-Signature-Certificate: -----BEGIN CERTIFICATE-----MIIEdjCCA16gAwIBAgIEVGIS+zANBgkqhkiG9w0BAQsFADByMR8wHQYDVQQDDBZBcHBDZXJ0aWZpY2F0ZU1lYW5zQVBJMQwwCgYDVQQLDANJbmcxDDAKBgNVBAoMA0luZzESMBAGA1UEBwwJQW1zdGVyZGFtMRIwEAYDVQQIDAlBbXN0ZXJkYW0xCzAJBgNVBAYTAk5MMB4XDTIzMDEyNTE2MzEwMFoXDTI2MDEyNjE2MzEwMFowPjEdMBsGA1UECwwUc2FuZGJveF9laWRhc19xc2VhbGMxHTAbBgNVBGEMFFBTRE5MLVNCWC0xMjM0NTEyMzQ1MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAgV7IDXg+9U7I7MlybwuIZ3xzZ8TazJ8mvTqKak5K3fwb9ny9jfJFtSaJbWHkpb1mc/WAS4iLC/ET6tvX404mD++Ed+epTxAGQgpPDKg+rQ4O9k/QLZGNPn2ujBU12YO+N+qkK0edTFP1s/CjO4yONLA1fgY1e+0K87PyPXw0OyNqFrKTL0pFgcGB4Jt+AVCoVP0a/zxhWOj6UFxdHsktOcMBRDiLz6QuSaNv+/DmZtnujzcByG62sg2H3WV0n9jXktxqvK5xToJQAYNQg9qcRafx2WUiA6iu8x6KC/MWp0t+ZBO1ahhXz75XdXrT0ZneXLlvLH21qH/xpwrtMmbufwIDAQABo4IBRjCCAUIwNwYDVR0fBDAwLjAsoCqgKIYmaHR0cHM6Ly93d3cuaW5nLm5sL3Rlc3QvZWlkYXMvdGVzdC5jcmwwPgYIKwYBBQUHAQEEMjAwMC4GCCsGAQUFBzABhiJodHRwOi8vbXkucmV2b2NhdGlvbi50ZXN0L3Rlc3RvY3NwMB8GA1UdIwQYMBaAFEJsCqHCMVi1pneOBeelHbYQtJ9TMB0GA1UdDgQWBBRUDFfAkj5oafpiTlt9f57TZtOVGTCBhgYIKwYBBQUHAQMEejB4MAoGBgQAjkYBAQwAMBMGBgQAjkYBBjAJBgcEAI5GAQYCMFUGBgQAgZgnAjBLMDkwEQYHBACBmCcBAwwGUFNQX0FJMBEGBwQAgZgnAQIMBlBTUF9QSTARBgcEAIGYJwEBDAZQU1BfQVMMBlgtV0lORwwGTkwtWFdHMA0GCSqGSIb3DQEBCwUAA4IBAQBWu2tqCoxDMt5JDweVcz4JFul6E+E7OENmTrUjwW7IwMn+LYVRpFMLoiYkfR0XR5SzJELjZVK5b8vnd8TTrUs2F+kb34uPDuE+34MvHa0CsKGFLOgeLBnlOrsweKOupNNz6mdXe4aylJlFMRun8yO2wQ2MfnXUomK5qKwfWJYoTTWgNiIoG8RSLQwismLyihbcxn9F8UQUfh6cEaZ9VujHwNHBEdQUnMbquyH1xWUKKYi1ApZcQplBnv822fabV/5vGo+UvKYvaaxge3hgmHL8NyXGf3CLfEKGrJGlapR9bKQOCJH0KZ/K9AuqpmCGBiqTPVbMK8AJHCrKGu3zBkI2-----END CERTIFICATE-----" \
-H "authorization: Signature keyId=\"$keyId\",algorithm=\"rsa-sha256\",headers=\"(request-target) date digest\",signature=\"$signature\"" \
-d "${payload}" \
--cert "${certPath}example_client_tls.cer" \
--key "${certPath}example_client_tls.key"
