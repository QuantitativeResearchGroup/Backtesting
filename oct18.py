import yfinance as yf
import pandas as pd 
import matplotlib.pyplot as plt
pd.options.mode.chained_assignment = None


tickers = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]

tickers = tickers.Symbol.to_list()

tickers = [i.replace('.','-') for i in tickers]
#print(tickers)

# rsi cacluclation and retursn dataframe
def RSIcalc(asset):
    df = yf.download(asset, start ="2018-01-01")
    df['MA200'] = df['Adj Close'].rolling(window=200).mean()
    df['Price Change'] = df['Adj Close'].pct_change()
    df['UpMove'] = df['Price Change'].apply(lambda x:x if x>0 else 0)
    df['DownMove'] = df['Price Change'].apply(lambda x: abs(x) if x<0 else 0)
    df['Avg Up'] = df['UpMove'].ewm(span=19).mean()
    df['Avg Down'] = df['DownMove'].ewm(span=19).mean()
    df = df.dropna()
    
    df['RS'] = df['Avg Up'] / df['Avg Down']
    df['RSI'] = df['RS'].apply(lambda x: 100 - (100 / (x + 1)))
    df['Buy'] = 'Empty'
    df.loc[(df['Adj Close'] > df['MA200']) & (df['RSI'] < 30), 'Buy'] = 'Yes'
    df.loc[(df['Adj Close'] < df['MA200']) | (df['RSI'] > 70), 'Buy'] = 'No'
    return df

def getSignals(df):
    Buying_dates =[]
    Selling_dates = []
    for i in range(len(df)-11):
        if 'Yes' in df['Buy'].iloc[i]:
            Buying_dates.append(df.iloc[i+1].name)
            for j in range(1,11):
                if df['RSI'].iloc[i + j] >40:
                    Selling_dates.append(df.iloc[i+j+1].name)
                    break
                elif j == 10:
                    Selling_dates.append(df.iloc[i+j+1].name)
    return(Buying_dates,Selling_dates)
                
            
    
frame=RSIcalc(tickers[2])
#print(frame)
buy, sell =getSignals(frame) 
#print(buy)

plt.figure(figsize=(12,5))
plt.scatter(frame.loc[buy].index,frame.loc[buy]['Adj Close'], marker = '^', c='g' )
plt.plot(frame['Adj Close'], alpha=0.7)
#plt.show()

Profits = (frame.loc[sell].Open.values - frame.loc[buy].Open.values)/frame.loc[buy].Open.values
#print(Profits)

wins = [i for i in Profits if i > 0]
#print(len(wins)/len(Profits))
#print(len(Profits))

matrixsignals =[]
matrixprofits = []

for i in range(len(tickers)-480):
    frame=RSIcalc(tickers[i])
    buy, sell =getSignals(frame) 
    Profits = (frame.loc[sell].Open.values - frame.loc[buy].Open.values)/frame.loc[buy].Open.values
    matrixsignals.append(buy)
    matrixprofits.append(Profits)
    
#len(matrixprofits)

allprofits = []
for i in matrixprofits:
    for e in i:
        allprofits.append(e)

wins = [ i for i in allprofits if i>0]
print(len(wins)/len(allprofits))

plt.hist(allprofits, bins=100)
plt.show()
