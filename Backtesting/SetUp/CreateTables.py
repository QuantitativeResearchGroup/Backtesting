# from methodsNEW import *
from Methods import *
conn = establish_database_connection()
cur = conn.cursor()

get_tickers_query = "SELECT symbol FROM sp500wiki;"
cur.execute(get_tickers_query)
tickers = [record[0] for record in cur.fetchall()]
tickers = tickers[0:4]  # limited for testing

# Create SQL Tables
create_yf_income_statement_table_if_not_exists(cur)
create_yf_balance_sheet_table_if_not_exists(cur)
create_yf_cash_flow_table_if_not_exists(cur)
create_daily_price_data(cur)
create_intraday_price_data(cur)
create_general_stock_data(cur)
create_tradelog_if_not_exists(cur)
create_holding_if_not_exists(cur)
create_performance_if_not_exists(cur)

# Annual Tables

conn.commit()
cur.close()
conn.close()