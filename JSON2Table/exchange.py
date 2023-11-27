import psycopg2
import json
# url = https://www.iso20022.org/market-identifier-codes

conn = psycopg2.connect(
    dbname='MyDatabase',
    user='postgres',
    password='bobwashere',
    host='localhost',
    port=5432  
)
cur = conn.cursor()
create_exchange_table_query = """
CREATE TABLE IF NOT EXISTS exchange (
    MIC SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50),
    timezone VARCHAR(50),
    open_time TIMESTAMPTZ
);
"""
cur.execute(create_exchange_table_query)

with open('exchange_data.json', 'r') as f:
    for line in f:
        record = json.loads(line)  
        insert_query = """
        INSERT INTO exchange (MIC, name, country, city, timezone, open_time)
        VALUES (%s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, (
            record['MIC'],
            record['name'],
            record['country'],
            record['city'],
            record['timezone'],
            record['opentime']
        ))

conn.commit()
cur.close()
conn.close()

