import yfinance as yf

# Initialize a Ticker object for the stock (e.g., Apple - AAPL)
ticker = yf.Ticker("AAPL")

# Get earnings data
earnings = ticker.earnings

# Print earnings report dates
print(earnings['Earnings Date'])




# conn = establish_database_connection()
# cur = conn.cursor()
# select_symbols_query = "SELECT Symbol FROM SP500Wiki LIMIT 10;"
# cur.execute(select_symbols_query)
# symbols = [row[0] for row in cur.fetchall()]
# stocks = ["AAPL", "NVDA", "MMM"]

# for stock in stocks:
#     ticker = yf.Ticker(stock)
#     earnings = ticker.earnings
#     if not earnings.empty:
#         earnings_dates = earnings.index.tolist()
#         print(f"Earnings report dates for {stock}: {earnings_dates}")
#     else:
#         print(f"No earnings data available for {stock}")
# cur.close()
# conn.close()

# # Print or use the list of symbols as needed
# print(symbols)