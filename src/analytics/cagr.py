def calculate_cagr(start_value, end_value, years):

    if years <= 0:
        return None, "INSUFFICIENT"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value > 0:

        cagr = (
            ((end_value / start_value) ** (1 / years) - 1)
            * 100
        )

        return round(cagr, 2), "NORMAL"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "UNKNOWN"


def revenue_cagr(history, years):

    if len(history) < years + 1:
        return None, "INSUFFICIENT"

    start = history[-(years + 1)]
    end = history[-1]

    return calculate_cagr(
        start,
        end,
        years
    )


def pat_cagr(history, years):

    if len(history) < years + 1:
        return None, "INSUFFICIENT"

    start = history[-(years + 1)]
    end = history[-1]

    return calculate_cagr(
        start,
        end,
        years
    )


def eps_cagr(history, years):

    if len(history) < years + 1:
        return None, "INSUFFICIENT"

    start = history[-(years + 1)]
    end = history[-1]

    return calculate_cagr(
        start,
        end,
        years
    )