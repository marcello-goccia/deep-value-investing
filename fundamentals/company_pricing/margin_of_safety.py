import fundamentals.measures as measures
from utilities.common_methods import Methods as methods


def get_margin_of_safety(equity):

    earning_per_share = methods.validate(equity.overview.eps)
    windage_growth = measures.get_growth_estimate(equity) + 1
    pe_ratio = methods.validate(equity.overview.pe_ratio)
    windage_price_to_earning = min((2 * (windage_growth - 1) * 100), pe_ratio)
    minimum_acceptable_rate_return = 0.15 + 1

    future_10y_eps = earning_per_share * (windage_growth ** 10)
    future_10y_share_price = future_10y_eps * windage_price_to_earning
    sticker_price = future_10y_share_price / (minimum_acceptable_rate_return ** 10)

    buying_price = sticker_price / 2

    return buying_price
