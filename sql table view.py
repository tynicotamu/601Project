import sqlite3


# Function to print the first three rows of a table
def print_top_three_rows(db_path, table_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Execute a query to retrieve the first three rows
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")

    # Fetch all the results
    rows = cursor.fetchall()

    # Print the rows
    for row in rows:
        print(row)

    # Close the connection
    conn.close()


# Usage
db_path = 'data/f1stats.db'  # Replace with the path to your database file
table_name = 'circuits'  # Replace with the name of your table
print_top_three_rows(db_path, table_name)
