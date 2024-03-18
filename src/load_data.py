"""
This scripts loads raw data from tables on source pages into sqlite for downstream processing.
"""
import pandas as pd
import sqlite3
import datetime as dt
import logging

def load_page(url: str) -> pd.DataFrame:
    """Load the raw table from source into DataFrame. Also renames columns.

    Args:
        url (str): Location of table on web.

    Returns:
        pd.DataFrame
    """
    tables = pd.read_html(url)

    table = tables[0]

    table.columns = [
        'rk','team','conf','g','rec','adjoe','adjde','barthag','efg_pct','efgd_pct',
        'tor','tord','orb','drb','ftr','ftrd','2p_pct','2pd_pct','3p_pct','3pd_pct','3pr','3prd',
        'adj_t','wab'
    ]

    table = table[table['rk']!='Rk'].copy()

    return table

def main() -> None:
    """
    Main Function to load data for multiple years from source

    Returns:
        None
    """

    logging.basicConfig(level=logging.INFO)

    url_root = "https://barttorvik.com/trank.php?year={year}&type=R"

    years = [
    2008,
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
    2021,
    2022,
    2023,
    2024
         ]

    out = pd.DataFrame()
    for year in years:
        logging.info(f'Loading {year}')

        url = url_root.format(year=year)

        table = load_page(url)

        table['year']=year

        out = pd.concat([out,table])

    conn = sqlite3.Connection('artifacts/data/db.sqlite3')

    today = dt.date.today().strftime("%Y-%m-%d")
    out['load_date'] = today

    out.to_sql(name='RAW',con = conn,
               if_exists='replace',index=False)

    return None

if __name__=='__main__':
    main()
