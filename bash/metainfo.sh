#!/bin/bash


###############################################################################
#                    REQUEST APPLICATIONS METADATA                            #
###############################################################################
  
certPath="../certs/ing/" # path of the downloaded certificates and keys
httpHost="https://api.ing.com" # production host
  
reqPath="/oauth2/applications/me"
  
accessToken="eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2Q0JDLUhTNTEyIiwia2lkIjoicHJkLThlZTk0NTIzLTAxNjMtNDMyZi1hYjgwLWFhNjU4MTFhNDBmYiIsImN0eSI6IkpXVCJ9..RDACO64bW8KGHlAvNCLQrw.IIhExDz9_3tFEXYGw64CRH3F_R1lV549riBsKbQZN-hRTf7ZMXxBZDRg4p059tJeMTQzlqpcgnLqhIUfgsJojXtlT6BaAsdeiaa3ezUFMpZv3K4gz6IwpnpHwx-nAHIiilGepkuWudcl2xO0XO_ZD0oxAi4HVuPkwqP4joth5PjZLPkQRHmuyaUYXzgPpdiJmGd9B8MAkQCqY8gG8Sa9DqOyGv92ThTYk-5fkGTuojOZtJDql4rX13K26IdT25jkvZJU8CeiE5KwxEQCZ89dbi5g3q8KQBRHjOzPPAvofrYtxbi-D18nvj2Lr1fqyDOmplrOsBuqiosnOU6GMgCt8WRYwS_Elf9AormC3FvxCsOtCnZwp8xZQ2QWMk5VfnI8RsLFdWnYnFrMkNUBPQ3JTCTP6SoINjB7Q_e0oQAKIwSh4jIJaKsIynWkYwQCxQ_-MQBIqyMuaRwVikO5w_0taziBOBRQeNeBnwlWkEfzoLV0snj2weMo6mC8dbIcdQYNOR9SImXfI-rDM7K0Mxc4wIotD2Od5X92rjaF24GyHcZreLf9SepecEBYnhcUmI7vdE5mVGFpptUwJHlRci3sBOnOokMhm8SmfjFNX3dcwjyo66Rod5wAMKONFvDmYEg4Lcf2mLzVWd5i3UNdLdCDLp0HsbqV7JlB0pFObcCRRALr3ona4bRsLrmG4w8gxY_t9d9Pz3dab_XaGJw5QWepWGzd7Eb9f0oeX_Nz8NHm6tXF-kMi4wc56GCticyC1r6nvq-QYRzkkgkhJSi3juOiyWh09bVB_MCNSSfgmzGBiVAR7VRB-2ndlqayuGvSSjapF06yvtQ6GEVvoc4UUxefOExAju-qXNFEtpxIlty98SaN1r8cxYch_7erGCjIpihAcEpDZODA1udHrA6WknYn9r1f8isWyXru185hypq40AOPp_xH87v16sIIaWu748SK388gACprrjqHoxWRNVj6ADNEpipMEavnxnOh6r3sHwjxLkuo24uANh7elu36JuZSy3hzH_Do330OQmuiBpz8Za38rPqK4nCU9zmg7-GWhFcF8iMPXNNVs0k-A1jh0utrV-bBw7gac_9aEfSrLj_7vymBA3IUPEbMVZtP6GHqEnfwVkCGc5V8q31aYaN331aHgQEQ8OKULcfvGX12Fi0WvjG0njh3qoBiUOhEqIYxfuoTNt5FHQ_lDLnmPBaq3PUS_g0khTrV_TU95YlAjwydcGPJYjhYIzOFmg4_O1cyXi3PjAP__WpQ3YSWfB7oo3Eiz4xjLQm1JBvF79-0LlzuFdbSvkAQsXCXExhm9tRmoQ_Yavm8tqnWK7fCysVW_DkmGwXYYlgOLJ8Q9DYQEDZvutR9e7-mTxezr_yDXRTzsXAs_YkHBzYPY24uwRMjU45VLswv4JQkyT7gcPfiLdIjd1XYuVpAZKVXO9hnzehAedEyAzn7-YP2dyqAj4YGS85hPyJHlpziMa1UlpA0dDvUFX9ksSvoYDYGYEpPytuD9ayOXPoJ0dhvTHqaRk5-8-djOz-Kv3cOXeYXrybjdOYR422-aRByRoYZlSOkK3xDbVI56oJvwvAFYSEbWhBXlBcfNrMPddmJ9EY8BJLHrPXy4D-wN9eFFD1E8V-DWjANTfXrE1WfUVrJtlzN0MV3dre7dAA5SWjVcPYY2b1g2rDJpIegfgAhqznaOw3leRTdFsUr-j-BO7TIfqhnbGh0f1hfyzHaGOElfChxgTNg9yxKK08UHTMXm-R5FEcCc225YNqXJpAabIM1rPRlKsp1EkdE.l3DYA9TcJ9K4vs8DKUCJXJYZfn4XxA-R-ATFkW18kmA"
  
# Curl request method must be in uppercase e.g "POST", "GET"
curl -k -X GET "${httpHost}${reqPath}" \
-H "Authorization: Bearer $accessToken" \
--cert "${certPath}example_client_tls.cer" \
--key "${certPath}example_client_tls.key"

