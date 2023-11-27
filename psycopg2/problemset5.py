import psycopg2

try:
    # Attempt to connect to a PostgreSQL database with incorrect credentials
    conn = psycopg2.connect(
        dbname='MyDatabase',
        user='postgres',
        password='bobwashere',
        host='localhost',
        port='5432'
    )

except Exception as e:
    print(f"Error: {e}")

# Close the connection if it was established
if 'conn' in locals():
    conn.close()
