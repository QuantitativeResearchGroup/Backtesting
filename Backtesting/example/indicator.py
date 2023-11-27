import backtrader as bt
# SMA


class MySimpleMovingAverage(bt.Indicator):
    params = (('period', 20),)
    alias = ('sma', 'MySimpleMovingAverage',)
    lines = ('sma',)

    def __init__(self):
        self.addminperiod(self.params.period)
        self.data_sma = bt.LineBuffer()  # LineBuffer to track SMA values

    def next(self):
        if len(self) >= self.params.period:
            sma_val = sum(self.data.get(size=self.params.period)) / self.params.period
            self.lines.sma[0] = sma_val

# EMA
class MyExponentialMovingAverage(bt.Indicator):
    params = (('period', 20),)
    alias = ('ema', 'MyExponentialMovingAverage',)
    lines = ('ema',)

    def __init__(self):
        self.addminperiod(self.params.period)
        self.alpha = 2 / (self.params.period + 1)
        self.data_ema = bt.LineBuffer()  # LineBuffer to track EMA values

    def next(self):
        if len(self) == 1:
            self.data_ema[0] = self.data[0]
            self.lines.ema[0] = self.data_ema[0]
        elif len(self) > 1:
            ema_val = self.alpha * self.data[0] + (1 - self.alpha) * self.data_ema[-1]
            self.lines.ema[0] = self.data_ema[0] = ema_val

class MyVWAP(bt.Indicator):
    params = (('period', 20), )
    alias = ('vwap', 'MyVWAP',)
    lines = ('vwap',)

    def __init__(self):
        self.cumulative_price_volume = 0.0
        self.cumulative_volume = 0.0

    def next(self):
        typical_price = (self.data.high + self.data.low + self.data.close) / 3
        price_volume = typical_price * self.data.volume
        self.cumulative_price_volume += price_volume
        self.cumulative_volume += self.data.volume

        if self.cumulative_volume != 0:
            vwap_val = self.cumulative_price_volume / self.cumulative_volume
            self.lines.vwap[0] = vwap_val
            
# bollinger bands
class BollingerBands(bt.Indicator):
    lines = ('bb_upper', 'bb_middle', 'bb_lower',)  # Define lines for upper, middle, and lower bands
    params = (('period', 20), ('devfactor', 2.0),)  # Define default period and deviation factor

    def __init__(self):
        self.lines.bb_middle = MySimpleMovingAverage(self.data, period=self.params.period)
        std = self.params.devfactor * bt.ind.StdDev(self.data, period=self.params.period)
        self.lines.bb_upper = self.lines.bb_middle+std
        self.lines.bb_lower = self.lines.bb_middle-std

# RSI
class MyRSI(bt.Indicator):
    lines = ('rsi',)

    params = (
        ('period', 14),
    )

    def __init__(self):
        self.data_close = self.data.close
        self.diff = self.data_close - self.data_close(-1)
        self.up = bt.indicators.SumN(self.diff * (self.diff > 0), period=self.p.period)
        self.down = -bt.indicators.SumN(self.diff * (self.diff < 0), period=self.p.period)
        self.rs = self.up / (self.up + self.down)
        self.lines.rsi = 100 - 100 / (1 + self.rs)



class MovingAverageDifference(bt.Indicator):
    lines = ('madiff',)  # Name of the line for the indicator
    params = (
        ('period1', 20),  # 50 Period for the first moving average
        ('period2', 50),  # 200 Period for the second moving average
    )

    def __init__(self, period1=20, period2=50):
        self.data_ma1 = MySimpleMovingAverage(self.data, period=period1)
        self.data_ma2 = MySimpleMovingAverage(self.data, period=period2)

    def next(self):
        if len(self) >= max(self.p.period1, self.p.period2):
            ma1_val = self.data_ma1[0]  # Get the value of the first moving average
            ma2_val = self.data_ma2[0]  # Get the value of the second moving average
            self.lines.madiff[0] = ma1_val - ma2_val  # Compute the moving average difference
    

# ROC
class RateOfChange(bt.Indicator):
    lines = ('roc',)  # Name of the line for the indicator
    params = (('period', 14), )

    def __init__(self):
        self.roc = (self.data - self.data(-self.params.period)) / self.data(-self.params.period) * 100
        self.lines.roc = self.roc

#MACD

class MyMACD(bt.Indicator):
    params = (('fast_period', 12), ('slow_period', 26), ('signal_period', 9))
    alias = ('MyMACD',)

    lines = ('macd', 'signal', 'histogram')

    def __init__(self):
        self.fast_ema = MyExponentialMovingAverage(period=self.params.fast_period)
        self.slow_ema = MyExponentialMovingAverage(period=self.params.slow_period)
        self.signal_ema = MyExponentialMovingAverage(period=self.params.signal_period)

    def next(self):
        fast_ema_val = self.fast_ema[0]
        slow_ema_val = self.slow_ema[0]

        if fast_ema_val is None or slow_ema_val is None:
            return

        self.lines.macd[0] = fast_ema_val - slow_ema_val

        if len(self) >= self.params.signal_period:
            signal_val = self.signal_ema(self.lines.macd[0])
            self.lines.signal[0] = signal_val
            self.lines.histogram[0] = self.lines.macd[0] - signal_val




'''
'''
def record_holding(strategy):
    if strategy.position.size != 0:
        strategy.__class__.holdingsdf.append({
            'Strategy': strategy.strategy_name,
            'Ticker': strategy.data._name,
            'Date': strategy.data.datetime.datetime(0),
            'Price': strategy.data.close[0],
            'Quantity': strategy.position.size,
        })
'''
'''       
def enter_long_trade(strategy):
    strategy.in_trade = True
    strategy.entry_price = strategy.data.close[0]
    value = strategy.buy()
    store_trade(strategy, "Buy", strategy.data.close[0])
    record_holding(strategy)
'''
'''
def enter_short_trade(strategy):
    strategy.in_trade = True
    strategy.entry_price = strategy.data.close[0]
    value = strategy.sell()
    store_trade(strategy, "Short" if strategy.position.size < 0 else "Short Cover", strategy.data.close[0])
    record_holding(strategy)
'''
'''
def store_trade(strategy, action, price):
    date = strategy.data.datetime.datetime(0)
    ticker = strategy.data._name
    quantity = strategy.position.size
    trade_info = {
        'Strategy': strategy.__class__.__name__,
        'Ticker': ticker,
        'Date': date,
        'Action': action,
        'Price': price,
        'Quantity': quantity,
    }
    strategy.__class__.trade_history.append(trade_info)
    