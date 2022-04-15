from utilities.common_methods import Methods as methods


def get_pricing_mizrahi(equity):

    earning_per_share_historical = methods.validate(equity.fundamentals.ratios[0].year_5_eps_growth)
    compounded_desired_return = 1.15 ** 5
    if earning_per_share_historical > 0.15:
        projected_eps = 0.15 + 1
    else:
        projected_eps = 0.10 + 1

    dividend_payout_ratio = methods.validate(equity.fundamentals.ratios[0].payout_ratio)

    pe_ratio = methods.validate(equity.overview.pe_ratio)
    if pe_ratio > 20:
        projected_pe_ratio = 17
    else:
        projected_pe_ratio = 12

    current_eps = methods.validate(equity.overview.eps)
    eps_in_5y = current_eps * (projected_eps ** 5)

    total_eps_in_5y = 0
    for i in range(1, 6):
        total_eps_in_5y += current_eps * (projected_eps ** i)
    projected_dividends = total_eps_in_5y * dividend_payout_ratio

    future_stock_price_in_5y = eps_in_5y * projected_pe_ratio
    future_stock_price_in_5y += projected_dividends

    buying_price = future_stock_price_in_5y / compounded_desired_return

    return buying_price
