from fileinput import filename
import os
import re
import pandas as pd


class ExcelLoader:
    """
    Smart Excel Loader for Bluestock Nifty100 Project
    """

    def __init__(self):
        pass

    def _clean_column_name(self, col):
        """
        Standardize column names.
        Example:
        'Company Name' -> 'company_name'
        'Operating Profit %' -> 'operating_profit_pct'
        """

        col = str(col).strip().lower()

        col = col.replace("%", "_pct")
        col = col.replace("&", "and")
        col = col.replace("/", "_")

        col = re.sub(r"[^\w\s]", "", col)
        col = re.sub(r"\s+", "_", col)

        return col

    def _find_header_row(self, filepath, sheet_name=0):
    
        preview = pd.read_excel(
            filepath,
            sheet_name=sheet_name,
            header=None,
            nrows=20
        )

        keywords = {

            "id",

            "company_id",

            "company_name",

            "year",

            "date",

            "sales",

            "revenue",

            "profit",

            "assets",

            "liabilities",

            "pros",

            "cons",

            "company_logo",

            "website",

            "broad_sector",

            "open_price",

            "close_price"

        }

        for i, row in preview.iterrows():

            matches = 0

            for cell in row:

            
                if pd.isna(cell):
                    continue

                cell = str(cell).strip().lower()

                if any(keyword in cell for keyword in keywords):
                    matches += 1

            if matches >= 2:
                return i

        return 0

    def load_excel(self, filepath, sheet_name=0):

        if not os.path.exists(filepath):
            raise FileNotFoundError(filepath)
        
        filename = filepath.lower()

        fixed_headers = {

            "companies.xlsx": 1,
            "analysis.xlsx": 1,
            "balancesheet.xlsx": 1,
            "cashflow.xlsx": 1,
            "documents.xlsx": 1,
            "profitandloss.xlsx": 1,
            "prosandcons.xlsx": 1

        }

        for file, row in fixed_headers.items():

            if  filename.endswith(file):

                header_row = row

                break

            else:

                header_row = self._find_header_row(
                    filepath,
                    sheet_name
                )

        header_row = self._find_header_row(filepath, sheet_name)

        df = pd.read_excel(
            filepath,
            sheet_name=sheet_name,
            header=header_row
        )

        df.dropna(how="all", inplace=True)

        
        df.dropna(axis=1, how="all", inplace=True)

        
        df.columns = [
            self._clean_column_name(c)
            for c in df.columns
        ]

        
        for col in df.columns:

            if df[col].dtype == object:

                df[col] = df[col].astype(str).str.strip()

        return df

    def load_folder(self, folder):

        datasets = {}

        for file in os.listdir(folder):

            if file.endswith(".xlsx"):

                path = os.path.join(folder, file)

                name = os.path.splitext(file)[0]

                try:

                    datasets[name] = self.load_excel(path)

                    print(f"✓ Loaded {file}")

                except Exception as e:

                    print(f"✗ Failed {file}")

                    print(e)

        return datasets


if __name__ == "__main__":

    loader = ExcelLoader()

    data = loader.load_folder("data/raw")

    print("\nDatasets Loaded:\n")

    for name, df in data.items():

        print(f"{name}")

        print(df.head())

        print(df.columns.tolist())

        print("-" * 80)