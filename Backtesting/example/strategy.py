import backtrader as bt
import pandas as pd
from sqlalchemy import create_engine, Table, Column, Integer, String, Float, DateTime
from sqlalchemy.sql import text
import psycopg2
import json
import numpy as np
from Methods import *
from example.indicator import *
from dateutil.relativedelta import relativedelta
import datetime 
   
class MyStrategy(bt.Strategy):
    params = (('sma_period', 20),)

    def __init__(self):
        self.sma = MySimpleMovingAverage(period=self.params.sma_period)
        self.order = None

    def next(self):
        if self.order:
            return  # If an order is active, no new orders are placed

        if self.data.close[0] > self.sma[0]:  # If the close price is above SMA
            self.order = self.buy()  # Buy
        elif self.data.close[0] < self.sma[0]:  # If the close price is below SMA
            self.order = self.sell()  # Sell

    def notify_order(self, order):
        if order.status in [order.Completed, order.Canceled, order.Margin]:
            self.order = None  # Reset the order status
             
'''
'''
class Strat0TEST(bt.Strategy):
    params = (
        ('sma_period', 20),
        ('stop_loss_ratio', 2.0),
    )
    trade_history = []
    holdingsdf = []

    def __init__(self):
        self.order = None
        self.strategy_name = self.__class__.__name__
        self.sma = MySimpleMovingAverage(self.data, period=self.params.sma_period)
        #self.sma = bt.indicators.SimpleMovingAverage(self.data, period=self.params.sma_period)
        self.in_trade = False
        self.entry_price = 0.0



    def next(self):
        if not self.in_trade:
            if self.data.close[0] > self.sma[0]:
                enter_long_trade(self)
                # print("Long")

            elif self.data.close[0] < self.sma[0]:
                enter_short_trade(self)
                # print("SHort")

        elif self.in_trade:
            if self.data.close[0] < self.sma[0] or self.data.close[0] <= (1 - self.params.stop_loss_ratio) * self.entry_price:
                self.in_trade = False
                self.close()
                action = 'Sell' if self.position.size > 0 else 'Cover'
                store_trade(self, action, self.data.close[0])
                record_holding(self)

    @classmethod
    def get_trade_history_df(cls):
        return pd.DataFrame(cls.trade_history)

    @classmethod
    def get_holdings_df(cls):
        return pd.DataFrame(cls.holdingsdf)

'''
'''
class Strat0SMA(bt.Strategy):
    params = (
        ('sma_period_short', 20),  # Shorter SMA period
        ('sma_period_long', 50),   # Longer SMA period
        ('stop_loss_ratio', 2.0),
    )
    trade_history = []
    holdingsdf = []

    def __init__(self):
        self.strategy_name = self.__class__.__name__
        self.sma_short = MySimpleMovingAverage(self.data, period=self.params.sma_period_short)
        self.sma_long = MySimpleMovingAverage(self.data, period=self.params.sma_period_long)
        self.in_trade = False
        self.entry_price = 0.0

    def next(self):
        if not self.in_trade:
            if self.sma_short[0] > self.sma_long[0]:
                enter_long_trade(self)
            elif self.sma_short[0] < self.sma_long[0]:
                enter_short_trade(self)
                
        elif self.in_trade:
            if self.sma_short[0] < self.sma_long[0] or self.data.close[0] <= (1 - self.params.stop_loss_ratio) * self.entry_price:
                self.in_trade = False
                self.close()
                action = 'Sell' if self.position.size > 0 else 'Cover'
                store_trade(self, action, self.data.close[0])
                record_holding(self)
    @classmethod
    def get_trade_history_df(cls):
        return pd.DataFrame(cls.trade_history)

    @classmethod
    def get_holdings_df(cls):
        return pd.DataFrame(cls.holdingsdf)

'''
'''

class Strat1MACD(bt.Strategy):
    params = (('macd_fast', 12), ('macd_slow', 26), ('macd_signal', 9),)

    def __init__(self):
        self.macd = MyMACD(fast_period=self.params.macd_fast,
                           slow_period=self.params.macd_slow,
                           signal_period=self.params.macd_signal)
        self.buy_signal_triggered = False


    def next(self):
        if self.macd.lines.macd[0] > self.macd.lines.signal[0] and self.macd.lines.macd[-1] <= self.macd.lines.signal[-1]:
            self.buy()  # Buy signal: MACD crosses above Signal
        elif self.macd.lines.macd[0] < self.macd.lines.signal[0] and self.macd.lines.macd[-1] >= self.macd.lines.signal[-1]:
            self.sell()  # Sell signal: MACD crosses below Signal


    @classmethod
    def get_trade_history_df(cls):
        return pd.DataFrame(cls.trade_history)

    @classmethod
    def get_holdings_df(cls):
        return pd.DataFrame(cls.holdingsdf)

class Strat1VWAP(bt.Strategy):
    params = (
        ('period', 20),  # Parameter for VWAP period
        ('risk_percentage', 0.02),  # Risk per trade as a percentage of the portfolio
    )
    trade_history = []
    holdingsdf = []

    def __init__(self):
        self.vwap = MyVWAP(period=self.params.period)
        self.size = 0  # Initialize position size

    def next(self):
        if self.data.volume[0] > 0:
            if self.data.close[0] > self.vwap[0]:
                # Buy based on strategy conditions
                if self.size == 0:
                    self.size = self.broker.getvalue() * self.params.risk_percentage / self.vwap[0]
                    self.buy(size=self.size)
            else:
                # Sell based on strategy conditions
                if self.size > 0:
                    self.sell(size=self.size)
                    self.size = 0  # Reset position size after selling
    @classmethod
    def get_trade_history_df(cls):
        return pd.DataFrame(cls.trade_history)

    @classmethod
    def get_holdings_df(cls):
        return pd.DataFrame(cls.holdingsdf)

'''
'''
class Strat1RSI(bt.Strategy):
    Description = "This strategy class combines the Relative Strength Index (RSI) and the Volume Weighted Average Price (VWAP) to make trading decisions. It buys when RSI is oversold, and the price is above VWAP. It shorts when RSI is overbought, and the price is below VWAP. It also includes exit conditions based on RSI and VWAP."
    params = (
        ('rsi_period', 14),
        ('vwap_period', 20),  # VWAP period
        ('oversold_threshold', 30),
        ('overbought_threshold', 70),
    )

    trade_history = []
    holdingsdf = []

    def __init__(self):
        self.rsi = MyRSI(period=self.params.rsi_period)
        self.vwap = MyVWAP(period=self.params.vwap_period)

    def next(self):
        rsi_value = self.rsi[0]
        vwap_value = self.vwap[0]

        if rsi_value < self.params.oversold_threshold and self.data.close[0] < vwap_value:
            self.buy()  # Buy signal: RSI below oversold threshold and price below VWAP
        elif rsi_value > self.params.overbought_threshold and self.data.close[0] > vwap_value:
            self.sell()  # Sell signal: RSI above overbought threshold and price above VWAP

    @classmethod
    def get_trade_history_df(cls):
        return pd.DataFrame(cls.trade_history)

    @classmethod
    def get_holdings_df(cls):
        return pd.DataFrame(cls.holdingsdf)


class Strat1(bt.Strategy):
    params = (

    )
    trade_history = []
    holdingsdf = []

    def __init__(self):
        pass

    def next(self):
        pass
    @classmethod
    def get_trade_history_df(cls):
        return pd.DataFrame(cls.trade_history)

    @classmethod
    def get_holdings_df(cls):
        return pd.DataFrame(cls.holdingsdf)
    
