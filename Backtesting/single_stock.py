import datetime
import backtrader as bt
import backtrader.analyzers as btanalyzers
import yfinance as yf
import pandas as pd
#from strategies import *
from example.strategy import *
#from Strategy.Strat5VWAPRSI import *

from Methods import *


if __name__ == "__main__":
    #portfolio = ["A", "AAPL", "AAL"]  # List of tickers to process
    portfolio = ["A"]
    strategy_class = Strat1RSI  # Strat0TEST Strat0SMA Strat5VWAPRSI
    dataframes = []  
    cash = 10000.0
    start_date = "2022-01-01"
    end_date = "2023-09-20"

    for ticker in portfolio:
        data = yf.download(ticker, start=start_date, end= end_date)
        data = bt.feeds.PandasData(dataname=data)
        cerebro = bt.Cerebro()
        cerebro.adddata(data, name=ticker)
        cerebro.addstrategy(strategy_class)
        cerebro.broker.setcash(cash)
        cerebro.addsizer(bt.sizers.PercentSizer, percents=10)
        cerebro.addanalyzer(btanalyzers.SharpeRatio, _name = "sharpe")

        print(f'Starting Portfolio Value for {ticker}: %.2f' % cerebro.broker.getvalue())
        back = cerebro.run()
        final =cerebro.broker.getvalue()
        print(f'Final Portfolio Value for {ticker}: %.2f' % final)

        conn = establish_database_connection()  # Establish a database connection
        cur = conn.cursor()  # Create a database cursor
        update_or_insert_strategy_summary(cur, str(strategy_class), cash, start_date, end_date, int(final))

        #tradelogdf = strategy_class.get_trade_history_df()
        holdings = strategy_class.get_holdings_df()

        # if not tradelogdf.empty:  # Trade log
        #     for _, row in tradelogdf.iterrows():
        #         update_or_insert_tradelog_data(cur, ticker, row)
        #     conn.commit()

        if not holdings.empty:  # Holdings
            for _, row in holdings.iterrows():
                #print(ticker)
                update_or_insert_holding_data(cur, ticker, row)
            conn.commit()
            cur.close()

        #dataframes.append((ticker, tradelogdf, holdings))  # Store dataframes for this ticker

    # tradelogdf = tradelogdf.sort_values(by='Date', ascending=True)
    # for ticker, tradelogdf, holdings in dataframes:
    #     print(f"Trade Log for {ticker}:")
    #     print(tradelogdf)
    #     print(f"Holdings for {ticker}:")
    #     print(holdings)
