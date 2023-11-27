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

create_companyholding_table_query = """
CREATE TABLE IF NOT EXISTS companyholding (
    company_id INT NOT NULL,
    security_id INT NOT NULL,
    quantity_held NUMERIC(10, 2) NOT NULL,
    purchase_date DATE NOT NULL,
    purchase_price NUMERIC(10, 2) NOT NULL
);
"""
cur.execute(create_companyholding_table_query)

with open('companyholding_data.json', 'r') as f:
    for line in f:
        record = json.loads(line)  
        insert_query = """
        INSERT INTO companyholding (company_id, security_id, quantity_held, purchase_date, purchase_price)
        VALUES (%s, %s, %s, %s, %s);
        """
        cur.execute(insert_query, (
            record['company_id'],
            record['security_id'],
            record['quantity_held'],
            record['purchase_date'],
            record['purchase_price']
        ))

conn.commit()
cur.close()
conn.close()
