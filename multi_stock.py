import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import yfinance as yf
from strategies import *

# Define a list of 10 stock tickers with equal weights
tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "F", "NFLX", "INTC", "NVDA", "AMD"]

# Create a Cerebro instance for the entire portfolio
cerebro = bt.Cerebro()
cerebro.broker.setcash(1000000.0)
print("A")
for ticker in tickers:
    data = yf.download(ticker, start="2019-01-01", end="2022-12-31")
    data = bt.feeds.PandasData(dataname=data)
    print("B", ticker)
    # Add the data for each stock to the portfolio
    cerebro.adddata(data, name=ticker)

# Add your strategy and analyzer settings here
cerebro.addstrategy(SmartCross)
cerebro.addsizer(bt.sizers.PercentSizer, percents=10)
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
cerebro.addanalyzer(btanalyzers.Transactions, _name="trans")
cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name="trades")

# Print starting portfolio value
print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}')

# Run the portfolio
back = cerebro.run()

# Print final portfolio value
print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')

# Get analysis results for the entire portfolio
sharpe = back[0].analyzers.sharpe.get_analysis()
trans = back[0].analyzers.trans.get_analysis()
trades = back[0].analyzers.trades.get_analysis()


    # Define a list of specific dates for analysis
specific_dates = ["2013-01-05", "2016-07-04", "2019-01-01"]

for date in specific_dates:
    specific_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()

    try:
        # Create a new cerebro instance for each specific date
        data = yf.download(ticker, start="2010-01-01", end=specific_date)
        data = bt.feeds.PandasData(dataname=data)
        #data.target = target

        cerebro = bt.Cerebro()
        cerebro.adddata(data, name=ticker)
        cerebro.addstrategy(SmartCross)
        cerebro.broker.setcash(1000000.0)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=10)

        # Execute the strategy
        back = cerebro.run()
        print(f'Portfolio Value on {specific_date}: %.2f' % cerebro.broker.getvalue())
        print(((cerebro.broker.getvalue() / 1000000.0) - 1) * 100)

    except Exception as e:
        print(f"Data is not available for {specific_date}. Error: {e}")
