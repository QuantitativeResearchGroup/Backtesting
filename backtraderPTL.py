import backtrader as bt
import yfinance as yf
from strategies import *

class PandasDataExtended(bt.feeds.PandasData):
    # Add the "ticker" parameter to the data feed
    params = (('ticker', None),)
    
tickers = {"QSR": 1.0}
cerebro = bt.Cerebro()
cerebro.broker.setcash(1000000.0)
    
for ticker, target in tickers.items():
    # Download Yahoo Finance data
    data = yf.download(ticker, start="2010-01-01", end="2020-12-31")
    # Create a custom data feed with the "ticker" parameter
    data = PandasDataExtended(dataname=data, ticker=ticker)
    
    cerebro.adddata(data)

cerebro.addstrategy(SmartCross)
cerebro.addsizer(bt.sizers.FixedSize,stake=1000)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue()) 
back = cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()