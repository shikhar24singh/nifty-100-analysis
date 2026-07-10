import re


def normalize_year(value):
    """
    Converts:
    FY24
    FY2024
    2024.0
    2024-25

    into

    2024
    """

    if value is None:
        return None

    value = str(value).strip().upper()

    if value.startswith("FY"):
        value = value.replace("FY", "")

    if "-" in value:
        value = value.split("-")[0]

    value = value.replace(".0", "")

    if len(value) == 2:
        value = "20" + value

    return int(value)


def normalize_ticker(value):

    if value is None:
        return None

    value = str(value).upper().strip()

    value = value.replace(".NS", "")
    value = value.replace(".BO", "")

    return value


def clean_company_name(name):

    if name is None:
        return None

    name = str(name).strip()

    name = name.replace("Ltd.", "")
    name = name.replace("Limited", "")

    return name.strip()


def clean_currency(value):

    if value is None:
        return None

    value = str(value)

    value = value.replace("₹", "")
    value = value.replace(",", "")

    return float(value)


def clean_percentage(value):

    if value is None:
        return None

    value = str(value)

    value = value.replace("%", "")

    return float(value)