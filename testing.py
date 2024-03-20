import os
import sqlite3
import pandas as pd

csv_files = ['circuits.csv', 'constructor_results.csv', 'constructor_standings.csv', 'constructors.csv', 'driver_standings.csv', 'drivers.csv', 'lap_times.csv', 'pit_stops.csv', 'qualifying.csv', 'races.csv', 'results.csv', 'seasons.csv', 'sprint_results.csv', 'status.csv']
csv_directory_path = 'data/csv_repo'  # Ensure this path is correct
sqlite_db_path = 'data/f1stats.db'    # Ensure this path is correct

conn = sqlite3.connect(sqlite_db_path)
print(f"Connected to database: {sqlite_db_path}")

for csv_file in csv_files:
    csv_path = os.path.join(csv_directory_path, csv_file)
    if os.path.isfile(csv_path):
        df = pd.read_csv(csv_path)
        table_name = csv_file.replace('.csv', '')
        df.to_sql(table_name, conn, if_exists='replace', index=False)
        print(f"Table '{table_name}' created with {len(df)} rows.")
    else:
        print(f"File '{csv_file}' does not exist in the directory '{csv_directory_path}'.")

conn.close()
print("Database connection closed.")
