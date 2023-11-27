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

try:
    # Begin a transaction
    conn.autocommit = False

    # Insert records into one table
    cur.execute("INSERT INTO books (title, author, publication_year) VALUES (%s, %s, %s)", ('The Catcher in the Rye', 'J. D. Salinger', 1951))

    # Update a record in the "customers" table
    cur.execute("UPDATE customers SET phone = %s WHERE email = %s", ('416-111-1111', 'amy@gmail.com'))

    # Commit the transaction to save the changes to the database
    conn.commit()

except Exception as e:
    # Rollback the transaction in case of an error
    conn.rollback()
    print(f"Error: {e}")

finally:
    # Close the cursor and the connection
    cur.close()
    conn.close()
