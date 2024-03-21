import sqlite3, csv
import pandas as pd

conn = sqlite3.connect('testDB.db')
# load data
df = pd.read_csv('data/drivers.csv')
# drop data into database
df.to_sql("DRIVERS", conn)
conn.close()


conn = sqlite3.connect('testDB.db')
cur = conn.cursor()
query = pd.read_sql_query("SELECT * FROM DRIVERS", conn)