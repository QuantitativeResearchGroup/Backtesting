import yfinance as yf
from SP500Wiki import *
from methodsNEW import *


# Establish the database connection and cursor
conn = establish_database_connection()
cur = conn.cursor()

# Replace 'AAPL' with the ticker symbol you want to test
ticker_symbol = 'AAPL'

# Test the get_latest_daily_date function
latest_date = get_latest_daily_date(cur, ticker_symbol)
print(f"Latest Daily Date for {ticker_symbol}: {latest_date}")

# Test the set_daily_date_ranges function
start_date, end_date = set_daily_date_ranges(cur, ticker_symbol)
print(f"Start Date: {start_date}")
print(f"End Date: {end_date}")

# Close the database cursor and connection
cur.close()
conn.close()
