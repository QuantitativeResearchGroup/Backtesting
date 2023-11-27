import yfinance as yf

msft = yf.Ticker("MSFT")

# get all stock info
msft.info

# get historical market data
hist = msft.history(period="1mo")

# show meta information about the history (requires history() to be called first)
#print(msft.history_metadata)


#print(msft.actions)
#print(msft.dividends)
#print(msft.splits)
#print(msft.capital_gains)  # only for mutual funds & etfs

# show share count
#print(msft.get_shares_full(start="2022-01-01", end=None))

# show financials:
# - income statement
#print(msft.income_stmt)
print(msft.quarterly_income_stmt)
# - balance sheet
#print(msft.balance_sheet)
#print(msft.quarterly_balance_sheet)
# - cash flow statement
#print(msft.cashflow)
#print(msft.quarterly_cashflow)

#print(msft.earnings_dates)