import sqlite3

conn = sqlite3.connect(
    "db/nifty100.db"
)

rows = conn.execute(

    "PRAGMA foreign_key_check;"

).fetchall()

if rows:

    print("Foreign key issues found:")

    for row in rows:

        print(row)

else:

    print("All foreign keys are valid.")

conn.close()