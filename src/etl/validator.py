import os
import re
import re
import coverage
import pandas as pd


class DataValidator:

    def __init__(self):

        self.failures = []


    def log_failure(
        self,
        rule,
        severity,
        table,
        row,
        column,
        expected,
        actual
    ):

        self.failures.append({

            "Rule": rule,
            "Severity": severity,
            "Table": table,
            "Row": row,
            "Column": column,
            "Expected": expected,
            "Actual": actual

        })


    def save_report(
        self,
        filename="output/validation_failures.csv"
    ):

        os.makedirs(
            os.path.dirname(filename),
            exist_ok=True
        )

        df = pd.DataFrame(self.failures)

        df.to_csv(
            filename,
            index=False
        )

        print(
            f"\nValidation Report Saved → {filename}"
        )

        print(
            f"Total Issues Found : {len(df)}"
        )


    @staticmethod
    def column_exists(df, column):

        return column in df.columns

    @staticmethod
    def has_null(df, column):

        return df[column].isnull().any()

    @staticmethod
    def duplicate_rows(df, columns):

        return df[df.duplicated(columns)]

    @staticmethod
    def unique_values(df, column):

        return df[column].unique()

    @staticmethod
    def row_count(df):

        return len(df)

    @staticmethod
    def company_count(df):

        if "company_id" not in df.columns:
            return 0

        return df["company_id"].nunique()
    
    def validate_primary_key(
        self,
        df,
        table_name,
        primary_key="id"
    ):

        if primary_key not in df.columns:

            self.log_failure(
                rule="DQ-01",
                severity="CRITICAL",
                table=table_name,
                row="-",
                column=primary_key,
                expected="Primary Key Column Exists",
                actual="Column Missing"
            )

            return

        duplicates = df[df.duplicated(primary_key, keep=False)]

        if duplicates.empty:
            return

        for idx, row in duplicates.iterrows():

            self.log_failure(
                rule="DQ-01",
                severity="CRITICAL",
                table=table_name,
                row=idx,
                column=primary_key,
                expected="Unique",
                actual=row[primary_key]
            )

    def validate_company_year(
        self,
        df,
        table_name
    ):

        required_columns = ["company_id", "year"]

        for column in required_columns:

            if column not in df.columns:

                self.log_failure(
                    rule="DQ-02",
                    severity="CRITICAL",
                    table=table_name,
                    row="-",
                    column=column,
                    expected="Column Exists",
                    actual="Column Missing"
                )

                return

        duplicates = df[df.duplicated(["company_id", "year"], keep=False)]

        if duplicates.empty:
            return

        for idx, row in duplicates.iterrows():

            self.log_failure(
                rule="DQ-02",
                severity="CRITICAL",
                table=table_name,
                row=idx,
                column="company_id, year",
                expected="Unique Combination",
                actual=f"{row['company_id']} | {row['year']}"
            )
    def validate_foreign_key(
        self,
        parent_df,
        child_df,
        child_table,
        parent_key="id",
        child_key="company_id"
    ):

        if parent_key not in parent_df.columns:

            self.log_failure(
                rule="DQ-03",
                severity="CRITICAL",
                table="companies",
                row="-",
                column=parent_key,
                expected="Column Exists",
                actual="Column Missing"
            )

            return

        if child_key not in child_df.columns:

            self.log_failure(
                rule="DQ-03",
                severity="CRITICAL",
                table=child_table,
                row="-",
                column=child_key,
                expected="Column Exists",
                actual="Column Missing"
            )

            return

        valid_ids = set(parent_df[parent_key])

        invalid_rows = child_df[
            ~child_df[child_key].isin(valid_ids)
        ]

        for idx, row in invalid_rows.iterrows():

            self.log_failure(
                rule="DQ-03",
                severity="CRITICAL",
                table=child_table,
                row=idx,
                column=child_key,
                expected="Existing Company ID",
                actual=row[child_key]
            )
    
    def validate_balance_sheet(
        self,
        df,
        table_name="balancesheet",
        tolerance=0.01
    ):

        required_columns = [
            "equity_capital",
            "reserves",
            "borrowings",
            "other_liabilities",
            "total_liabilities"
        ]

        for column in required_columns:

            if column not in df.columns:

                self.log_failure(
                    rule="DQ-04",
                    severity="CRITICAL",
                    table=table_name,
                    row="-",
                    column=column,
                    expected="Column Exists",
                    actual="Column Missing"
                )

                return

        for idx, row in df.iterrows():

            calculated = (
                row["equity_capital"]
                + row["reserves"]
                + row["borrowings"]
                + row["other_liabilities"]
            )

            actual = row["total_liabilities"]

            if actual == 0:
                continue

            difference = abs(calculated - actual) / actual

            if difference > tolerance:

                self.log_failure(
                    rule="DQ-04",
                    severity="WARNING",
                    table=table_name,
                    row=idx,
                    column="total_liabilities",
                    expected=round(calculated, 2),
                    actual=actual
                )
                
    def validate_opm(
        self,
        df,
        table_name="profitandloss",
        tolerance=0.5
    ):

        required_columns = [
            "sales",
            "operating_profit",
            "opm_percentage"
        ]

        for column in required_columns:

            if column not in df.columns:

                self.log_failure(
                    rule="DQ-05",
                    severity="CRITICAL",
                    table=table_name,
                    row="-",
                    column=column,
                    expected="Column Exists",
                    actual="Column Missing"
                )

                return

        for idx, row in df.iterrows():

            sales = row["sales"]

            if pd.isna(sales) or sales == 0:
                continue

            operating_profit = row["operating_profit"]
            actual_opm = row["opm_percentage"]

            calculated_opm = (operating_profit / sales) * 100

            if abs(calculated_opm - actual_opm) > tolerance:

                self.log_failure(
                    rule="DQ-05",
                    severity="WARNING",
                    table=table_name,
                    row=idx,
                    column="opm_percentage",
                    expected=round(calculated_opm, 2),
                    actual=actual_opm
                )
                
    def validate_positive_sales(
        self,
        df,
        table_name="profitandloss"
    ):

        if "sales" not in df.columns:

            self.log_failure(
                rule="DQ-06",
                severity="CRITICAL",
                table=table_name,
                row="-",
                column="sales",
                expected="Column Exists",
                actual="Column Missing"
            )

            return

        invalid_rows = df[df["sales"] <= 0]

        for idx, row in invalid_rows.iterrows():

            self.log_failure(
                rule="DQ-06",
                severity="WARNING",
                table=table_name,
                row=idx,
                column="sales",
                expected="Sales > 0",
                actual=row["sales"]
            )
            
    def validate_net_cash_flow(
        self,
        df,
        table_name="cashflow",
        tolerance=1
    ):

        required_columns = [
            "operating_activity",
            "investing_activity",
            "financing_activity",
            "net_cash_flow"
        ]

        for column in required_columns:

            if column not in df.columns:

                self.log_failure(
                    rule="DQ-07",
                    severity="CRITICAL",
                    table=table_name,
                    row="-",
                    column=column,
                    expected="Column Exists",
                    actual="Column Missing"
                )

                return

        for idx, row in df.iterrows():

            operating = row["operating_activity"]
            investing = row["investing_activity"]
            financing = row["financing_activity"]
            actual = row["net_cash_flow"]

            if pd.isna(operating) or pd.isna(investing) or pd.isna(financing) or pd.isna(actual):
                continue

            calculated = operating + investing + financing

            if abs(calculated - actual) > tolerance:

                self.log_failure(
                    rule="DQ-07",
                    severity="WARNING",
                    table=table_name,
                    row=idx,
                    column="net_cash_flow",
                    expected=calculated,
                    actual=actual
                )
    
    def validate_tax_rate(
        self,
        df,
        table_name="profitandloss"
    ):

        if "tax_percentage" not in df.columns:

            self.log_failure(
                rule="DQ-08",
                severity="CRITICAL",
                table=table_name,
                row="-",
                column="tax_percentage",
                expected="Column Exists",
                actual="Column Missing"
            )

            return

        invalid_rows = df[
            (df["tax_percentage"] < 0) |
            (df["tax_percentage"] > 100)
        ]

        for idx, row in invalid_rows.iterrows():

            self.log_failure(
                rule="DQ-08",
                severity="WARNING",
                table=table_name,
                row=idx,
                column="tax_percentage",
                expected="0 - 100",
                actual=row["tax_percentage"]
            )
    
    def validate_dividend_payout(
        self,
        df,
        table_name="profitandloss"
    ):

        if "dividend_payout_percentage" not in df.columns:

            self.log_failure(
                rule="DQ-09",
                severity="CRITICAL",
                table=table_name,
                row="-",
                column="dividend_payout_percentage",
                expected="Column Exists",
                actual="Column Missing"
            )

            return

        invalid_rows = df[
            (df["dividend_payout_percentage"] < 0) |
            (df["dividend_payout_percentage"] > 100)
        ]

        for idx, row in invalid_rows.iterrows():

            self.log_failure(
                rule="DQ-09",
                severity="WARNING",
                table=table_name,
                row=idx,
                column="dividend_payout_percentage",
                expected="0 - 100",
                actual=row["dividend_payout_percentage"]
            )
    
    def validate_eps_sign(
        self,
        df,
        table_name="profitandloss"
    ):

        required_columns = [
            "net_profit",
            "eps"
        ]

        for column in required_columns:

            if column not in df.columns:

                self.log_failure(
                    rule="DQ-10",
                    severity="CRITICAL",
                    table=table_name,
                    row="-",
                    column=column,
                    expected="Column Exists",
                    actual="Column Missing"
                )

                return

        for idx, row in df.iterrows():

            net_profit = row["net_profit"]
            eps = row["eps"]

            if pd.isna(net_profit) or pd.isna(eps):
                continue

            invalid = (
                (net_profit > 0 and eps <= 0) or
                (net_profit < 0 and eps >= 0) or
                (net_profit == 0 and eps != 0)
            )

            if invalid:

                self.log_failure(
                    rule="DQ-10",
                    severity="WARNING",
                    table=table_name,
                    row=idx,
                    column="eps",
                    expected="EPS sign should match Net Profit",
                    actual=eps
                )
    
    def validate_cashflow_reconciliation(
        self,
        df,
        table_name="cashflow",
        tolerance=1
    ):

        required_columns = [
            "operating_activity",
            "investing_activity",
            "financing_activity",
            "net_cash_flow"
        ]

        for column in required_columns:

            if column not in df.columns:

                self.log_failure(
                    rule="DQ-11",
                    severity="CRITICAL",
                    table=table_name,
                    row="-",
                    column=column,
                    expected="Column Exists",
                    actual="Column Missing"
                )

                return

        for idx, row in df.iterrows():

            if row[required_columns].isnull().any():
                continue

            expected_cash_flow = (
                row["operating_activity"]
                + row["investing_activity"]
                + row["financing_activity"]
            )

            actual_cash_flow = row["net_cash_flow"]

            if abs(expected_cash_flow - actual_cash_flow) > tolerance:

                self.log_failure(
                    rule="DQ-11",
                    severity="WARNING",
                    table=table_name,
                    row=idx,
                    column="net_cash_flow",
                    expected=expected_cash_flow,
                    actual=actual_cash_flow
                )
                
    def validate_assets_vs_liabilities(
        self,
        df,
        table_name="balancesheet"
    ):

        required_columns = [
            "total_assets",
            "total_liabilities"
        ]

        for column in required_columns:

            if column not in df.columns:

                self.log_failure(
                    rule="DQ-12",
                    severity="CRITICAL",
                    table=table_name,
                    row="-",
                    column=column,
                    expected="Column Exists",
                    actual="Column Missing"
                )

                return

        invalid_rows = df[
            df["total_assets"] < df["total_liabilities"]
        ]

        for idx, row in invalid_rows.iterrows():

            self.log_failure(
                rule="DQ-12",
                severity="WARNING",
                table=table_name,
                row=idx,
                column="total_assets",
                expected=f">= {row['total_liabilities']}",
                actual=row["total_assets"]
            )

    def validate_stock_price_duplicates(
        self,
        df,
        table_name="stock_prices"
    ):

        required_columns = [
            "company_id",
            "date"
        ]

        for column in required_columns:

            if column not in df.columns:

                self.log_failure(
                    rule="DQ-13",
                    severity="CRITICAL",
                    table=table_name,
                    row="-",
                    column=column,
                    expected="Column Exists",
                    actual="Column Missing"
                )

                return

        duplicates = df[
            df.duplicated(
                ["company_id", "date"],
                keep=False
            )
        ]

        for idx, row in duplicates.iterrows():

            self.log_failure(
                rule="DQ-13",
                severity="CRITICAL",
                table=table_name,
                row=idx,
                column="company_id, date",
                expected="Unique Combination",
                actual=f"{row['company_id']} | {row['date']}"
            )
    
    def validate_urls(
        self,
        df,
        table_name="documents"
    ):


        if "document_url" not in df.columns:

            self.log_failure(
                rule="DQ-14",
                severity="CRITICAL",
                table=table_name,
                row="-",
                column="document_url",
                expected="Column Exists",
                actual="Column Missing"
            )

            return

        pattern = re.compile(
            r"^https?://[^\s]+$",
            re.IGNORECASE
        )

        for idx, row in df.iterrows():

            url = row["document_url"]

            if pd.isna(url):
                continue

            if not pattern.match(str(url).strip()):

                self.log_failure(
                    rule="DQ-14",
                    severity="WARNING",
                    table=table_name,
                    row=idx,
                    column="document_url",
                    expected="Valid HTTP/HTTPS URL",
                    actual=url
                )
    
    def validate_mandatory_fields(
        self,
        df,
        table_name,
        required_columns
    ):

        for column in required_columns:

            if column not in df.columns:

                self.log_failure(
                    rule="DQ-15",
                    severity="CRITICAL",
                    table=table_name,
                    row="-",
                    column=column,
                    expected="Column Exists",
                    actual="Column Missing"
                )

                continue

            for idx, value in df[column].items():

                if pd.isna(value) or str(value).strip() == "":

                    self.log_failure(
                        rule="DQ-15",
                        severity="CRITICAL",
                        table=table_name,
                        row=idx,
                        column=column,
                        expected="Non-null value",
                        actual=value
                    )
    
    def validate_year_coverage(
        self,
        df,
        table_name,
        minimum_years=5
    ):

        required_columns = [
            "company_id",
            "year"
        ]

        for column in required_columns:

            if column not in df.columns:

                self.log_failure(
                    rule="DQ-16",
                    severity="CRITICAL",
                    table=table_name,
                    row="-",
                    column=column,
                    expected="Column Exists",
                    actual="Column Missing"
                )

                return

        coverage = (
            df.groupby("company_id")["year"]
            .nunique()
        )

        for company, years in coverage.items():

            if years < minimum_years:

                self.log_failure(
                    rule="DQ-16",
                    severity="WARNING",
                    table=table_name,
                    row="-",
                    column="year",
                    expected=f"At least {minimum_years} years",
                    actual=f"{company}: {years} years"
                )
    
    def summary(self):

        if len(self.failures) == 0:

            print("\n✓ No validation failures found.")

            return

        df = pd.DataFrame(self.failures)

        print("\n===============================")
        print(" Validation Summary")
        print("===============================")

        print(df.groupby("Severity").size())

        print("\nRule Counts")

        print(df.groupby("Rule").size())


    def clear(self):

        self.failures = []


    def get_failures(self):

        return pd.DataFrame(self.failures)




if __name__ == "__main__":

    validator = DataValidator()

    print("Validator Initialized")

    print()

    print("Current Failures")

    print(validator.get_failures())