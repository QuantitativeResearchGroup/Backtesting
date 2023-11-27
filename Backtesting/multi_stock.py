import datetime as dt
import backtrader as bt
import backtrader.analyzers as btanalyzers
import yfinance as yf
import pandas as pd
import quantstats as qs  # Import quantstats
import webbrowser as web
from strategies import *
from Methods import *
from dateutil.relativedelta import relativedelta
import numpy as np
import os


def ma_cross_strategy(ticker, slow=200, fast=50, end=None, period=3):
    if not end:
        end = dt.date.today()
    start = end - relativedelta(years=period)

    data = pd.DataFrame(yf.download(ticker, start=start, end=end)["Close"])
    data[f'{fast}-day'] = data.Close.rolling(fast).mean()
    data[f'{slow}-day'] = data.Close.rolling(slow).mean()
    data['returns'] = np.log(data.Close).diff()
    data['strategy'] = np.where(data[f'{fast}-day'] > data[f'{slow}-day'], 1, 0)
    data['strategy'] = np.where(data[f'{fast}-day'] < data[f'{slow}-day'], -1, data['strategy'])
    strategy = data['returns'] * data['strategy']
    return strategy

    
if __name__ == "__main__":
    connection = establish_database_connection()
    if connection is not None:    
        #portfolio = ["QSR", "SHOP", "F"]  # List of tickers to process
        portfolio = ["A"]
        strategy_class = Strat0TEST
        dataframes = []  
        cash = 100000.0
        start_date = "2020-01-21"
        end_date = "2020-02-03"
        exclude_list = [
                'warn', 'treynor_ratio', 'to_drawdown_series', 'ror',
                'rolling_volatility', 'rolling_sortino', 'rolling_sharpe', 'rolling_greeks',
                'remove_outliers', 'r_squared', 'r2', 'pct_rank',
                'outliers', 'omega', 'monthly_returns', 'information_ratio',
                'implied_volatility', 'greeks', 'drawdown_details', 'distribution', 'compsum', 'compare', '_norm', '_linregress', '_ceil'
            ]

        # variable of the strategy : potflioname, cash, startdate, enddate, 

        for ticker in portfolio:
            data = yf.download(ticker, start=start_date, end= end_date)
            data = bt.feeds.PandasData(dataname=data)
            cerebro = bt.Cerebro()
            cerebro.adddata(data, name=ticker)
            cerebro.addstrategy(strategy_class)
            cerebro.broker.setcash(cash)
            cerebro.addsizer(bt.sizers.PercentSizer, percents=10)

            print(f'Starting Portfolio Value for {ticker}: %.2f' % cerebro.broker.getvalue())
            back = cerebro.run()
            final =cerebro.broker.getvalue()
            print(f'Final Portfolio Value for {ticker}: %.2f' % final)

            conn = establish_database_connection()  # Establish a database connection
            cur = conn.cursor()  # Create a database cursor
            qs.extend_pandas()

            # strategy
            A_cross = ma_cross_strategy(ticker, slow=21, fast=9, period=3)
            A_cross.index = A_cross.index.tz_localize(None)
            gld = qs.utils.download_returns(ticker)
            #gld.index = gld.index.tz_localize(None)
            stock = gld
            results_df = pd.DataFrame(columns=["Function", "Result"])
            
            for item in dir(qs.stats):
                if item in exclude_list:
                    continue  
                if callable(getattr(qs.stats, item)):
                    function = getattr(qs.stats, item)  # Get the function
                    try:
                        result = function(stock)  # Call the function with your stock data
                        results_df[item] = [result]  # Add a new column with the result
                        print(f"Function: {item}")
                        print("Result:", result)
                    except Exception as e:
                        pass
                        print(f"Function: {item}")
                        print(f"Error: {str(e)}")
                else:
                    pass

            print(results_df.drop(['Function', 'Result'], axis=1))
            update_or_insert_strategy_summary(cur, str(strategy_class), cash, start_date, end_date, int(final))
            update_or_insert_strategy_summary_LONG(cur, class_name=str(strategy_class.__name__), cash_used=str(cash), start_date=start_date, end_date=end_date, final_value=str(final),adjusted_sortino= str(results_df.loc[0, 'adjusted_sortino']), autocorr_penalty= str(results_df.loc[0, 'autocorr_penalty']),avg_loss= str(results_df.loc[0, 'avg_loss']), avg_return= str(results_df.loc[0, 'avg_return']), avg_win= str(results_df.loc[0, 'avg_win']), best= str(results_df.loc[0, 'best']), cagr= str(results_df.loc[0, 'cagr']), calmar=str(results_df.loc[0, 'calmar']), common_sense_ratio=str(results_df.loc[0, 'common_sense_ratio']), comp=str(results_df.loc[0, 'comp']), conditional_value_at_risk=str(results_df.loc[0, 'conditional_value_at_risk']), consecutive_losses=str(results_df.loc[0, 'consecutive_losses']), consecutive_wins=str(results_df.loc[0, 'consecutive_wins']), cpc_index=str(results_df.loc[0, 'cpc_index']), cvar=str(results_df.loc[0, 'cvar']), expected_return= str(results_df.loc[0, 'expected_return']), expected_shortfall=str(results_df.loc[0, 'expected_shortfall']), exposure=str(results_df.loc[0, 'exposure']), gain_to_pain_ratio=str(results_df.loc[0, 'gain_to_pain_ratio']), geometric_mean=str(results_df.loc[0, 'geometric_mean']), ghpr=str(results_df.loc[0, 'ghpr']), kelly_criterion=str(results_df.loc[0, 'kelly_criterion']), kurtosis=str(results_df.loc[0, 'kurtosis']), max_drawdown=str(results_df.loc[0, 'max_drawdown']), outlier_loss_ratio=str(results_df.loc[0, 'outlier_loss_ratio']), outlier_win_ratio=str(results_df.loc[0, 'outlier_win_ratio']), payoff_ratio=str(results_df.loc[0, 'payoff_ratio']), probabilistic_adjusted_sortino_ratio=str(results_df.loc[0, 'probabilistic_adjusted_sortino_ratio']), probabilistic_ratio=str(results_df.loc[0, 'probabilistic_ratio']), probabilistic_sharpe_ratio=str(results_df.loc[0, 'probabilistic_sharpe_ratio']), probabilistic_sortino_ratio=str(results_df.loc[0, 'probabilistic_sortino_ratio']), profit_factor=str(results_df.loc[0, 'profit_factor']), profit_ratio=str(results_df.loc[0, 'profit_ratio']), rar=str(results_df.loc[0, 'rar']), recovery_factor=str(results_df.loc[0, 'recovery_factor']), risk_of_ruin=str(results_df.loc[0, 'risk_of_ruin']), risk_return_ratio=str(results_df.loc[0, 'risk_return_ratio']), serenity_index=str(results_df.loc[0, 'serenity_index']), sharpe= str(results_df.loc[0, 'sharpe']), skew=str(results_df.loc[0, 'skew']), smart_sharpe=str(results_df.loc[0, 'smart_sharpe']), smart_sortino=str(results_df.loc[0, 'smart_sortino']), sortino=str(results_df.loc[0, 'sortino']), tail_ratio=str(results_df.loc[0, 'tail_ratio']), ulcer_index=str(results_df.loc[0, 'ulcer_index']), ulcer_performance_index=str(results_df.loc[0, 'ulcer_performance_index']), upi=str(results_df.loc[0, 'upi']), value_at_risk=str(results_df.loc[0, 'value_at_risk']), var=str(results_df.loc[0, 'var']), volatility=str(results_df.loc[0, 'volatility']), win_loss_ratio=str(results_df.loc[0, 'win_loss_ratio']), win_rate=str(results_df.loc[0, 'win_rate']), worst= str(results_df.loc[0, 'worst']))

            tradelogdf = strategy_class.get_trade_history_df()
            holdings = strategy_class.get_holdings_df()

            if not tradelogdf.empty:  # Trade log
                for _, row in tradelogdf.iterrows():
                    update_or_insert_tradelog_data(cur, ticker, row)
                conn.commit()

            if not holdings.empty:  # Holdings
                for _, row in holdings.iterrows():
                    update_or_insert_holding_data(cur, ticker, row)
                conn.commit()

            dataframes.append((ticker, tradelogdf, holdings))  # Store dataframes for this ticker
            cur.close()

            report=qs.reports.html(A_cross, gld, output=f"output/{ticker}_cross.html", download_filename=f"output/{ticker}_cross.html")
            web=web.open_new(f"file:///{os.getcwd()}/output/{ticker}_cross.html")
            #print(f"web for {web}:")   

        # tradelogdf = tradelogdf.sort_values(by='Date', ascending=True)
        # for ticker, tradelogdf, holdings in dataframes:
        #     print(f"Trade Log for {ticker}:")
        #     print(tradelogdf)
        #     print(f"Holdings for {ticker}:")
        #     print(holdings)
    connection.close()