from config.config_loader import LICENSE_KEY, OUTPUT_PATH, DB_PATH
from config.auth import get_token
import requests
from pandas import DataFrame, Series
import pandas as pd
import json
from textwrap import dedent

# constants
API_URL = 'https://api.sims.fantasymath.com'
SEASON = 2025

# Helper function to make sure argument is allowed
def _check_arg(name, arg, allowed, none_ok=False):
    if not ((arg in allowed) or (none_ok and arg is None)):
        raise ValueError(f"Invalid {name} argument. Needs to be in {allowed}.")

if __name__ == '__main__':
      print(f"Running Chapter 3 utilities.py...")
      print(f"Config sdk values: {LICENSE_KEY} | {OUTPUT_PATH} | {DB_PATH}")

      # Get Token
      token = get_token(API_URL, LICENSE_KEY)

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

      r = requests.post(API_URL, json={'query': QUERY_STR},
                        headers={'Authorization': f'Bearer {token}'})

      df = DataFrame(json.loads(r.text)['data']['available'])
      print(f"{df.head()}")
    