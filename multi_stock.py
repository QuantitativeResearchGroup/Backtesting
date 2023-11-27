from datetime import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import yfinance as yf
from strategies import *
from auxillary import *

tickers = [ "MSFT","AAPL"]

cerebro = bt.Cerebro()
cerebro.broker.setcash(1000000.0)
#print("A")
for ticker in tickers:
    data = yf.download(ticker, start="2022-01-01", end="2022-12-31")
    data = bt.feeds.PandasData(dataname=data)
    #print("B", ticker)
    cerebro.adddata(data, name=ticker)

cerebro.addstrategy(TestStrategy)
cerebro.addsizer(bt.sizers.PercentSizer, percents=10)


# create custom fucntion for later ratio or call to get details
# position, size, value, date
# 
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
cerebro.addanalyzer(btanalyzers.Transactions, _name="trans")
cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name="trades")

print(f'Starting Portfolio Value: {cerebro.broker.getvalue():.2f}') # print date
back = cerebro.run()
print(f'Final Portfolio Value: {cerebro.broker.getvalue():.2f}')

sharpe = back[0].analyzers.sharpe.get_analysis()
trans = back[0].analyzers.trans.get_analysis()
trades = back[0].analyzers.trades.get_analysis()


# # Define a list of specific dates for analysis
# specific_dates = ["2022-01-05", "2022-07-04", "2022-11-01"]
# for date in specific_dates:
#     specific_date = datetime.strptime(date, "%Y-%m-%d").date()

#     try:
#         data = yf.download(ticker, start="2022-01-01", end=specific_date)
#         data = bt.feeds.PandasData(dataname=data)
#         #data.target = target

#         cerebro = bt.Cerebro()
#         cerebro.adddata(data, name=ticker)
#         cerebro.addstrategy(SmartCross)
#         cerebro.broker.setcash(1000000.0)
#         cerebro.addsizer(bt.sizers.PercentSizer, percents=10)

#         back = cerebro.run()
#         print(f'Portfolio Value on {specific_date}: %.2f' % cerebro.broker.getvalue())
#         #print(((cerebro.broker.getvalue() / 1000000.0) - 1) * 100)
#         portfolio_info = get_portfolio_value(cerebro.runstrats[0][0], specific_date)  # Access the strategy using cerebro.runstrats
    
#         print("Portfolio Information for", portfolio_info['Date'])
#         print("Portfolio Value:", portfolio_info['Portfolio Value'])
#         print("Number of Trades:", portfolio_info['Number of Trades'])
#         print("Open Positions:", portfolio_info['Open Positions'])
#         print("Total Profit/Loss:", portfolio_info['Total Profit/Loss'])
#     except Exception as e:
#         print(f"Data is not available for {specific_date}. Error: {e}")
        
        
# insert and read data from python
# pyscopg2
# data extraction into securities, exchange, companies
# .py write a method to
#      extract based on date (after or range) (time filter)
#      duplicates
