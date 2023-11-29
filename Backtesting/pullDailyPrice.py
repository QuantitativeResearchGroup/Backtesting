'''
- Pull Daily Stock Price Data -
Retrieve daily price data for stocks from sp500wiki table. It tabulates the data into two tables:
yfdailyprice. It checks the table for most recent date netry and starts the fill from that 
date to current datestamp.
'''

import yfinance as yf
import pandas as pd
from SP500Wiki import *
from Methods import *

conn = establish_database_connection()
cur = conn.cursor()

# Ticker Extraction
get_tickers_query = "SELECT symbol FROM sp500wiki;"
cur.execute(get_tickers_query)
tickers = [record[0] for record in cur.fetchall()]
tickers = tickers[0:2]

for ticker_symbol in tickers:
    ticker = yf.Ticker(ticker_symbol)
    
    # Fetching latest date from the database
    latest_date = get_latest_daily_date(cur, ticker_symbol)
    # Setting the end date as the current date
    enddate = datetime.now().strftime('%Y-%m-%d')
    # Using the latest date from the database as the start date
    startdate = latest_date if latest_date else datetime.now().replace(day=15).strftime('%Y-%m-%d')
  # Use enddate if no latest date is found
    
    # Get daily data
    data = ticker.history(start=startdate, end=enddate)
    if not data.empty:
        data['Ticker'] = ticker_symbol
        data.reset_index(inplace=True)
        data['Date'] = data['Date'].dt.strftime('%Y-%m-%d')
        data_list = data.to_dict('records')
        update_or_insert_yf_daily_data(cur, ticker_symbol, data_list)

conn.commit()
cur.close()
