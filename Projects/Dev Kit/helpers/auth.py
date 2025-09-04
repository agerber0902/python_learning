################################################################################
# auth functions
################################################################################
from textwrap import dedent
import requests
import json
from helpers.helper import setErrorMessage, printInfo, printSuccess

# Only import this, it calls both functions and retuns the token
def get_token(API_URL, LICENSE_KEY):
    token = generate_token(API_URL, LICENSE_KEY)['token']
    response = validate(API_URL, token)

    if response['validate']['validated'] != True:
        raise PermissionError(setErrorMessage(f"Token is invalid."))
    
    return token

def generate_token(API_URL, license):
    printInfo(f"Attempting to generate token for {API_URL} with key {license}")

    query_token = dedent(
        f"""
        query {{
            token (license: "{license}") {{
                success,
                message,
                token
            }}
            }}
        """)

    r = requests.post(API_URL, json={'query': query_token})
    token = json.loads(r.text)['data']['token']
    printSuccess(f"Token: {token}")
    return token

def validate(API_URL, token):
    printInfo(f"Attempting to validate token for {API_URL} with token {token}")
    query_validate = ("""
                      query {
                        validate {
                            validated,
                            message
                        }
                      }
                      """)

    r = requests.post(API_URL, json={'query': query_validate},
                  headers={'Authorization': f'Bearer {token}'})
    response = json.loads(r.text)['data']
    if response['validate']['validated'] == True:
        printSuccess(response)
    else:
        printInfo(response)
    return response