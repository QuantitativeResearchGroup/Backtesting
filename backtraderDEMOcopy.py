import backtrader as bt
import backtrader.analyzers as btanalyzers
import matplotlib
from datetime import datetime
from strategies import *


cerebro = bt.Cerebro()
# from data.txt
data = bt.feeds.YahooFinanceData(dataname = 'oracle.txt', fromdate = datetime(2010, 1, 1), todate = datetime(2020, 1, 1))
cerebro.adddata(data)

# strategy implementation
cerebro.addstrategy(SmartCross)
cerebro.broker.setcash(1000000.0)
cerebro.addsizer(bt.sizers.PercentSizer, percents = 10)
# cerebro.addsizer(bt.sizers.SizerFix, stake=3)

# https://www.backtrader.com/docu/analyzers/analyzers/
cerebro.addanalyzer(btanalyzers.SharpeRatio, _name = "sharpe")
cerebro.addanalyzer(btanalyzers.Transactions, _name = "trans")
cerebro.addanalyzer(btanalyzers.TradeAnalyzer, _name = "trades")
#cerebro.addanalyzer(btanalyzers.Alpha, _name = "alpha")  # attributes

# performance
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue()) 
back = cerebro.run()
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())


back[0].analyzers.sharpe.get_analysis()
back[0].analyzers.trans.get_analysis()
back[0].analyzers.trades.get_analysis()
 
# plot 
cerebro.plot()[0]


 