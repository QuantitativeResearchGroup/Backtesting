<<<<<<< HEAD
'''
- Pull Intraday Stock Price Data -
Retrieve Intraday price data for stocks from sp500wiki table. It tabulates the data into two tables:
yfintradaprice. It checks the table for most recent date netry and starts the fill from that 
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
    data2 = yf.download(ticker_symbol, period="1d", interval="1m", start=startdate, end=enddate)

    if not data2.empty:
        data2.reset_index(inplace=True)
        data2['Date'] = data2['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        data2['Ticker'] = ticker_symbol
        data2['Delta'] = data2['Close'] - data2['Open']
        data2['Hourly_RoC'] = data2['Close'].diff(periods=60)
        data2_list = data2.to_dict('records')
        update_or_insert_yf_intraday_data(cur, ticker_symbol, data2_list)

conn.commit()
=======
'''
- Pull Intraday Stock Price Data -
Retrieve Intraday price data for stocks from sp500wiki table. It tabulates the data into two tables:
yfintradaprice. It checks the table for most recent date netry and starts the fill from that 
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
    data2 = yf.download(ticker_symbol, period="1d", interval="1m", start=startdate, end=enddate)

    if not data2.empty:
        data2.reset_index(inplace=True)
        data2['Date'] = data2['Datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')
        data2['Ticker'] = ticker_symbol
        data2['Delta'] = data2['Close'] - data2['Open']
        data2['Hourly_RoC'] = data2['Close'].diff(periods=60)
        data2_list = data2.to_dict('records')
        update_or_insert_yf_intraday_data(cur, ticker_symbol, data2_list)

conn.commit()
>>>>>>> 85f750df57588cfae33da9de016c8803d69cd05b
cur.close()