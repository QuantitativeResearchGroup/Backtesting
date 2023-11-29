# https://teddykoker.com/2019/04/backtesting-a-cross-sectional-mean-reversion-strategy-in-python/
# 
import pandas as pd
import pandas_datareader.data as web
import backtrader as bt
import numpy as np
from datetime import datetime 
from concurrent import futures 


data = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
table = data[0]
tickers = table.iloc[1:, 0].tolist()  # Adjust indexing based on the DataFrame structure
pd.Series(tickers).to_csv("spy/tickers.csv")


end = datetime.now() 
start = datetime(end.year - 5, end.month , end.day)
bad = []

def download(ticker):
    df = web.DataReader(ticker,'iex', start, end)
    df.to_csv(f"spy/{ticker}.csv")

with futures.ThreadPoolExecutor(50) as executor: 
    res = executor.map(download, tickers) 
    
class CrossSectionalMR(bt.Strategy):
    def prenext(self):
        self.next()
    
    def next(self):
        # only look at data that existed yesterday
        available = list(filter(lambda d: len(d), self.datas)) 
        
        rets = np.zeros(len(available))
        for i, d in enumerate(available):
            # calculate individual daily returns
            rets[i] = (d.close[0]- d.close[-1]) / d.close[-1]

        # calculate weights using formula
        market_ret = np.mean(rets)
        weights = -(rets - market_ret)
        weights = weights / np.sum(np.abs(weights))
        
        for i, d in enumerate(available):
            self.order_target_percent(d, target=weights[i])
            
cerebro = bt.Cerebro(stdstats=False)
cerebro.broker.set_coc(True)

for ticker in tickers:
    data = bt.feeds.GenericCSVData(
        fromdate=start,
        todate=end,
        dataname=f"spy/tickers.csv",
        dtformat=('%Y-%m-%d'),
        openinterest=-1,
        nullvalue=0.0,
        plot=False
    )
    cerebro.adddata(data)

cerebro.broker.setcash(1_000_000)
cerebro.addobserver(bt.observers.Value)
cerebro.addanalyzer(bt.analyzers.SharpeRatio, riskfreerate=0.0)
cerebro.addanalyzer(bt.analyzers.Returns)
cerebro.addanalyzer(bt.analyzers.DrawDown)
cerebro.addstrategy(CrossSectionalMR)
results = cerebro.run()
print(f"Sharpe: {results[0].analyzers.sharperatio.get_analysis()['sharperatio']:.3f}")
print(f"Norm. Annual Return: {results[0].analyzers.returns.get_analysis()['rnorm100']:.2f}%")
print(f"Max Drawdown: {results[0].analyzers.drawdown.get_analysis()['max']['drawdown']:.2f}%")
cerebro.plot()[0][0]