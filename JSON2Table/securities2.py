import psycopg2

# Establish a connection to the PostgreSQL database
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
    name VARCHAR(100) NOT NULL,
    security_type VARCHAR(50) NOT NULL,
    description TEXT
);
"""
cur.execute(create_securities_table_query)

securities_data = [
    {
        'name': 'Common Stock',
        'security_type': 'Stock',
        'description': 'Represents ownership in a corporation and typically entitles the holder to voting rights and dividends.',
    },
    {
        'name': 'Preferred Stock',
        'security_type': 'Stock',
        'description': 'A type of stock that has a higher claim on a company\'s assets and earnings than common stock but typically doesn\'t have voting rights.',
    },
    {
        'name': 'Bond',
        'security_type': 'Bond',
        'description': 'Debt securities issued by governments, municipalities, or corporations, promising periodic interest payments and the return of the principal at maturity.' },
    {
        'name': 'Exchange-Traded Funds',
        'security_type': 'ETF',
        'description': 'Investment funds that are traded on stock exchanges, offering diversified exposure to various assets or indices.'
    },
    {
        'name': 'Mutual Funds',
        'security_type': 'Mutual Funds',
        'description': 'Pooled investment vehicles that invest in a diversified portfolio of stocks, bonds, or other securities.'
    },
    {
        'name': 'Options',
        'security_type': 'Options',
        'description': 'Contracts that give the holder the right, but not the obligation, to buy (call option) or sell (put option) a specific underlying asset at a predetermined price.'
    },
    {
        'name': 'Futures',
        'security_type': 'Futures',
        'description': 'Contracts that obligate the buyer to purchase and the seller to sell a specific quantity of an underlying asset at a future date for a predetermined price.' 
    },
    {
        'name': 'Real Estate Investment Trusts',
        'security_type': 'REITs',
        'description': 'Companies that own or finance income-producing real estate, offering shares to investors.'    
    },
    {
        'name': 'Convertible Securities',
        'security_type': 'Convertible Securities',
        'description': 'Bonds or preferred stocks that can be converted into common stock at the option of the holder.'
    },
    {
        'name': 'Warrants',
        'security_type': 'Warrants',
        'description': 'A security that gives the holder the right to purchase other securities, typically common stock, at a specific price within a specific time frame.'
    },
    {
        'name': 'Commodities',
        'security_type': 'Commodities',
        'description': 'Physical goods like gold, oil, or agricultural products, which can be traded as securities through commodity futures contracts.'  
    },
    {
        'name': 'Crypto Assets',
        'security_type': 'Crypto Assets',
        'description': 'Digital or virtual currencies like Bitcoin and Ethereum, which are traded as cryptocurrencies.'
    }
]

for record in securities_data:
    insert_query = """
    INSERT INTO securities (name, security_type, description)
    VALUES (%s, %s, %s);
    """
    cur.execute(insert_query, (
        record['name'],
        record['security_type'],
        record['description'],
    ))

conn.commit()
cur.close()
conn.close()
