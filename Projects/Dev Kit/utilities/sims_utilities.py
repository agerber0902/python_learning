from pandas import DataFrame, Series
import pandas as pd
import json
import requests

from utilities.player_utilities import get_players
from utilities.utilities import _check_arg

from helpers.constants import FANTASY_MATH_API_URL
from helpers.helper import printError, printInfo

def remaining_teams_this_week(token):
    query = f"""
        query {{
            remaining_teams_this_week 
        }}
        """

    r = requests.post(FANTASY_MATH_API_URL, json={'query': query},
                  headers={'Authorization': f'Bearer {token}'})
    raw = json.loads(r.text)['data']

    if raw is None:
        printError("No data. Check token.")
        return []

    return raw['remaining_teams_this_week']

def get_sims_from_roster(token, rosters, nsims=100, **kwargs):
    """
    Takes a league roster input, which is a DataFrame with player_id + any
    points scored so far (if running midweek).

    Uses that to get sims for players yet to to play. Adds in players actual
    scores if they played.
    """

    # teams still to play
    teams_to_play = remaining_teams_this_week(token)

    # add in team to rosters
    # available players (need this because it has team)
    players = get_players(token, **kwargs).set_index('player_id')
    rosters = pd.merge(rosters, players[['team']].reset_index(), how='left',
                       indicator=True)

    # print a warning for anyone in rosters that isn't available
    if (rosters['_merge'] == 'left_only').any():
        printInfo("No sims available for:")
        printInfo(rosters.query("_merge == 'left_only'"))

    rosters.drop('_merge', axis=1, inplace=True)

    # now get sims for players who have yet to play

    played = rosters['team'].apply(lambda x: x not in teams_to_play)
    players_to_get = list(rosters.loc[~played, 'player_id'])

    if len(players_to_get) == 0:
        sims = DataFrame(columns=list(rosters['player_id']), index=range(nsims))
    else:
        sims = get_sims(token, players_to_get, nsims=nsims, **kwargs)

    # add in any actual scores
    for i, row in rosters.set_index('player_id').iterrows():
        if i in players_to_get:
            continue
        else:
            if pd.isna(row['actual']):
                sims[i] = 0
            else:
                sims[i] = row['actual']

    return sims

def get_sims(token, players, qb='pass_6', skill='ppr_1', dst='dst_std',
             nsims=100, week=None, season=None):

    ###########################
    # check for valid arguments
    ###########################
    _check_arg('week', week, range(1, 19), none_ok=True)
    _check_arg('season', season, range(2020, 2026), none_ok=True)
    _check_arg('qb scoring', qb, ['pass_6', 'pass_4'])
    _check_arg('rb/wr/te scoring', skill, ['ppr_1', 'ppr_0', 'ppr_1over2'])
    _check_arg('dst scoring', dst, ['dst_high', 'dst_std'])

    player_str = ','.join([f'"{x}"' for x in players])

    arg_string = f'qb: "{qb}", skill: "{skill}", dst: "{dst}", nsims: {nsims}, player_ids: [{player_str}]'

    if (week is not None) and (season is not None):
        arg_string = arg_string + f', season: {season}, week: {week}'

    query = f"""
        query {{
            sims({arg_string}) {{
                players {{
                    player_id
                    sims
                }}
            }}
        }}
        """

    # send request
    r = requests.post(FANTASY_MATH_API_URL, json={'query': query},
                  headers={'Authorization': f'Bearer {token}'})
    raw = json.loads(r.text)['data']

    if raw is None:
        printError("No data. Check token.")
        return DataFrame()

    return pd.concat([Series(x['sims']).to_frame(x['player_id']) for x in
        raw['sims']['players']], axis=1)

def get_sims_from_file(filename):
    sims = pd.read_csv(filename)
    sims.columns = [int(x) for x in sims.columns]
    return sims

def name_sims(sims, players):
    if 'player_id' in players.columns:
        players = players.set_index('player_id').copy()
    sims = DataFrame(sims, copy=True)
    sims.columns = list(players.loc[sims.columns, 'name']
                        .str.lower()
                        .str.replace('.','', regex=False)
                        .str.replace(' ', '-', regex=False))
    return sims

def update_sims_with_actual(sims, rosters):
    players_w_pts = rosters.query("actual.notnull()")
    for player, pts in zip(players_w_pts['player_id'], players_w_pts['actual']):
        sims[player] = pts
    return sims