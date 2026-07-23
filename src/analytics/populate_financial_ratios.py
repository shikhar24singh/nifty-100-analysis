import sqlite3
from collections import defaultdict
from turtle import pd
import pandas as pnd

from src.analytics.ratios import (
    net_profit_margin,
    operating_profit_margin,
    return_on_equity,
    debt_to_equity,
    interest_coverage_ratio,
    asset_turnover,
)

from src.analytics.cashflow import (
    free_cash_flow,
)

from src.analytics.cagr import (
    revenue_cagr,
    pat_cagr,
    eps_cagr,
)


DB_PATH = "db/nifty100.db"


def get_connection():
    return sqlite3.connect(DB_PATH)


def load_profit_and_loss(cursor):

    cursor.execute("""
        SELECT *
        FROM profitandloss
        ORDER BY company_id, year
    """)

    return cursor.fetchall()


def load_balance_sheet(cursor):

    cursor.execute("""
        SELECT *
        FROM balancesheet
        ORDER BY company_id, year
    """)

    return cursor.fetchall()


def load_cashflow(cursor):

    cursor.execute("""
        SELECT *
        FROM cashflow
        ORDER BY company_id, year
    """)

    return cursor.fetchall()


def load_companies(cursor):

    cursor.execute("""
        SELECT
            id,
            face_value,
            book_value,
            roce_percentage,
            roe_percentage
        FROM companies
    """)

    rows = cursor.fetchall()

    company_dict = {}

    for row in rows:

        company_dict[row[0]] = {
            "face_value": row[1],
            "book_value": row[2],
            "roce_source": row[3],
            "roe_source": row[4]
        }

    return company_dict


def create_lookup(rows):

    lookup = {}

    for row in rows:

        company = row[1]
        year = row[2]

        lookup[(company, year)] = row

    return lookup


def build_history_dict(pl_rows):

    revenue_history = defaultdict(list)
    pat_history = defaultdict(list)
    eps_history = defaultdict(list)

    year_history = defaultdict(list)

    for row in pl_rows:

        company = row[1]
        year = row[2]

        revenue = row[3]
        pat = row[12]
        eps = row[13]

        revenue_history[company].append(revenue)
        pat_history[company].append(pat)
        eps_history[company].append(eps)

        year_history[company].append(year)

    return (
        revenue_history,
        pat_history,
        eps_history,
        year_history,
    )


def composite_score(
    roe,
    npm,
    de,
    icr,
    revenue_growth
):

    score = 0

    if roe is not None and roe >= 15:
        score += 1

    if npm is not None and npm >= 10:
        score += 1

    if de is not None and de <= 1:
        score += 1

    if icr is not None and icr >= 3:
        score += 1

    if revenue_growth is not None and revenue_growth >= 10:
        score += 1

    return score


