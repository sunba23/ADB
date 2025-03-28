import sqlite3
import pandas as pd

conn = sqlite3.connect("../db/database.sqlite")

cursor = conn.cursor()
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

for table_name in tables:
    table_name = table_name[0]
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    df.to_csv(f"../csv/{table_name}.csv", index=False)
    print(f"Exported {table_name} to CSV")

conn.close()
