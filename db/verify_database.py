import sqlite3

connection = sqlite3.connect("db/nifty100.db")

cursor = connection.cursor()

cursor.execute("""

SELECT name

FROM sqlite_master

WHERE type='table'

""")

for table in cursor.fetchall():

    print(table[0])

connection.close()