def main():

    conn = get_connection()

    cursor = conn.cursor()

    print("Loading tables...")

    pl_rows = load_profit_and_loss(cursor)
    bs_rows = load_balance_sheet(cursor)
    cf_rows = load_cashflow(cursor)

    companies = load_companies(cursor)

    pl_lookup = create_lookup(pl_rows)
    bs_lookup = create_lookup(bs_rows)
    cf_lookup = create_lookup(cf_rows)

    (
        revenue_history,
        pat_history,
        eps_history,
        year_history,
    ) = build_history_dict(pl_rows)

    print(f"Profit & Loss rows : {len(pl_rows)}")
    print(f"Balance Sheet rows : {len(bs_rows)}")
    print(f"Cashflow rows      : {len(cf_rows)}")

    print("All tables loaded successfully.")
    print("Calculating financial ratios...")
            
    processed = 0
    log = open("output/ratio_edge_cases.log", "w")
                    
    for key, pl in pl_lookup.items():
                    
                company_id, year = key
                    
                if key not in bs_lookup:
                    continue
                    
                if key not in cf_lookup:
                    continue
                    
                bs = bs_lookup[key]
                cf = cf_lookup[key]
                    
                            
                sales = pl[3]
                operating_profit = pl[5]
                other_income = pl[7]
                interest = pl[8]
                net_profit = pl[12]
                eps = pl[13]
                dividend_payout = pl[14]
                    
                equity_capital = bs[3]
                reserves = bs[4]
                borrowings = bs[5]
                investments = bs[10]
                total_assets = bs[12]
                    
                operating_activity = cf[3]
                investing_activity = cf[4]
                    
                company_info = companies.get(company_id)
                    
                if company_info is None:
                    continue
                    
                face_value = company_info["face_value"]
                book_value = company_info["book_value"]
                roce_source = company_info["roce_source"]
                roe_source = company_info["roe_source"]
                    
                npm = net_profit_margin(
                    net_profit,
                    sales
                )
                    
                opm = operating_profit_margin(
                    operating_profit,
                    sales
                )
                    
                roe = return_on_equity(
                    
                    net_profit,
                    equity_capital,
                    reserves
                )
                if (
                    operating_profit is not None
                    and equity_capital is not None
                    and reserves is not None
                    and borrowings is not None
                ):
                    capital_employed = equity_capital + reserves + borrowings

                    if capital_employed > 0:
                        roce = round(
                            (operating_profit / capital_employed) * 100,
                            2
                        )
                    else:
                        roce = None
                else:
                    roce = None
                
                if (
                    roce is not None
                    and roce_source is not None
                    and abs(roce - roce_source) > 5
                ):
                    log.write(
                        f"{company_id} | {year} | ROCE | "
                        f"Calc={roce} | Source={roce_source}\n"
                    )
                
                if (
                    roe is not None
                    and roe_source is not None
                    and abs(roe - roe_source) > 5
                ):
                    log.write(
                        f"{company_id} | {year} | ROE | "
                        f"Calc={roe} | Source={roe_source}\n"
                    )
                    
                de_ratio = debt_to_equity(
                    borrowings,
                    equity_capital,
                    reserves
                )
                    
                icr = interest_coverage_ratio(
                    operating_profit,
                    other_income,
                    interest
                )
                    
                asset_turn = asset_turnover(
                    sales,
                    total_assets
                )
                if operating_activity is None or investing_activity is None:
                    print("=" * 60)
                    print("Missing cashflow values")
                    print("Company :", company_id)
                    print("Year    :", year)
                    print("Operating Activity :", operating_activity)
                    print("Investing Activity:", investing_activity)
                    
                if operating_activity is not None and investing_activity is not None:
                    fcf = free_cash_flow(
                        operating_activity,
                        investing_activity
                    )
                    if investing_activity is not None:
                        capex = abs(investing_activity)
                    else:
                        capex = None
                else:
                    fcf = None
                    capex = None
                    
                if face_value in (None, 0):
                    book_value_per_share = None
                else:
                    book_value_per_share = round(
                        book_value / face_value,
                        2
                    )
                    
                total_debt = borrowings
                    
                cash_from_operations = operating_activity
                    
                revenue_growth = None
                pat_growth = None
                eps_growth = None
                    
                company_years = year_history[company_id]
                    
                try:
                    
                    idx = company_years.index(year)
                    
                    if idx >= 5:
                    
                        revenue_growth, _ = revenue_cagr(
                            revenue_history[company_id][:idx + 1],
                            5
                        )
                    
                        pat_growth, _ = pat_cagr(
                            pat_history[company_id][:idx + 1],
                            5
                        )
                    
                        eps_growth, _ = eps_cagr(
                            eps_history[company_id][:idx + 1],
                            5
                        )
                    
                except ValueError:
                    pass
                    
                quality_score = composite_score(
                    roe,
                    npm,
                    de_ratio,
                    icr,
                    revenue_growth
                )
                    
                processed += 1
                cursor.execute(
                    """
                    UPDATE financial_ratios
                    SET
                        net_profit_margin_pct=?,
                        operating_profit_margin_pct=?,
                        return_on_equity_pct=?,
                        debt_to_equity=?,
                        interest_coverage=?,
                        asset_turnover=?,
                        free_cash_flow_cr=?,
                        capex_cr=?,
                        earnings_per_share=?,
                        book_value_per_share=?,
                        dividend_payout_ratio_pct=?,
                        total_debt_cr=?,
                        cash_from_operations_cr=?,
                        revenue_cagr_5yr=?,
                        pat_cagr_5yr=?,
                        eps_cagr_5yr=?,
                        composite_quality_score=?
                    WHERE company_id=? AND year=?
                    """,
                    (
                        npm,
                        opm,
                        roe,
                        de_ratio,
                        icr,
                        asset_turn,
                        fcf,
                        capex,
                        eps,
                        book_value_per_share,
                        dividend_payout,
                        total_debt,
                        cash_from_operations,
                        revenue_growth,
                        pat_growth,
                        eps_growth,
                        quality_score,
                        company_id,
                        year,
                    )
                )
                    
                if processed % 100 == 0:
                    print(f"{processed} rows updated...")
    conn.commit()

    print("-" * 50)
    print("Financial ratio population completed.")
    print(f"Rows processed : {processed}")

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM financial_ratios
        """
    )

    total_rows = cursor.fetchone()[0]

    print(f"Rows in financial_ratios : {total_rows}")

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM financial_ratios
        WHERE net_profit_margin_pct IS NOT NULL
        """
    )

    populated = cursor.fetchone()[0]

    print(f"Rows populated : {populated}")
    
    log.close()

    conn.close()

    print("Database connection closed.")


if __name__ == "__main__":
    main()