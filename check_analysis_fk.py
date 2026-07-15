from src.etl.loader import ExcelLoader

loader = ExcelLoader()

companies = loader.load_excel("data/raw/companies.xlsx")
analysis = loader.load_excel("data/raw/analysis.xlsx")

print("Companies columns:")
print(companies.columns.tolist())

print("\nAnalysis columns:")
print(analysis.columns.tolist())

print("\nFirst 10 company IDs:")
print(companies["id"].head(10).tolist())

print("\nFirst 10 analysis company IDs:")
print(analysis["company_id"].head(10).tolist())

company_ids = set(companies["id"])

invalid = analysis[~analysis["company_id"].isin(company_ids)]

print("\nInvalid rows:", len(invalid))

if len(invalid) > 0:
    print(invalid[["company_id"]].drop_duplicates())