import pandas as pd
def free_cash_flow(
    operating_activity,
    investing_activity
):
    if pd.isna(operating_activity) or pd.isna(investing_activity):
        return None

    return operating_activity + investing_activity


def cfo_quality_score(
    cfo_history,
    pat_history
):

    if len(cfo_history) != len(pat_history):
        return None

    ratios = []

    for cfo, pat in zip(cfo_history, pat_history):

        if pat == 0:
            return None

        ratios.append(cfo / pat)

    avg_ratio = sum(ratios) / len(ratios)

    if avg_ratio > 1:
        return round(avg_ratio, 2), "High Quality"

    if avg_ratio >= 0.5:
        return round(avg_ratio, 2), "Moderate"

    return round(avg_ratio, 2), "Accrual Risk"


def capex_intensity(
    investing_activity,
    sales
):

    if sales == 0:
        return None, None

    intensity = abs(investing_activity) / sales * 100

    if intensity < 3:
        label = "Asset Light"

    elif intensity <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return round(intensity, 2), label


def fcf_conversion_rate(
    free_cash_flow,
    operating_profit
):

    if operating_profit == 0:
        return None

    return round(
        free_cash_flow / operating_profit * 100,
        2
    )


def capital_allocation_pattern(
    cfo,
    cfi,
    cff,
    cfo_pat_ratio=None
):

    cfo_sign = "+" if cfo >= 0 else "-"
    cfi_sign = "+" if cfi >= 0 else "-"
    cff_sign = "+" if cff >= 0 else "-"

    pattern = (cfo_sign, cfi_sign, cff_sign)

    if pattern == ("+", "-", "-"):

        if cfo_pat_ratio is not None and cfo_pat_ratio > 1:
            label = "Shareholder Returns"
        else:
            label = "Reinvestor"

    elif pattern == ("+", "+", "-"):
        label = "Liquidating Assets"

    elif pattern == ("-", "+", "+"):
        label = "Distress Signal"

    elif pattern == ("-", "-", "+"):
        label = "Growth Funded by Debt"

    elif pattern == ("+", "+", "+"):
        label = "Cash Accumulator"

    elif pattern == ("-", "-", "-"):
        label = "Pre-Revenue"

    elif pattern == ("+", "-", "+"):
        label = "Mixed"

    else:
        label = "Unknown"

    return {
        "cfo_sign": cfo_sign,
        "cfi_sign": cfi_sign,
        "cff_sign": cff_sign,
        "pattern_label": label
    }