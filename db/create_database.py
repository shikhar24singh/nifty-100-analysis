import sqlite3


def create_database():

    connection = sqlite3.connect("db/nifty100.db")

    connection.execute(
        "PRAGMA foreign_keys = ON;"
    )

    cursor = connection.cursor()

    with open("db/schema.sql", "r") as file:

        schema = file.read()

    cursor.executescript(schema)

    connection.commit()

    connection.close()

    print("Database created successfully.")


if __name__ == "__main__":

    create_database()