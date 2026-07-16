from math import isclose


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