from example.indicator import *
import pandas as pd
class Strat5VWAPRSI(bt.Strategy):
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