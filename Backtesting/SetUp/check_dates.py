import datetime
from Methods import *
# Connect to your database

conn = establish_database_connection()
today = datetime.date.today()
cur = conn.cursor()
cur.execute("SELECT date_column FROM your_table")

dates_from_table = [row[0] for row in cur.fetchall()]

# Check if today's date matches any date in the table
if today in dates_from_table:
    # Perform the action or run the desired script here
    print("Today's date matches a date in the table. Run your script or action here.")

# Close database connection
conn.close()
