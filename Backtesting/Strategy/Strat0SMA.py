
from Strategy.General import *
from example.indicator import *

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

# class Strat0SMA(bt.Strategy):
#     params = (
#         ('sma_period_short', 20),  # Shorter SMA period
#         ('sma_period_long', 50),   # Longer SMA period
#         ('ema_period', 30),        # EMA period
#         ('stop_loss_ratio', 2.0),
#     )
#     trade_history = []
#     holdings = {}
#     holdingsdf = []

#     def __init__(self):
#         self.strategy_name = self.__class__.__name__
#         self.sma_short = bt.indicators.SimpleMovingAverage(self.data, period=self.params.sma_period_short)
#         self.sma_long = bt.indicators.SimpleMovingAverage(self.data, period=self.params.sma_period_long)
#         self.ema = bt.indicators.ExponentialMovingAverage(self.data, period=self.params.ema_period)
#         self.in_trade = False
#         self.entry_price = 0.0

#     def next(self):
#         if not self.in_trade:
#             if self.sma_short[0] > self.sma_long[0] and self.data.close[0] > self.ema[0]:
#                 print("1")
#                 self.enter_long_trade()
#             elif self.sma_short[0] < self.sma_long[0] and self.data.close[0] < self.ema[0]:
#                 print("2")
#                 self.enter_short_trade()
#         elif self.in_trade:
#             if self.data.close[0] < self.sma_long[0] or self.data.close[0] <= (1 - self.params.stop_loss_ratio) * self.entry_price:
#                 self.exit_trade()
                
                
                

# class Strat1SMAEMA(bt.Strategy):
#     params = (
#         ('sma_period_short', 20),  # Shorter SMA period
#         ('sma_period_long', 50),   # Longer SMA period
#         ('ema_period', 30),        # EMA period
#         ('stop_loss_ratio', 2.0),
#     )
#     trade_history = []
#     holdings = {}
#     holdingsdf = []

#     def __init__(self):
#         self.strategy_name = self.__class__.__name__
#         self.sma_short = SimpleMovingAverage(period=self.params.sma_period_short)
#         self.sma_long = SimpleMovingAverage(period=self.params.sma_period_long)
#         self.ema = ExponentialMovingAverage(period=self.params.ema_period)
#         self.in_trade = False
#         self.entry_price = 0.0

#     def next(self):
#         if not self.in_trade:
#             if self.sma_short[0] > self.sma_long[0] and self.data.close[0] > self.ema[0]:
#                 self.enter_long_trade()
#             elif self.sma_short[0] < self.sma_long[0] and self.data.close[0] < self.ema[0]:
#                 self.enter_short_trade()
#         elif self.in_trade:
#             if self.data.close[0] < self.sma_long[0] or self.data.close[0] <= (1 - self.params.stop_loss_ratio) * self.entry_price:
#                 self.exit_trade()

                