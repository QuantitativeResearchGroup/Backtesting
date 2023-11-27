import psycopg2
import json

conn = psycopg2.connect(
    dbname='MyDatabase',
    user='postgres',
    password='bobwashere',
    host='localhost',
    port=5432  
)

cur = conn.cursor()

create_securities_table_query = """
CREATE TABLE IF NOT EXISTS securities (
    security_id SERIAL PRIMARY KEY,
    symbol VARCHAR(10) NOT NULL,
    name VARCHAR(100) NOT NULL,
    security_type VARCHAR(50) NOT NULL,
    sector VARCHAR(50) NOT NULL,
    description TEXT,
    listing_exchange_id INT REFERENCES exchanges(exchange_id),
    issuance_date DATE,
    market_cap NUMERIC(15, 2)
);

"""
cur.execute(create_securities_table_query)

with open('securities_data.json', 'r') as f:
    for line in f:
        record = json.loads(line)  
        insert_query = """
        INSERT INTO securities (security_id, symbol, name, security_type, sector, description, listing_exchange_id, issuance_date, market_cap)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, (
            record['security_id'],
            record['symbol'],
            record['name'],
            record['security_type'],
            record['sector'],
            record['description'],
            record['listing_exchange_id'],
            record['issuance_date'],
            record['market_cap']
        ))

conn.commit()
cur.close()
conn.close()
