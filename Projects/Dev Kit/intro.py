import pandas as pd
from os import path
import seaborn as sns

from helpers.auth import get_token
from helpers.helper import printInfo
from helpers.constants import FANTASY_MATH_API_URL, SCORING, SEASON
from helpers.config_helper import LICENSE_KEY
from utilities.player_utilities import get_players
from utilities.sims_utilities import get_sims, get_sims_from_file, name_sims

# constants
WEEK = 3
USE_SAVED_DATA = False

if __name__ == '__main__':

    printInfo(f"Calling intro.py")

    # generate token
    token = get_token(FANTASY_MATH_API_URL, LICENSE_KEY)

    # get players
    # This checks to get data from data/players.csv
    if USE_SAVED_DATA:
        players = (pd.read_csv(path.join('data', 'players.csv'))
            .set_index('player_id'))
    else:
        players = get_players(token, **SCORING, season=SEASON, week=WEEK).set_index('player_id')
        
    # print(players.head())
        
    # use this list of player ids (players.index) to get all the simulations for
    # this week
    if USE_SAVED_DATA:
        sims = get_sims_from_file(path.join('data', 'sims.csv'))
    else:
        sims = get_sims(token, players=list(players.index), week=WEEK, season=SEASON,
                        nsims=500, **SCORING)
        
    # print(sims.head())
    
    # who is player 165
    players.loc[[1091, 498]]

    nsims = name_sims(sims, players)

    # print(nsims.head())
    
    # print(nsims['justin-herbert'].mean())
    # print(nsims['justin-herbert'].median())

    # print(nsims['justin-herbert'].describe(percentiles=[0.05, .25, .5, .75, .95]))
    
    g = sns.FacetGrid(nsims, aspect=2)
    g = g.map(sns.kdeplot, 'justin-herbert', fill=True)
    g.fig.subplots_adjust(top=0.9)
    g.fig.suptitle("Justin Herbert's Fantasy Points Distribution - Wk 3, 2023")

    # print(nsims[['justin-herbert', 'patrick-mahomes']].head())

    # print((nsims['justin-herbert'] > nsims['patrick-mahomes']).head())

    # print((nsims['justin-herbert'] > nsims['patrick-mahomes']).mean())

    # run longer sim
    nsims_long = nsims[['justin-herbert', 'patrick-mahomes']].stack().reset_index()
    nsims_long.columns = ['sim_n', 'player', 'pts']
    # print(nsims_long)
    
    g = sns.FacetGrid(nsims_long, hue='player', aspect=2)
    g.map(sns.kdeplot, 'pts', fill=True)
    g.add_legend()
    g.fig.subplots_adjust(top=0.9)
    g.fig.suptitle("Herbert vs Mahomes Fantasy Points Distribution - Wk 3, 2023")

    (nsims['justin-herbert'] >
            nsims[['matthew-stafford', 'justin-fields']].max(axis=1) + 11.5).mean()

    nsims['bb_qb'] = nsims[['justin-herbert', 'matthew-stafford']].max(axis=1)
    nsims[['bb_qb', 'justin-herbert', 'matthew-stafford']].describe()

    nsims['bb_qb2'] = nsims[['justin-herbert', 'matthew-stafford',
                        'kirk-cousins']].max(axis=1)
    nsims[['bb_qb2', 'bb_qb', 'justin-herbert', 'matthew-stafford',
        'kirk-cousins']].describe().round(2)
    
    # projected vs actual vs % likelihood

    print(players.head())

    (25.68 > nsims['patrick-mahomes']).mean()

    qbs = players.loc[players['pos'] == 'QB']
    qbs['proj'] = sims.mean().round(2)


    print(qbs.sort_values('proj', ascending=False).head(15)[['name', 'proj', 'actual']])

    def fpts_percentile(row):
        return (row['actual'] > sims[row.name]).mean()
    
    # qbs['pctile'] = qbs.apply(fpts_percentile, axis=1)

    # qbs.sort_values('proj', ascending=False).head(15)[['name', 'proj', 'actual',
    #                                                 'pctile']]

    # qbs['pctile'].describe(percentiles=[.1, .2, .3, .4, .5, .6, .7, .8, .9])

    # qbs.sort_values('pctile', ascending=False).head(10)[['name', 'proj', 'actual',
    #                                                     'pctile']]

    # qbs.sort_values('pctile', ascending=False).tail(10)[['name', 'proj', 'actual',
    #                                                     'pctile']]

    # qbs.sort_values('actual', ascending=False).head(10)[['name', 'proj', 'actual',
    #                                                     'pctile']]