# VWAP
from General import *

class StratVWAP(bt.Strategy):
    params = (
        ('vwap_period', 20),  # Period for VWAP calculation
        ('stop_loss_ratio', 2.0),
    )
    trade_history = []
    holdings = {}
    holdingsdf = []

    def __init__(self):
        self.strategy_name = self.__class__.__name__
        self.vwap = bt.indicators.VWAP(self.data, period=self.params.vwap_period)
        self.in_trade = False
        self.entry_price = 0.0

    def next(self):
        if not self.in_trade:
            if self.data.close[0] > self.vwap[0]:
                self.enter_long_trade()
            elif self.data.close[0] < self.vwap[0]:
                self.enter_short_trade()
        elif self.in_trade:
            if self.data.close[0] < self.vwap[0] or self.data.close[0] <= (1 - self.params.stop_loss_ratio) * self.entry_price:
                self.exit_trade()
