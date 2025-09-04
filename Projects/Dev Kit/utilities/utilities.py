from helpers.config_helper import LICENSE_KEY, OUTPUT_PATH, DB_PATH
from helpers.auth import get_token
import requests
from pandas import DataFrame
import pandas as pd
import json
from textwrap import dedent
from helpers.helper import printInfo

# constants
from helpers.constants import FANTASY_MATH_API_URL, SEASON

# Helper function to make sure argument is allowed
def _check_arg(name, arg, allowed, none_ok=False):
    if not ((arg in allowed) or (none_ok and arg is None)):
        raise ValueError(f"Invalid {name} argument. Needs to be in {allowed}.")



if __name__ == '__main__':
      printInfo(f"Running Chapter 3 utilities.py...")
      printInfo(f"Config sdk values: {LICENSE_KEY} | {OUTPUT_PATH} | {DB_PATH}")

      # Get Token
      token = get_token(FANTASY_MATH_API_URL, LICENSE_KEY)

      # GraphQL
      # raw graphql example

      QUERY_STR = f"""
            query {{
                  available (season: {SEASON}, week: 1) {{
                  player_id,
                  name,
                  pos,
                  actual
                  }}
            }}
            """

      r = requests.post(FANTASY_MATH_API_URL, json={'query': QUERY_STR},
                        headers={'Authorization': f'Bearer {token}'})

      df = DataFrame(json.loads(r.text)['data']['available'])
      print(f"{df.head()}")
    