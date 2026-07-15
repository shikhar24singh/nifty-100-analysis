import sqlite3
import pandas as pd
import random

conn = sqlite3.connect("db/nifty100.db")

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

sample = companies.sample(
    n=5,
    random_state=42
)

print(sample)

sample.to_csv(
    "output/manual_review.csv",
    index=False
)


for company in sample["id"]:

    print("\n", company)

    years = pd.read_sql(

        f"""
        SELECT year
        FROM profitandloss
        WHERE company_id='{company}'
        ORDER BY year
        """,

        conn

    )

    print(years)
    
coverage = pd.read_sql("""

SELECT

company_id,

COUNT(DISTINCT year) AS total_years

FROM profitandloss

GROUP BY company_id

HAVING COUNT(DISTINCT year) < 5

ORDER BY total_years

""", conn)

print(coverage)

coverage.to_csv(

    "output/companies_less_than_5_years.csv",

    index=False

)

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

for table in tables:

    count = conn.execute(

        f"SELECT COUNT(*) FROM {table}"

    ).fetchone()[0]

    print(table, count)

conn.close()
