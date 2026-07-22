import sqlite3
import pandas as pd

from src.analytics.cashflow import (
    cfo_quality_score,
    capital_allocation_pattern
)

DB_PATH = "db/nifty100.db"
OUTPUT_FILE = "output/capital_allocation.csv"


def generate_capital_allocation():

    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT
        c.company_id,
        c.year,
        c.operating_activity,
        c.investing_activity,
        c.financing_activity,
        p.net_profit
    FROM (
        SELECT *
        FROM cashflow
        WHERE NOT (
            operating_activity = 0
            AND investing_activity = 0
            AND financing_activity = 0
            AND net_cash_flow = 0
        )
    ) c
    LEFT JOIN (
        SELECT DISTINCT
            company_id,
            year,
            net_profit
        FROM profitandloss
    ) p
    ON c.company_id = p.company_id
    AND c.year = p.year
    ORDER BY
        c.company_id,
        c.year;
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    output = []

    for company_id, company_data in df.groupby("company_id"):

        company_data = company_data.sort_values("year")

        quality = cfo_quality_score(
            company_data["operating_activity"].tolist(),
            company_data["net_profit"].tolist()
        )

        if quality is None:
            cfo_pat_ratio = None
        else:
            cfo_pat_ratio = quality[0]

        for _, row in company_data.iterrows():

            pattern = capital_allocation_pattern(
                row["operating_activity"],
                row["investing_activity"],
                row["financing_activity"],
                cfo_pat_ratio
            )

            output.append({
                "company_id": row["company_id"],
                "year": row["year"],
                "cfo_sign": pattern["cfo_sign"],
                "cfi_sign": pattern["cfi_sign"],
                "cff_sign": pattern["cff_sign"],
                "pattern_label": pattern["pattern_label"]
            })

    output_df = pd.DataFrame(output)

    output_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print(output_df.head())
    print(f"\nSaved to {OUTPUT_FILE}")


if __name__ == "__main__":
    generate_capital_allocation()