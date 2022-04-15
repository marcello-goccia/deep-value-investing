import fundamentals.measures.free_cash_flow as fcf
import fundamentals.measures as measures


def get_pay_back_time(equity):

    free_cash_flow = fcf.get_free_cash_flow(equity)
    # free_cash_flow = fcf.get_free_cash_flow_v2(equity)
    # free_cash_flow = fcf.get_free_cash_flow_v3(equity)

    growth_estimate = measures.get_growth_estimate(equity) + 1

    compound_growth = 0
    number_of_years = 8
    for i in range(1, number_of_years + 1):
        compound_growth += growth_estimate ** i

    payback_time = free_cash_flow * compound_growth

    buying_price = payback_time / equity.overview.shares_outstanding

    return buying_price
