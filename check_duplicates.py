import sqlite3
import pandas as pd

conn = sqlite3.connect("db/nifty100.db")

print(pd.read_sql("""
SELECT *
FROM cashflow
WHERE company_id = 'ABB'
AND year = 'Mar 2015';
""", conn))

conn.close()