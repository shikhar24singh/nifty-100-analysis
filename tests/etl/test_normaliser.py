from src.etl.normaliser import *


def test_year1():
    assert normalize_year("FY24") == 2024


def test_year2():
    assert normalize_year("FY2024") == 2024


def test_year3():
    assert normalize_year("2024.0") == 2024


def test_year4():
    assert normalize_year("2024-25") == 2024


def test_year5():
    assert normalize_year(2024) == 2024


def test_ticker1():
    assert normalize_ticker("tcs") == "TCS"


def test_ticker2():
    assert normalize_ticker("TCS.NS") == "TCS"


def test_ticker3():
    assert normalize_ticker("TCS.BO") == "TCS"


def test_ticker4():
    assert normalize_ticker(" tcs ") == "TCS"


def test_company():
    assert clean_company_name("Infosys Ltd.") == "Infosys"


def test_currency():
    assert clean_currency("₹1,20,000") == 120000.0


def test_percentage():
    assert clean_percentage("18.5%") == 18.5