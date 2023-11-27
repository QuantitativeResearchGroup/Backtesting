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
    MIC VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    country VARCHAR(50) NOT NULL,
    city VARCHAR(50),
    timezone VARCHAR(50),
    open_time TIMESTAMPTZ
);
"""
cur.execute(create_exchange_table_query)

exchange_data = [
    {
        "MIC": "XNYS",
        "name": "New York Stock Exchange",
        "country": "United States",
        "city": "New York",
        "timezone": "Eastern Time (ET)",
        "opentime": "2023-01-01 09:30:00-05:00" # daylight
    },
    {
        "MIC": "XNAS",
        "name": "Nasdaq Stock Market",
        "country": "United States",
        "city": "New York",
        "timezone": "Eastern Time (ET)",
        "opentime": "2023-01-01 09:30:00-05:00"
    },
    {
        "MIC": "XLON",
        "name": "London Stock Exchange",
        "country": "United Kingdom",
        "city": "London",
        "timezone": "Greenwich Mean Time (GMT)",
        "opentime": "2023-01-01 08:00:00+00:00"
    },
    {
        "MIC": "XTKS",
        "name": "Tokyo Stock Exchange",
        "country": "Japan",
        "city": "Tokyo",
        "timezone": "Japan Standard Time (JST)",
        "opentime": "2023-01-01 09:00:00+09:00"
    },  
    {
        "MIC": "XHKG",
        "name": "Hong Kong Exchanges and Clearing",
        "city": "Hong Kong ",
        "country": "China",
        "timezone": "Hong Kong Time (HKT)",
        "opentime": "2023-01-01 09:30:00+08:00"
    },  
    {
        "MIC": "XAMS",
        "name": "Euronext Amsterdam",
        "country": "Netherlands",
        "city": "Amsterdam",
        "timezone": "Central European Time (CET)",
        "opentime": "2023-01-01 09:00:00+01:00"
    },  
    {
        "MIC": "XSHE",
        "name": "Shanghai Stock Exchange",
        "city": "Shanghai",
        "country": "China",
        "timezone": "China Standard Time (CST)",
        "opentime": "2023-01-01 09:30:00+08:00"
    },  
    {
        "MIC": "XTSE",
        "name": "Toronto Stock Exchange",
        "city": "Toronto",
        "country": "Canada",
        "timezone": "Eastern Time (ET)",
        "opentime": "2023-01-01 09:30:00-04:00"
    },  
    {
        "MIC": "XETR",
        "name": "Frankfurt Stock Exchange",
        "city": "Frankfurt",
        "country": "Germany",
        "timezone": "Central European Time (CET)",
        "opentime": "2023-01-01 08:00:00+01:00"
    },  
    {
        "MIC": "XBOM",
        "name": "Bombay Stock Exchange",
        "city": "Mumbai",
        "country": "India",
        "timezone": "Indian Standard Time (IST)",
        "opentime": "2023-01-01 09:15:00+05:30"
    }
]

for record in exchange_data:
    insert_query = """
    INSERT INTO exchange (MIC, name, country, city, timezone, open_time)
    VALUES (%s, %s, %s,%s, %s, %s);
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


            
        


