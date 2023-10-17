import backtrader as bt
import backtrader.analyzers as btanalyzers
import pandas as pd
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from datetime import datetime

stocks = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
stock = yf.Ticker(stocks[1])
stock.history(period="1y")['High'][0]
stock.history(period="1y")['Close'][0]

# General Info via yahoo finance website
data = []
officer_dataframes = []
news_dataframes = []


for symbol in stocks:
    stock = yf.Ticker(symbol)
    stock_info = stock.info
    url = f'https://finance.yahoo.com/quote/{symbol}?p={symbol}&.tsrc=fin-srch'
    response = requests.get(url)
    if response.status_code == 200:
        
        if 'companyOfficers' in stock_info:
            officers_data = []
            for i in range(len(stock_info['companyOfficers'])):
                officers_data.append({
                    'Name': stock_info['companyOfficers'][i]['name'],
                    'Title': stock_info['companyOfficers'][i]['title']
                })
            officers_df = pd.DataFrame(officers_data)
            officer_dataframes.append(officers_df)

        stock_info = {
            'ticker': symbol,
            'website': stock_info["website"],
            'industry': stock_info["industry"],
            'sector': stock_info["sector"],
            'longBusinessSummary': stock_info["longBusinessSummary"],
        }
        data.append({
            'Ticker': stock_info['ticker'],
            'Industry': stock_info['industry'],
            'Sector': stock_info["sector"],
            'Website': stock_info['website'],
            'Description': stock_info['longBusinessSummary'],
        })    
info_df = pd.DataFrame(data)
print(info_df)
officer_dict = {symbol: df for symbol, df in zip(stocks, officer_dataframes)}
for symbol, officer_df in officer_dict.items():
    print(f"Company: {symbol}")
    print(officer_df)

