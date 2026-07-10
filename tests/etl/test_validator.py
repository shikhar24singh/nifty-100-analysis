import pandas as pd
from src.etl.validator import *

validator = DataValidator()

def test_primary_key_duplicates():

    df = pd.DataFrame({
        "id": [1, 2, 2, 3]
    })

    validator = DataValidator()

    validator.validate_primary_key(
        df,
        "test_table"
    )

    assert len(validator.failures) == 2
    
def test_company_year_duplicates():

    df = pd.DataFrame({

        "company_id": ["ABB", "ABB", "TCS"],

        "year": [2024, 2024, 2024]

    })

    validator = DataValidator()

    validator.validate_company_year(
        df,
        "profitandloss"
    )

    assert len(validator.failures) == 2
    
def test_foreign_key_validation():

    parent = pd.DataFrame({

        "id": [
            "ABB",
            "TCS",
            "INFY"
        ]

    })

    child = pd.DataFrame({

        "company_id": [
            "ABB",
            "XYZ",
            "TCS"
        ]

    })

    validator = DataValidator()

    validator.validate_foreign_key(
        parent,
        child,
        "profitandloss"
    )

    assert len(validator.failures) == 1
    
def test_balance_sheet_validation():

    df = pd.DataFrame({

        "equity_capital": [100],

        "reserves": [200],

        "borrowings": [50],

        "other_liabilities": [150],

        "total_liabilities": [600]

    })

    validator = DataValidator()

    validator.validate_balance_sheet(df)

    assert len(validator.failures) == 1

def test_opm_validation():

    df = pd.DataFrame({

        "sales": [1000],

        "operating_profit": [200],

        "opm_percentage": [15]

    })

    validator = DataValidator()

    validator.validate_opm(df)

    assert len(validator.failures) == 1
    
def test_positive_sales():

    df = pd.DataFrame({

        "sales": [
            1000,
            500,
            0,
            -100
        ]

    })

    validator = DataValidator()

    validator.validate_positive_sales(df)

    assert len(validator.failures) == 2
    
def test_net_cash_flow():

    df = pd.DataFrame({

        "operating_activity": [100],

        "investing_activity": [-20],

        "financing_activity": [-30],

        "net_cash_flow": [40]

    })

    validator = DataValidator()

    validator.validate_net_cash_flow(df)

    assert len(validator.failures) == 1
    
def test_tax_rate():

    df = pd.DataFrame({

        "tax_percentage": [
            25,
            -5,
            110,
            18
        ]

    })

    validator = DataValidator()

    validator.validate_tax_rate(df)

    assert len(validator.failures) == 2
    
def test_dividend_payout():

    df = pd.DataFrame({

        "dividend_payout_percentage": [
            40,
            -10,
            120,
            75
        ]

    })

    validator = DataValidator()

    validator.validate_dividend_payout(df)

    assert len(validator.failures) == 2
    
def test_eps_sign():

    df = pd.DataFrame({

        "net_profit": [
            100,
            -50,
            0,
            200
        ],

        "eps": [
            10,
            5,
            1,
            -8
        ]

    })

    validator = DataValidator()

    validator.validate_eps_sign(df)

    assert len(validator.failures) == 3
    
def test_cashflow_reconciliation():

    df = pd.DataFrame({

        "operating_activity": [100, 200],

        "investing_activity": [-30, -50],

        "financing_activity": [-20, -70],

        "net_cash_flow": [50, 100]

    })

    validator = DataValidator()

    validator.validate_cashflow_reconciliation(df)

    assert len(validator.failures) == 1

def test_assets_vs_liabilities():

    df = pd.DataFrame({

        "total_assets": [
            1000,
            500,
            800
        ],

        "total_liabilities": [
            900,
            700,
            800
        ]

    })

    validator = DataValidator()

    validator.validate_assets_vs_liabilities(df)

    assert len(validator.failures) == 1
    
def test_stock_price_duplicates():

    df = pd.DataFrame({

        "company_id": [
            "ABB",
            "ABB",
            "TCS"
        ],

        "date": [
            "2024-01-01",
            "2024-01-01",
            "2024-02-01"
        ]

    })

    validator = DataValidator()

    validator.validate_stock_price_duplicates(df)

    assert len(validator.failures) == 2

def test_url_validation():

    df = pd.DataFrame({

        "document_url": [
            "https://example.com/report.pdf",
            "http://company.com/file.pdf",
            "invalid_url",
            "www.google.com"
        ]

    })

    validator = DataValidator()

    validator.validate_urls(df)

    assert len(validator.failures) == 2

def test_mandatory_fields():

    df = pd.DataFrame({

        "company_id": [
            "ABB",
            None,
            ""
        ],

        "year": [
            2024,
            2023,
            None
        ]

    })

    validator = DataValidator()

    validator.validate_mandatory_fields(
        df,
        "profitandloss",
        ["company_id", "year"]
    )

    assert len(validator.failures) == 3
    
def test_year_coverage():

    df = pd.DataFrame({

        "company_id": [
            "ABB",
            "ABB",
            "ABB",
            "TCS",
            "TCS",
            "TCS",
            "TCS",
            "TCS"
        ],

        "year": [
            2020,
            2021,
            2022,
            2020,
            2021,
            2022,
            2023,
            2024
        ]

    })

    validator = DataValidator()

    validator.validate_year_coverage(
        df,
        "profitandloss"
    )

    assert len(validator.failures) == 1

validator.save_report()