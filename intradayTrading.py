import backtrader as bt
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import backtrader.analyzers as btanalyzers
from strategies import *
import matplotlib.pyplot as plt

stocks = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
startdate = '2022-01-01'
enddate = '2023-10-01'

##
for symbol in stocks:
    stock = yf.Ticker(symbol)
    data = stock.history(period="1d", start=startdate, end=enddate)
    previous_closing_price = data["Close"].iloc[-2]  # Use iloc[-2] to get the second-to-last day
    sma_50 = data['Close'].rolling(window=50).mean().iloc[-1]
    sma_200 = data['Close'].rolling(window=200).mean().iloc[-1]

    print(f"Previous Day's Closing Price for {symbol}: {previous_closing_price:.2f}")
    print(f"SMA(50) for {symbol}: {sma_50:.2f}")
    print(f"SMA(200) for {symbol}: {sma_200:.2f}")
    
    
## Backtrader Algorithm
if __name__ == '__main__':
    cerebro = bt.Cerebro()
    for symbol in stocks:
        data = bt.feeds.PandasData(dataname=yf.download(symbol, start=startdate, end=enddate))
        cerebro.adddata(data)


    cerebro.adddata(data)
    cerebro.addstrategy(MaCrossStrategy) #IntradayVWAPStrategy)
    cerebro.broker.setcash(1000000.0)

    cerebro.run()
    cerebro.plot()