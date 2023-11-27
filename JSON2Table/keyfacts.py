import psycopg2
import pandas as pd
import yfinance as yf
from pulldata import *
# Suppress pandas warnings
pd.options.mode.chained_assignment = None

# Get the list of S&P 500 tickers
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
table = pd.read_html(url)[0]
tickers = table['Symbol'].str.replace('.', '-').to_list()
tickers = tickers[0:10]
#print(tickers)
a,b,c,d = pulldata(tickers)

print(a)

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname='MyDatabase',
    user='postgres',
    password='bobwashere',
    host='localhost',
    port=5432
)

# Create a cursor to execute SQL queries
cur = conn.cursor()

# Create the "keyfacts" table if it doesn't exist
create_keyfacts_table_query = """
CREATE TABLE IF NOT EXISTS keyfacts (
    Ticker VARCHAR(10) PRIMARY KEY,
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

# Load data from the DataFrame into the "keyfacts" table
for index, row in a.iterrows():
    insert_query = """
    INSERT INTO keyfacts (Ticker, StockExchange, Name, Industry, Sector, LongDescription, Website, "52WeekHigh", "52WeekLow", Volume)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """
    cur.execute(insert_query, (
        row['Ticker'],
        row['StockExchange'],
        row['Name'],
        row['Industry'],
        row['Sector'],
        row['LongDescription'],
        row['Website'],
        row['52WeekHigh'],
        row['52WeekLow'],
        row['Volume']
    ))

# Commit the changes to the database
conn.commit()

# Close the cursor and the connection
cur.close()
conn.close()
