import pytest
from src.etl.loader import ExcelLoader


loader = ExcelLoader()


def test_load_companies():

    df = loader.load_excel("data/raw/companies.xlsx")

    assert not df.empty


def test_dataframe_type():

    df = loader.load_excel("data/raw/companies.xlsx")

    assert df is not None


def test_file_not_found():

    with pytest.raises(FileNotFoundError):

        loader.load_excel("data/raw/random.xlsx")