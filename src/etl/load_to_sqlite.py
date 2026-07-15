import os
import sqlite3
import pandas as pd

from src.etl.loader import ExcelLoader


class SQLiteLoader:

    def __init__(self):

        self.connection = sqlite3.connect(
            "db/nifty100.db"
        )

        self.connection.execute(
            "PRAGMA foreign_keys = ON;"
        )

        self.loader = ExcelLoader()

        self.audit = []

    def close(self):

        self.connection.commit()

        self.connection.close()

    def clear_tables(self):

        tables = [

            "stock_prices",
            "financial_ratios",
            "cashflow",
            "balancesheet",
            "profitandloss",
            "prosandcons",
            "documents",
            "analysis",
            "sectors",
            "companies"

        ]

        for table in tables:

            self.connection.execute(
                f"DELETE FROM {table};"
            )

        self.connection.commit()

    def insert_table(self, table_name, dataframe):

        if table_name != "companies" and "company_id" in dataframe.columns:

            company_ids = pd.read_sql(
                "SELECT id FROM companies",
                self.connection
            )["id"]

            valid_ids = set(company_ids)

            valid_rows = dataframe[
                dataframe["company_id"].isin(valid_ids)
            ]

            rejected_rows = dataframe[
                ~dataframe["company_id"].isin(valid_ids)
            ]

        else:

            valid_rows = dataframe

            rejected_rows = pd.DataFrame()

        valid_rows.to_sql(

            table_name,

            self.connection,

            if_exists="append",

            index=False

        )

        loaded = len(valid_rows)

        rejected = len(rejected_rows)

        self.audit.append({

            "table": table_name,

            "rows_loaded": loaded,

            "rows_rejected": rejected

        })

        print(
            f"{table_name} -> Loaded: {loaded} | Rejected: {rejected}"
        )

        if rejected > 0:

            rejected_rows["table"] = table_name

            rejected_rows["reason"] = "Foreign key not found"

            output_file = "output/rejected_rows.csv"

            import os

            if os.path.exists(output_file):

                rejected_rows.to_csv(

                    output_file,

                    mode="a",

                    header=False,

                    index=False

                )

            else:

                rejected_rows.to_csv(

                    output_file,

                    index=False

                )

                print(

                    rejected_rows[
                        ["company_id"]
                    ].drop_duplicates()

                )

    def load_all_tables(self):

        self.clear_tables()

        files = {

            "companies": "data/raw/companies.xlsx",

            "analysis": "data/raw/analysis.xlsx",

            "balancesheet": "data/raw/balancesheet.xlsx",

            "cashflow": "data/raw/cashflow.xlsx",

            "documents": "data/raw/documents.xlsx",

            "financial_ratios": "data/raw/financial_ratios.xlsx",

            "profitandloss": "data/raw/profitandloss.xlsx",

            "prosandcons": "data/raw/prosandcons.xlsx",

            "sectors": "data/raw/sectors.xlsx",

            "stock_prices": "data/raw/stock_prices.xlsx"

        }

        load_order = [

        "companies",

        "sectors",

        "analysis",

        "documents",

        "prosandcons",

        "profitandloss",

        "balancesheet",

        "cashflow",

        "financial_ratios",

        "stock_prices"

    ]

        for table in load_order:

            print(f"\nLoading {table}...")

            dataframe = self.loader.load_excel(

                files[table]

            )
            if table == "prosandcons":

                print("\nColumns:")
                print(dataframe.columns.tolist())

                print("\nFirst 5 rows:")
                print(dataframe.head())

            self.insert_table(

                table,

                dataframe

            )
            
        audit_df = pd.DataFrame(self.audit)

        audit_df.to_csv(
            "output/load_audit.csv",
            index=False
        )

        print("\nLoad audit saved.")

    def get_audit(self):

        return pd.DataFrame(

            self.audit

        )


if __name__ == "__main__":

    loader = SQLiteLoader()

    loader.load_all_tables()

    print()

    print(loader.get_audit())

    loader.close()