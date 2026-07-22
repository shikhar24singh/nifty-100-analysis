import math

def net_profit_margin(net_profit, sales):

    if sales == 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit, sales):

    if sales == 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def check_opm(opm_calculated, opm_source):

    if opm_calculated is None or opm_source is None:
        return False

    return abs(opm_calculated - opm_source) > 1


def return_on_equity(net_profit, equity_capital, reserves):

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round((net_profit / equity) * 100, 2)


def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings
):

    capital_employed = equity_capital + reserves + borrowings

    if capital_employed <= 0:
        return None

    return round((ebit / capital_employed) * 100, 2)


def roce_status(roce, broad_sector):

    if roce is None:
        return "Unavailable"

    if broad_sector == "Financials":

        if roce >= 12:
            return "Good"

        return "Below Benchmark"

    if roce >= 15:
        return "Good"

    return "Below Benchmark"


def return_on_assets(net_profit, total_assets):

    if total_assets == 0:
        return None

    return round((net_profit / total_assets) * 100, 2)

def debt_to_equity(borrowings, equity_capital, reserves):

    if borrowings == 0:
        return 0

    equity = equity_capital + reserves

    if equity <= 0:
        return None

    return round(borrowings / equity, 2)


def high_leverage_flag(de_ratio, broad_sector):

    if de_ratio is None:
        return False

    if broad_sector == "Financials":
        return False

    return de_ratio > 5


def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):

    if interest == 0:
        return None

    return round(
        (operating_profit + other_income) / interest,
        2
    )


def icr_label(icr):

    if icr is None:
        return "Debt Free"

    return ""


def icr_warning(icr):

    if icr is None:
        return False

    return icr < 1.5


def net_debt(
    borrowings,
    investments
):

    return borrowings - investments


def asset_turnover(
    sales,
    total_assets
):

    if total_assets == 0:
        return None

    return round(
        sales / total_assets,
        2
    )