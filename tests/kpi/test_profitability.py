import pytest

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    check_opm,
    return_on_equity,
    return_on_capital_employed,
    roce_status,
    return_on_assets,
)


def test_net_profit_margin():

    assert net_profit_margin(20, 100) == 20.0


def test_net_profit_margin_zero_sales():

    assert net_profit_margin(20, 0) is None


def test_operating_profit_margin():

    assert operating_profit_margin(25, 100) == 25.0


def test_opm_crosscheck():

    calculated = operating_profit_margin(25, 100)

    assert check_opm(calculated, 22) is True


def test_return_on_equity():

    assert return_on_equity(25, 50, 50) == 25.0


def test_return_on_equity_negative():

    assert return_on_equity(20, -10, 5) is None


def test_return_on_capital_employed():

    assert return_on_capital_employed(30, 50, 100, 50) == 15.0


def test_return_on_assets():

    assert return_on_assets(20, 200) == 10.0