from src.analytics.cashflow import *


def test_free_cash_flow():

    assert free_cash_flow(
        500,
        -200
    ) == 300


def test_cfo_quality():

    score, label = cfo_quality_score(
        [100, 110, 120, 130, 140],
        [80, 90, 100, 110, 120]
    )

    assert label == "High Quality"


def test_pat_zero():

    assert cfo_quality_score(
        [100],
        [0]
    ) is None


def test_capex_asset_light():

    value, label = capex_intensity(
        -20,
        1000
    )

    assert label == "Asset Light"


def test_capex_capital_intensive():

    value, label = capex_intensity(
        -120,
        1000
    )

    assert label == "Capital Intensive"


def test_fcf_conversion():

    assert fcf_conversion_rate(
        300,
        500
    ) == 60.0


def test_zero_operating_profit():

    assert fcf_conversion_rate(
        100,
        0
    ) is None


def test_reinvestor():

    result = capital_allocation_pattern(
        100,
        -50,
        -20
    )

    assert result["pattern_label"] == "Reinvestor"


def test_growth_funded():

    result = capital_allocation_pattern(
        -100,
        -50,
        120
    )

    assert result["pattern_label"] == "Growth Funded by Debt"


def test_cash_accumulator():

    result = capital_allocation_pattern(
        100,
        50,
        25
    )

    assert result["pattern_label"] == "Cash Accumulator"