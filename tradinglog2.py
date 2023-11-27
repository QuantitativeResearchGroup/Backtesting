import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import yfinance as yf
from strategies import *
from auxillary import *

tickers = {"AAPL": 1.0}
start_date = "2018-01-01"

for ticker, target in tickers.items():
    #start_date = set_data_timeframe(start_date)
    data = yf.download(ticker, start=start_date, end="2022-12-31")
    data = bt.feeds.PandasData(dataname=data)

    cerebro = bt.Cerebro()  
    cerebro.adddata(data, name=ticker)
    cerebro.addstrategy(SmartCross)
    cerebro.broker.setcash(1000000.0)
    cerebro.addsizer(bt.sizers.PercentSizer, percents=10)
    cerebro.addanalyzer(btanalyzers.SharpeRatio, _name="sharpe")
    cerebro.addanalyzer(btanalyzers.Transactions, _name="trans")
    cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name="trades")

    print(f'Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())
    back = cerebro.run()
    #date_to_analyze = "2022-10-16"  # Replace with your desired date
    print(f'Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

    sharpe = back[0].analyzers.sharpe.get_analysis()
    trans = back[0].analyzers.trans.get_analysis()
    trades = back[0].analyzers.trades.get_analysis()

    cerebro.plot()[0]
    
    
    specific_date = datetime(2020, 10, 1)
    # loop for window
    # start end
    # 
    portfolio_info = get_portfolio_value_at_date(cerebro.runstrats[0][0],start_date, specific_date, 1000000.0)  # Access the strategy using cerebro.runstrats
    
    print("Portfolio Information for", portfolio_info['Date'])
    print("Portfolio Value:", portfolio_info['Portfolio Value'])
    print("Number of Trades:", portfolio_info['Number of Trades'])
    print("Open Positions:", portfolio_info['Open Positions'])
    print("Total Profit/Loss:", portfolio_info['Total Profit/Loss'])