from General import *

class TrendIdentificationStrategy(bt.Strategy):
    params = (
        ('rsi_period', 14),         # Period for RSI calculation
        ('vwap_period', 20),        # Period for VWAP calculation
        ('bb_period', 20),          # Period for Bollinger Bands calculation
        ('bb_devfactor', 2),        # Deviation factor for Bollinger Bands
        ('stochastic_period', 14),  # Period for Stochastic calculation
        ('stochastic_slow_period', 3),  # Period for Stochastic slow
        ('stop_loss_ratio', 2.0),
    )
    trade_history = []
    holdings = {}
    holdingsdf = []

    def __init__(self):
        self.strategy_name = self.__class__.__name__
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
        self.vwap = bt.indicators.VWAP(self.data, period=self.params.vwap_period)
        self.bollinger = bt.indicators.BollingerBands(self.data.close, period=self.params.bb_period, devfactor=self.params.bb_devfactor)
        self.stochastic = bt.indicators.Stochastic(self.data, period=self.params.stochastic_period, period_dfast=self.params.stochastic_slow_period)
        self.in_trade = False
        self.entry_price = 0.0

    def next(self):
        rsi_val = self.rsi[0]
        vwap_val = self.vwap[0]
        bb_upper = self.bollinger.lines.top[0]
        bb_lower = self.bollinger.lines.bot[0]
        stochastic_k = self.stochastic.lines.percK[0]
        stochastic_d = self.stochastic.lines.percD[0]

        if not self.in_trade:
            if rsi_val > 70 and self.data.close[0] > vwap_val and self.data.close[0] > bb_upper and stochastic_k > stochastic_d:
                self.enter_short_trade()
                print("Trend: Short")
            elif rsi_val < 30 and self.data.close[0] < vwap_val and self.data.close[0] < bb_lower and stochastic_k < stochastic_d:
                self.enter_long_trade()
                print("Trend: Long")

        elif self.in_trade:
            if self.data.close[0] > vwap_val and self.data.close[0] > bb_upper and stochastic_k > stochastic_d:
                self.exit_trade()
                print("Exit Trend: Short")
            elif self.data.close[0] < vwap_val and self.data.close[0] < bb_lower and stochastic_k < stochastic_d:
                self.exit_trade()
                print("Exit Trend: Long")


