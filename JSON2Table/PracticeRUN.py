import psycopg2
import pandas as pd
from datetime import datetime
from Methods import *
conn = establish_database_connection()
cur = conn.cursor()

create = []  # list of 4 methods to make table
create_general_table_if_not_exists(cur)
get_tickers_query = "SELECT symbol FROM sp500wiki;"
cur.execute(get_tickers_query)
tickers = [record[0] for record in cur.fetchall()]

Update_or_Insert = [] # list of 4 methods

for ticker in tickers:
    a, b, c, d = pulldata([ticker])
    alpha = [a,b,c,d]  #  list of 4 databases
    
    a_Dictionary = a.to_dict()
    #print(type(A_Dictionary))
    if not a.empty:
        update_or_insert_general_data(cur, ticker, a_Dictionary)

conn.commit()
cur.close()
conn.close()
