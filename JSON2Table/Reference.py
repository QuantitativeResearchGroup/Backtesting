import psycopg2
import pandas as pd
import yfinance as yf
from pulldata import *
from datetime import datetime
# Suppress pandas warnings
pd.options.mode.chained_assignment = None

conn = psycopg2.connect(
    dbname='MyDatabase',
    user='postgres',
    password='bobwashere',
    host='localhost',
    port=5432
)
cur = conn.cursor()

create_keyfacts_table_query = """
CREATE TABLE IF NOT EXISTS Reference (
    "Ticker.Exchange" VARCHAR(50) PRIMARY KEY,
    "Ticker.Date" TEXT,
    Ticker VARCHAR(10),
    StockExchange VARCHAR(50),
    Name VARCHAR(100),
    CIK NUMERIC(10,2),
    Industry VARCHAR(50),
    Sector VARCHAR(50),
    LongDescription TEXT,
    Website VARCHAR(255),
    HeadQuarter TEXT,
    Founded TEXT
);
"""
cur.execute(create_keyfacts_table_query)

get_tickers_query = "SELECT symbol FROM sp500wiki;"
cur.execute(get_tickers_query)
tickers = [record[0] for record in cur.fetchall()]
tickers = tickers[0:3]
#print(tickers)
a, b, c, d = pulldata(tickers)

# Bulk insert data into a list
data_to_insert = []
for index, row in a.iterrows():
    data_to_insert.append((
        row['Ticker.Exchange'],
        row['Ticker.Date'],
        row['Ticker'],
        row['StockExchange'],
        row['Name'],
        row['Industry'],
        row['Sector'],
        row['Website'],
        row['HeadQuarter'],
        row['Founded'],
        row['LongDescription']
    ))

insert_query = """
INSERT INTO Reference ("Ticker.Exchange", "Ticker.Date", Ticker, StockExchange, Name,  Industry, Sector, Website, HeadQuarter, Founded, LongDescription)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

# method that only deals with the database (bulk). add to auxillary.py
#

# Bulk insert data into the database
cur.executemany(insert_query, data_to_insert)

conn.commit()
cur.close()
conn.close()
