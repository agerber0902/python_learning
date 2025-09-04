import json
import requests
from textwrap import dedent
import pandas as pd
from pandas import DataFrame

from utilities.utilities import _check_arg
from helpers.constants import FANTASY_MATH_API_URL
from helpers.helper import printInfo, printError

def get_players(token,  qb='pass_6', skill='ppr_1', dst='dst_std', week=None,
                season=None):

    _check_arg('qb scoring', qb, ['pass_6', 'pass_4'])
    _check_arg('rb/wr/te scoring', skill, ['ppr_1', 'ppr_0', 'ppr_1over2'])
    _check_arg('dst scoring', dst, ['dst_high', 'dst_std'])

    arg_string = f'qb: "{qb}", skill: "{skill}", dst: "{dst}"'

    variables = ['player_id', 'name', 'pos', 'fleaflicker_id', 'espn_id',
                 'yahoo_id', 'sleeper_id', 'team']

    if (week is not None) and (season is not None):
        arg_string = arg_string + f', season: {season}, week: {week}'
        variables = variables + ['actual']

    query_available = dedent(
        f"""
        query {{
            available({arg_string}) {{
                {','.join(variables)}
            }}
        }}
        """)

    r = requests.post(FANTASY_MATH_API_URL, json={'query': query_available},
                  headers={'Authorization': f'Bearer {token}'})

    raw = json.loads(r.text)['data']

    printInfo(f"Returning players with arg_string(s): {arg_string}")

    if not raw or not raw.get('available'):
        raise ValueError("Something went wrong. No data.")
    else:
        return DataFrame(raw['available'])