import pytest

from src.analytics.ratios import (

    debt_to_equity,

    high_leverage_flag,

    interest_coverage_ratio,

    icr_label,

    icr_warning,

    net_debt,

    asset_turnover

)


def test_de_ratio():

    assert debt_to_equity(

        100,

        50,

        50

    ) == 1.0


def test_debt_free():

    assert debt_to_equity(

        0,

        100,

        100

    ) == 0


def test_negative_equity():

    assert debt_to_equity(

        100,

        -50,

        20

    ) is None


def test_high_leverage():

    de = debt_to_equity(

        600,

        50,

        50

    )

    assert high_leverage_flag(

        de,

        "Technology"

    ) is True


def test_interest_coverage():

    assert interest_coverage_ratio(

        120,

        30,

        30

    ) == 5.0


def test_interest_zero():

    assert interest_coverage_ratio(

        100,

        20,

        0

    ) is None


def test_debt_free_label():

    assert icr_label(

        None

    ) == "Debt Free"


def test_asset_turnover():

    assert asset_turnover(

        500,

        250

    ) == 2.0