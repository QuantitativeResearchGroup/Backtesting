import os, sys, argparse
import pandas as pd
import backtrader as bt
import yfinance as yf
from goldencross import GoldenCross

cerebro = bt.Cerebro()
cerebro.broker.setcash(100000)
data = yf.download("SPY", start="2010-01-01", end="2020-12-31")
feed = bt.feeds.PandasData(dataname=data)
cerebro.adddata(feed)

cerebro.addstrategy(GoldenCross)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue()) 
back = cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())
cerebro.plot()
