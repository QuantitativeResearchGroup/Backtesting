from datetime import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import yfinance as yf
from strategies import *
from auxillary import *


cerebro = bt.Cerebro()

symbols = ['AAPL', 'MSFT']  # List of stock symbols

for symbol in symbols:
    data = bt.feeds.YahooFinanceData(
        dataname=symbol, fromdate="2022-01-01",
        todate="2022-04-04"
    )
    cerebro.adddata(data, name=symbol)  # Add data feed with the symbol

cerebro.addstrategy(MyStrategy1)

cerebro.broker.set_cash(100000)

cerebro.run()

# Create a DataFrame from the trade history
trade_df = pd.DataFrame(trade_history)
trade_df.set_index('Date', inplace=True)

# Print the trade history
print(trade_df)

print(f'Final Portfolio Value: {cerebro.broker.getvalue()}')
