# Sprint 2 Retrospective

## Formula Decisions

- ROE = Net Profit / (Equity + Reserves)
- ROCE = Operating Profit / Capital Employed
- EPS = Net Profit / Shares Outstanding
- Debt-to-Equity = Borrowings / Net Worth
- Asset Turnover = Revenue / Total Assets

## Edge Cases

- Missing cashflow values produce NULL Free Cash Flow.
- Negative reserves can produce unusual ROE.
- Small capital employed inflates ROCE.
- Historical ratios differ from companies.xlsx snapshot values.
- Financial companies require special interpretation of leverage metrics.

## Improvements

- Compare only latest year during validation.
- Add sector-specific validation rules.
- Improve duplicate detection.