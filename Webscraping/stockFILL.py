import yfinance as yf
import pandas as pd
# Suppress pandas warnings
pd.options.mode.chained_assignment = None

# Get the list of S&P 500 tickers
url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
table = pd.read_html(url)[0]
tickers = table['Symbol'].str.replace('.', '-').to_list()

data_frames = []

# Iterate through the tickers
for ticker in tickers:
    try:
        # Download the ticker's data
        ticker_data = yf.Ticker(ticker)

        # Get the historical data to calculate 52-week high and low
        history = ticker_data.history(period="1y")
        high_52w = history['High'].max()
        low_52w = history['Low'].min()

        # Get other information from info property
        info = ticker_data.info

        # Create a DataFrame for the ticker's information
        ticker_info = pd.DataFrame({
            'Ticker': [ticker],
            'StockExchange': [info.get('exchange', None)],  # Add Stock Exchange Info
            'Name': [info.get('longName', None)],
            'Industry': [info.get('industry', None)],
            'Sector': [info.get('sector', None)],
            'LongDescription': [info.get('longBusinessSummary', None)],
            'Website': [info.get('website', None)],
            '52WeekHigh': [high_52w],
            '52WeekLow': [low_52w],
            'Volume': [info.get('averageVolume10days', None)]
        })

        # Append the DataFrame to the list
        data_frames.append(ticker_info)
        print(ticker)
    except Exception as e:
        print(f"Error retrieving data for {ticker}: {str(e)}")

# Concatenate the list of DataFrames into one DataFrame
data = pd.concat(data_frames, ignore_index=True)

# Print the DataFrame
print(data)

# Save the DataFrame to a CSV file
#data.to_csv('sp500_data.csv', index=False)
# Save the DataFrame to a JSON file
data.to_json('sp500_data.json', orient='records', lines=True)
