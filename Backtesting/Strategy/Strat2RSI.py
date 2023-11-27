from General import *

class StratRSI(bt.Strategy):
    params = (
        ('rsi_period', 14),       # Period for RSI calculation
        ('rsi_upper', 70),        # RSI upper threshold for selling
        ('rsi_lower', 30),        # RSI lower threshold for buying
        ('stop_loss_ratio', 2.0),
    )
    trade_history = []
    holdings = {}
    holdingsdf = []

    def __init__(self):
        self.strategy_name = self.__class__.__name__
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.in_trade = False
        self.entry_price = 0.0

    def next(self):
        if not self.in_trade:
            if self.rsi[0] < self.params.rsi_lower:
                self.enter_long_trade()
            elif self.rsi[0] > self.params.rsi_upper:
                self.enter_short_trade()
        elif self.in_trade:
            if self.rsi[0] > self.params.rsi_upper or self.rsi[0] < self.params.rsi_lower \
                    or self.data.close[0] <= (1 - self.params.stop_loss_ratio) * self.entry_price:
                self.exit_trade()
