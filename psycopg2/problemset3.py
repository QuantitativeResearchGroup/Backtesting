import psycopg2

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

cur.execute('''
    CREATE TABLE customers (
        id serial PRIMARY KEY,
        name VARCHAR,
        email VARCHAR,
        phone VARCHAR
    )
''')

# Insert multiple customer records using prepared statements
customer_data = [
    ('Amy', 'amy@gmail.com', '123-456-7890'),
    ('Bob', 'bob@gmail.com', '987-654-3210'),
    ('Cark', 'carl@gmail.com', '555-555-5555')
]

insert_query = "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)"
cur.executemany(insert_query, customer_data)

# Commit the changes to the database
conn.commit()

# Retrieve and display customer records
cur.execute("SELECT * FROM customers")
for row in cur.fetchall():
    print(row)

# Close the cursor and the connection
cur.close()
conn.close()
