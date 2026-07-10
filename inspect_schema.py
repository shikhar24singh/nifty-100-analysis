import os
import pandas as pd

folder = "data/raw"

for file in sorted(os.listdir(folder)):
    if file.endswith(".xlsx"):

        print("=" * 100)
        print(file)

        excel_path = os.path.join(folder, file)

        xl = pd.ExcelFile(excel_path)

        for sheet in xl.sheet_names:

            print(f"\nSheet: {sheet}")

            df = pd.read_excel(
                excel_path,
                sheet_name=sheet,
                header=None,
                nrows=12
            )

            print(df.to_string(index=True, header=False))
            print("\n")