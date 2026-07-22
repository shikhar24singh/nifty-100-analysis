from src.analytics.cagr import (
    calculate_cagr,
    revenue_cagr,
    pat_cagr,
    eps_cagr
)


def test_normal_cagr():

    value, flag = calculate_cagr(
        100,
        200,
        5
    )

    assert round(value, 2) == 14.87
    assert flag == "NORMAL"


def test_turnaround():

    value, flag = calculate_cagr(
        -100,
        200,
        5
    )

    assert value is None
    assert flag == "TURNAROUND"


def test_decline_to_loss():

    value, flag = calculate_cagr(
        100,
        -50,
        5
    )

    assert value is None
    assert flag == "DECLINE_TO_LOSS"


def test_both_negative():

    value, flag = calculate_cagr(
        -100,
        -20,
        5
    )

    assert value is None
    assert flag == "BOTH_NEGATIVE"


def test_zero_base():

    value, flag = calculate_cagr(
        0,
        200,
        5
    )

    assert value is None
    assert flag == "ZERO_BASE"


def test_insufficient():

    value, flag = revenue_cagr(
        [100, 150],
        5
    )

    assert value is None
    assert flag == "INSUFFICIENT"


def test_revenue_cagr():

    value, flag = revenue_cagr(
        [100, 120, 140, 160, 180, 200],
        5
    )

    assert round(value, 2) == 14.87
    assert flag == "NORMAL"


def test_pat_cagr():

    value, flag = pat_cagr(
        [50, 60, 70, 80, 90, 100],
        5
    )

    assert round(value, 2) == 14.87
    assert flag == "NORMAL"


def test_eps_cagr():

    value, flag = eps_cagr(
        [10, 12, 14, 16, 18, 20],
        5
    )

    assert round(value, 2) == 14.87
    assert flag == "NORMAL"


def test_three_year_cagr():

    value, flag = revenue_cagr(
        [100, 120, 150, 200],
        3
    )

    assert round(value, 2) == 25.99
    assert flag == "NORMAL"