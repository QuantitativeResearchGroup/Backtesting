import psycopg2
# import json

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(
    dbname='MyDatabase',
    user='postgres',
    password='bobwashere',
    host='localhost',
    port=5432  # Port should be an integer, not a string
)

# Create a cursor to execute SQL queries
cur = conn.cursor()

# Create the table if it doesn't exist
create_table_query = """
CREATE TABLE IF NOT EXISTS dummy (
    Ticker VARCHAR(255) PRIMARY KEY,
    StockExchange VARCHAR(255),
    Name VARCHAR(255),
    Industry VARCHAR(255),
    Sector VARCHAR(255),
    LongDescription TEXT,
    Website VARCHAR(255),
    "52WeekHigh" NUMERIC,
    "52WeekLow" NUMERIC,
    Volume BIGINT
);
"""
cur.execute(create_table_query)

# Load data from a JSON file into the table
with open('sp500_data.json', 'r') as f:
    for line in f:
        record = json.loads(line)  # Load one JSON object at a time
        insert_query = """
        INSERT INTO dummy (Ticker, StockExchange, Name, Industry, Sector, LongDescription, Website, "52WeekHigh", "52WeekLow", Volume)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, (
            record['Ticker'],
            record['StockExchange'],
            record['Name'],
            record['Industry'],
            record['Sector'],
            record['LongDescription'],
            record['Website'],
            record['52WeekHigh'],
            record['52WeekLow'],
            record['Volume']
        ))

# Commit the changes to the database
conn.commit()

# Close the cursor and the connection
cur.close()
conn.close()
