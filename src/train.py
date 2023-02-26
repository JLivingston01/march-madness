"""
1. Load Features
2. Train SKLEARN model
3. Log validation metric
4. Store model object
"""

import pandas as pd
import sqlite3
import numpy as np
from joblib import dump
from sklearn.ensemble import RandomForestRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler
import logging

def rank_to_round(x):
    round_made = pd.Series(np.where(
        x==1,1,
    np.where(
        x==2,2,
    np.where(
        x<=4,3,
    np.where(
        x<=8,4,
    np.where(
        x<=16,5,
    np.where(
        x<=32,6,
    np.where(
        x<=64,7,
    np.where(
        x<=68,8,
    9
    )
    )
    )
    )
    )
    )
    )
    ),index = x.index)
    return round_made

def main():

    logging.basicConfig(level=logging.INFO)
    conn = sqlite3.Connection("artifacts/data/db.sqlite3")

    logging.info('Loading FEATURES')
    dat = pd.read_sql('select * from FEATURES',
    con=conn)

    features = ['adjoe', 'adjde', 'barthag',
        'efg_pct', 'efgd_pct', 'tor', 'tord', 'orb', 'drb', 'ftr', 'ftrd',
        '2p_pct', '2pd_pct', '3p_pct', '3pd_pct',
        'win_perc', 
        'WCC', 'Amer', 'B12', 'ACC', 'SEC',
        'BE', 'P12', 'B10', 'MWC', 'MVC', 'A10', 'OVC', 'CUSA', 'AE', 'SC',
        'WAC', 'Sum', 'CAA', 'MAAC', 'MAC', 'Ivy', 'ASun', 'Pat', 'SB', 'BW',
        'BSth', 'BSky', 'NEC', 'Horz', 'SWAC', 'MEAC', 'Slnd'
        ]
    target = 'OUTCOME'

    training_mask = dat['year'].isin([2008,
        2009,
        2010,
        2011,
        2012,
        2013,
        2014,
        2015,
        2016,
        2017,
        2018,
        2019,
        2021,])
    validation_mask = dat['year'].isin([2022])
    X = dat[training_mask][features].copy()
    y = dat[training_mask][target].copy()

    model = Pipeline(
        steps=[
        ('scaler',MinMaxScaler()),
        ('learner',RandomForestRegressor(n_estimators=500,random_state=50,#max_depth=8
                                        ))
        ]
    )

    logging.info('Training MODEL')
    model.fit(X,y)

    Xx = dat[validation_mask][features].copy()
    yy = dat[validation_mask][target].copy()
    yval = model.predict(Xx)


    logging.info('Calculating VALIDATION')
    val_result = pd.DataFrame({
        'team':dat[validation_mask]['team'],
        'OUTCOME':yy})
    val_result['PREDICTION_NUMERIC'] = yval
    val_result['PREDICTION_RANK']=val_result['PREDICTION_NUMERIC'].rank(ascending=True,)
    val_result['OUTCOME_ROUND'] = rank_to_round(val_result['OUTCOME'])
    val_result['PREDICTION_ROUND'] = rank_to_round(val_result['PREDICTION_RANK'])

    tourney_val = val_result[val_result['OUTCOME']<=68].copy()

    correlation = tourney_val[
        ['OUTCOME_ROUND','PREDICTION_ROUND']
        ].corr()['PREDICTION_ROUND'].values[0]
    
    logging.info(f'Round Correlation: {round(correlation,2)}')

    logging.info('Saving MODEL')
    dump(model,'artifacts/models/model.joblib')
    logging.info('SUCCESS')

    return

if __name__=='__main__':
    main()
    