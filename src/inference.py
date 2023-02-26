"""
1. Load current year FEATURES
2. Load MODEL
3. Infer OUTCOME
4. Save PREDICTIONS to CSV
"""

import pandas as pd
import sqlite3
import numpy as np
from joblib import load
import logging

def main():
    logging.basicConfig(level=logging.INFO)

    logging.info("Loading FEATURES for 2023")
    conn = sqlite3.Connection("artifacts/data/db.sqlite3")

    dat = pd.read_sql('select * from FEATURES where year=2023',
        con=conn)

    logging.info("Loading MODEL")
    model = load('artifacts/models/model.joblib')

    features = ['adjoe', 'adjde', 'barthag',
        'efg_pct', 'efgd_pct', 'tor', 'tord', 'orb', 'drb', 'ftr', 'ftrd',
        '2p_pct', '2pd_pct', '3p_pct', '3pd_pct',
        'win_perc', 
        'WCC', 'Amer', 'B12', 'ACC', 'SEC',
        'BE', 'P12', 'B10', 'MWC', 'MVC', 'A10', 'OVC', 'CUSA', 'AE', 'SC',
        'WAC', 'Sum', 'CAA', 'MAAC', 'MAC', 'Ivy', 'ASun', 'Pat', 'SB', 'BW',
        'BSth', 'BSky', 'NEC', 'Horz', 'SWAC', 'MEAC', 'Slnd'
        ]

    X = dat[features].copy()

    logging.info("Predicting OUTCOME_PREDICTED")
    ypred = model.predict(X)

    logging.info("Saving OUTCOME_PREDICTED to /artifacts")
    val_result = pd.DataFrame({
        'TEAM':dat['team'],
        'OUTCOME_PREDICTED':ypred})

    val_result.sort_values(
        by='OUTCOME_PREDICTED'
        ).to_csv("artifacts/predictions/result.csv",index=False)

    return

if __name__=='__main__':
    main()