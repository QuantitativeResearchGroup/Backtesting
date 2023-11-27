import pandas as pd
import backtrader as bt

def enter_long_trade(self):
    self.in_trade = True
    self.entry_price = self.data.close[0]
    value = self.buy()
    self.__class__.trade_history.append({
        'Strategy': self.strategy_name,
        'Ticker': self.data._name,
        'Date': self.data.datetime.datetime(0),
        'Action': "Buy",
        'Price': self.data.close[0],
        'Quantity': value.size,
        'PnL': (self.data.close[0] - self.entry_price) * abs(self.position.size),
    })
    self.record_holding()
    store_trade(self, 'Buy', self.data.close[0])
    
    # Additional code
def enter_short_trade(self):
    self.in_trade = True
    self.entry_price = self.data.close[0]
    value = self.sell()
    self.record_holding()
    action = "Short" if self.position.size < 0 else "Cover"
    self.__class__.trade_history.append({
        'Strategy': self.strategy_name,
        'Ticker': self.data._name,
        'Date': self.data.datetime.datetime(0),
        'Action': action,
        'Price': self.data.close[0],
        'Quantity': value.size,
        'PnL': (self.data.close[0] - self.entry_price) * abs(self.position.size),
    })
    self.record_holding()
    store_trade(self, 'Sell', self.data.close[0])
    
def execute_after_close(self, action):
    pnl = (self.data.close[0] - self.entry_price) * abs(self.position.size)
    self.__class__.trade_history.append({
        'Strategy': self.strategy_name,
        'Ticker': self.data._name,
        'Date': self.data.datetime.datetime(0),
        'Action': action,
        'Price': self.data.close[0],
        'Quantity': -self.position.size,
        'PnL': pnl,
    })
    self.record_holding()
    
def exit_trade(self):
    self.in_trade = False
    self.close()  # Close the current position
    action = 'Sell' if self.position.size > 0 else 'Cover'
    pnl = (self.data.close[0] - self.entry_price) * abs(self.position.size)
    self.record_trade_exit(action, pnl)   
   


def record_trade_exit(self, action, pnl):
    ticker = self.data._name
    current_quantity = self.position.size
    current_price = self.data.close[0]

    if current_quantity != 0:
        if ticker in self.holdings:
            if action == 'Sell':
                self.holdings[ticker]['Quantity'] -= current_quantity
            elif action == 'Cover':
                self.holdings[ticker]['Quantity'] += current_quantity
        else:
            self.holdings[ticker] = {
                'Strategy': self.strategy_name,
                'Ticker': ticker,
                'Date': self.data.datetime.datetime(0),
                'Price': current_price,
                'Quantity': current_quantity,
            }
        self.__class__.holdingsdf.append({
            'Strategy': self.strategy_name,
            'Ticker': ticker,
            'Date': self.data.datetime.datetime(0),
            'Price': current_price,
            'Quantity': self.holdings[ticker]['Quantity']
        })

 
def store_trade(self, action, price):
    trade_info = {
        'Strategy': self.strategy_name,
        'Ticker': self.data._name,
        'Date': self.data.datetime.datetime(0),
        'Action': action,
        'Price': price,
        'Quantity': self.position.size,
    }
    self.__class__.trade_history.append(trade_info)

def record_holding(self):
    if self.position.size != 0:
        self.__class__.holdingsdf.append({
            'Strategy': self.strategy_name,
            'Ticker': self.data._name,
            'Date': self.data.datetime.datetime(0),
            'Price': self.data.close[0],
            'Quantity': self.position.size,
        })  
        
def get_trade_history_df(strategy_instance):
    return pd.DataFrame(strategy_instance.trade_history)

def get_holdings_df(strategy_instance):
    return pd.DataFrame(strategy_instance.holdingsdf)


