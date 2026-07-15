import sqlite3

conn = sqlite3.connect("db/nifty100.db")

tables = [

    "companies",
    "analysis",
    "documents",
    "prosandcons",
    "profitandloss",
    "balancesheet",
    "cashflow",
    "financial_ratios",
    "stock_prices",
    "sectors"

]

print("\nDATABASE SUMMARY\n")

for table in tables:

    count = conn.execute(

        f"SELECT COUNT(*) FROM {table}"

    ).fetchone()[0]

    print(f"{table:<20}{count}")

conn.close()