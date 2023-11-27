import psycopg2
import pandas as pd
import yfinance as yf
from pulldata import *
from datetime import datetime
# Suppress pandas warnings
pd.options.mode.chained_assignment = None

from methodsNEW import *
conn = establish_database_connection()
cur = conn.cursor()


create_keyfacts_table_query = """
CREATE TABLE IF NOT EXISTS General2 (
    "Ticker.Date" TEXT PRIMARY KEY,
    "Ticker.Exchange" VARCHAR(50),
    Ticker VARCHAR(10),
    StockExchange VARCHAR(50),
    Name VARCHAR(100),
    Industry VARCHAR(50),
    Sector VARCHAR(50),
    LongDescription TEXT,
    Website VARCHAR(255),
    "52WeekHigh" NUMERIC(10, 2),
    "52WeekLow" NUMERIC(10, 2),
    Volume INT
);
"""
cur.execute(create_keyfacts_table_query)

get_tickers_query = "SELECT symbol FROM sp500wiki;"
cur.execute(get_tickers_query)
tickers = [record[0] for record in cur.fetchall()]
tickers = tickers[0:3]
#print(tickers)
a, b, c, d = pulldata(tickers)

# function to check if a record already exists in the table
def record_exists(cur, date):
    query = """
    SELECT COUNT(*) FROM General2
    WHERE "Ticker.Date" = %s;
    """
    cur.execute(query, (date,))
    count = cur.fetchone()[0]
    return count > 0


# Define the insert query template
insert_query = """
INSERT INTO General2 ("Ticker.Exchange", "Ticker.Date", Ticker, StockExchange, Name, Industry, Sector, LongDescription, Website, "52WeekHigh", "52WeekLow", Volume)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""

# Bulk insert data into a list
data_to_insert = []
# Bulk insert data into the database with checking for existence
for index, row in a.iterrows():
    date = row['Ticker.Date']

    if not record_exists(cur, date):
        data_to_insert = (
            row['Ticker.Exchange'],
            date,
            row['Ticker'],
            row['StockExchange'],
            row['Name'],
            row['Industry'],
            row['Sector'],
            row['LongDescription'],
            row['Website'],
            row['52WeekHigh'],
            row['52WeekLow'],
            str(row['Volume'])
        )

        cur.execute(insert_query, data_to_insert)
    else:
        # Insert new entry with a different Ticker.Date
        new_date = "new_date_value"  # Provide the new Ticker.Date value
        data_to_insert = (
            row['Ticker.Exchange'],
            new_date,
            row['Ticker'],
            row['StockExchange'],
            row['Name'],
            row['Industry'],
            row['Sector'],
            row['LongDescription'],
            row['Website'],
            row['52WeekHigh'],
            row['52WeekLow'],
            str(row['Volume'])
        )

        cur.execute(insert_query, data_to_insert)


conn.commit()
cur.close()
conn.close()