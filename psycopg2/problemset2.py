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

# Create a new table for books
# cur.execute('''
#     CREATE TABLE books (
#         id serial PRIMARY KEY,
#         title VARCHAR,
#         author VARCHAR,
#         publication_year INTEGER
#     )
# ''')

# Insert data into the table using the correct SQL syntax
cur.execute("INSERT INTO books (title, author, publication_year) VALUES (%s, %s, %s)", ('The Great Gatsby', 'F. Scott Fitzgerald', 1925))
cur.execute("INSERT INTO books (title, author, publication_year) VALUES (%s, %s, %s)", ('The Adventures of Huckleberry Finn', 'Mark Twain', 1884))

# Update the publication year of a specific book
cur.execute("UPDATE books SET publication_year = %s WHERE title = %s", (1884, 'The Adventures of Huckleberry Finn'))

# Delete a book record
cur.execute("DELETE FROM books WHERE title = %s", ('The Great Gatsby',))

# Commit the changes to the database
conn.commit()

# Retrieve and display the remaining book records
cur.execute("SELECT * FROM books")
for row in cur.fetchall():
    print(row)

# Close the cursor and the connection
cur.close()
conn.close()
