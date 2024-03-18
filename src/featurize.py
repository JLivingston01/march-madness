"""
This script featurizes the table of raws in the sqlite db.
"""

import pandas as pd
import sqlite3
import datetime as dt
import logging
import numpy as np

## FEATURE FUNCS

def strip_and_make_0_float(x: str) -> float:
    """
    Special purpose function for saving only a float value found at front of a string in stats data.

    Args:
        x (str): string that contained a float followed by multiple pieces of metadata space-separated

    Returns:
        float: value pulled from string
    """
    return x.str.split(expand=True)[0].astype(float)

def featurize(table: pd.DataFrame) -> pd.DataFrame:
    """
    Takes a table of stats data and returns additional feature columns for ML processes.

    Args:
        table (pd.DataFrame): Table of Raws

    Returns:
        pd.DataFrame: DF with features
    """
    table[['w','l']]=table['rec'].str.split(expand=True)[0].str.split("–",expand=True).astype(int)
    table['win_perc'] = table['w']/(table['w']+table['l'])

    table['tourney'] = np.where(
        table['team'].str.contains('CHAMPS'),'CHAMPS',
        np.where(
        table['team'].str.contains('Finals'),'Finals',
        np.where(
        table['team'].str.contains('Final Four'),'Final Four',
        np.where(
        table['team'].str.contains('Elite Eight'),'Elite Eight',
        np.where(
        table['team'].str.contains('Sweet Sixteen'),'Sweet Sixteen',
        np.where(
        table['team'].str.contains('R32'),'R32',
        np.where(
        table['team'].str.contains('R64'),'R64',
        np.where(
        table['team'].str.contains('R68'),'R68',
        'no tourney'
        )
        )
        )
        )
        )
        )
        )
    )

    table['team']=table['team'].str.split(",",expand=True)[0]
    table['team'] = table['team'].str.replace(" seed","").apply(
        lambda x: ''.join([i for i in x if (i.isalpha())|(i==" ")])
    ).str.strip()

    tourney_values = {
        'no tourney':128,
        'R68':68,
        'R64':64,
        'R32':32,
        'Sweet Sixteen':16,
        'Elite Eight':8,
        'Final Four':4,
        'Finals':2,
        'CHAMPS':1,
    }

    table['OUTCOME'] = table['tourney'].map(tourney_values)

    table['adjoe'] = strip_and_make_0_float(table['adjoe'])
    table['adjde'] = strip_and_make_0_float(table['adjde'])
    table['barthag'] = strip_and_make_0_float(table['barthag'])
    table['efg_pct'] = strip_and_make_0_float(table['efg_pct'])
    table['efgd_pct'] = strip_and_make_0_float(table['efgd_pct'])
    table['tor'] = strip_and_make_0_float(table['tor'])
    table['tord'] = strip_and_make_0_float(table['tord'])
    table['orb'] = strip_and_make_0_float(table['orb'])
    table['drb'] = strip_and_make_0_float(table['drb'])
    table['ftr'] = strip_and_make_0_float(table['ftr'])
    table['ftrd'] = strip_and_make_0_float(table['ftrd'])
    table['2p_pct'] = strip_and_make_0_float(table['2p_pct'])
    table['2pd_pct'] = strip_and_make_0_float(table['2pd_pct'])
    table['3p_pct'] = strip_and_make_0_float(table['3p_pct'])
    table['3pd_pct'] = strip_and_make_0_float(table['3pd_pct'])
    table['3pr'] = strip_and_make_0_float(table['3pr'])
    table['3prd'] = strip_and_make_0_float(table['3prd'])
    table['adj_t'] = strip_and_make_0_float(table['adj_t'])
    table['wab'] = strip_and_make_0_float(table['wab'])

    conferences = ['WCC', 'Amer', 'B12', 'ACC', 'SEC', 'BE', 'P12', 'B10', 'MWC',
        'MVC', 'A10', 'OVC', 'CUSA', 'AE', 'SC', 'WAC', 'Sum', 'CAA',
        'MAAC', 'MAC', 'Ivy', 'ASun', 'Pat', 'SB', 'BW', 'BSth', 'BSky',
        'NEC', 'Horz', 'SWAC', 'MEAC', 'Slnd']

    for c in conferences:
        table[c] = np.where(table['conf']==c,1,0)

    return table

def main():

    logging.basicConfig(level=logging.INFO)

    logging.info("Loading RAW")

    conn = sqlite3.Connection("artifacts/data/db.sqlite3")

    dat = pd.read_sql('select * from RAW',
    con=conn)

    logging.info("Featurizing RAW -> FEATURES")

    features = featurize(dat)
    
    logging.info("Storing FEATURES")

    features.to_sql(name='FEATURES',con=conn,if_exists='replace',index=False)

    logging.info("Featurizing SUCCESS")

    return None

if __name__=='__main__':
    main()

