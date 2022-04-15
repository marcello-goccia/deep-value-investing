
from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float, DECIMAL, Date, Enum
from sqlalchemy.orm import relationship

from data_storing.assets.base import Base
from data_storing.assets.common import Benchmark

table_name = database.name_table_ratios


class Ratios(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    equity_id = Column(Integer)
    current_period = Column(Date, default=None)
    benchmark = Column(Enum(Benchmark), default=None)

    # Decimals are constructed in this way: (p,s) p = total number of digits, s = digits at right of decimal point.

    # Valuation Ratios
    pe_ratio_ttm = Column(Float, default=None)
    price_to_sales_ttm = Column(Float, default=None)
    price_to_cash_flow_mrq = Column(Float, default=None)
    price_to_free_cash_flow_ttm = Column(Float, default=None)
    price_to_book_mrq = Column(Float, default=None)
    price_to_tangible_book_mrq = Column(Float, default=None)

    # Profitability
    gross_margin_ttm = Column(Float, default=None)  # %
    gross_margin_5ya = Column(Float, default=None) # %
    operating_margin_ttm = Column(Float, default=None)  # %
    operating_margin_5ya = Column(Float, default=None)  # %
    pretax_margin_ttm = Column(Float, default=None)  # %
    pretax_margin_5ya = Column(Float, default=None)  # %
    net_profit_margin_ttm = Column(Float, default=None)  # %
    net_profit_margin_5ya = Column(Float, default=None)  # %

    # Per Share Data
    revenue_share_ttm = Column(Float, default=None)
    basic_eps = Column(Float, default=None)
    diluted_eps = Column(Float, default=None)
    book_value_share_mrq = Column(Float, default=None)
    tangible_book_value_share_mrq = Column(Float, default=None)
    cash_share_mrq = Column(Float, default=None)
    cash_flow_share_ttm = Column(Float, default=None)

    # Management Effectiveness
    return_on_equity_ttm = Column(Float, default=None)  # %
    return_on_equity_5ya = Column(Float, default=None)  # %
    return_on_assets_ttm = Column(Float, default=None)  # %
    return_on_assets_5ya = Column(Float, default=None)  # %
    return_on_investment_ttm = Column(Float, default=None)  # %
    return_on_investment_5ya = Column(Float, default=None)  # %

    # Growth
    eps_mrq_vs_qtr_1_yr_ago = Column(Float, default=None)  # %
    eps_ttm_vs_ttm_1_yr_ago = Column(Float, default=None)  # %
    year_5_eps_growth = Column(Float, default=None)  # %
    sales_mrq_vs_qtr_1_yr_ago = Column(Float, default=None)  # %
    sales_ttm_vs_ttm_1_yr_ago = Column(Float, default=None)  # %
    year_5_sales_growth = Column(Float, default=None)  # %
    year_5_capital_spending_growth = Column(Float, default=None)  # %

    # Financial Strength
    quick_ratio_mrq = Column(Float, default=None)
    current_ratio_mrq = Column(Float, default=None)
    lt_debt_to_equity_mrq = Column(Float, default=None)
    total_debt_to_equity_mrq = Column(Float, default=None)

    # Efficiency
    asset_turnover_ttm = Column(Float, default=None)
    inventory_turnover_ttm = Column(Float, default=None)
    revenue_employee_ttm = Column(Float, default=None)
    net_income_employee_ttm = Column(Float, default=None)
    receivable_turnover_ttm = Column(Float, default=None)

    # Dividend
    dividend_yield = Column(Float, default=None)  # %
    dividend_yield_5_year_avg = Column(Float, default=None)  # %
    dividend_growth_rate = Column(Float, default=None)  # %
    payout_ratio = Column(Float, default=None)

    fundamentals_id = Column(Integer, ForeignKey(f'{database.name_table_fundamentals}.id'))
    fundamentals = relationship(u'Fundamentals', back_populates=f'{table_name}')
    item_ratios = relationship("ItemRatios", back_populates=f'{table_name}', cascade='all, delete-orphan')

    def __repr__(self):
        date = self.current_period.strftime("%Y-%m")
        return f"<{table_name}, current_period={date}, benchmark={self.benchmark}>"


def add_single_element(ratios, field, value):
    try:
        if ratios is None:
            return -2

        # Valuation Ratios
        if "P/E Ratio TTM" in field:
            ratios.pe_ratio_ttm = value
        elif "Price to Sales TTM" in field:
            ratios.price_to_sales_ttm = value
        elif "Price to Cash Flow MRQ" in field:
            ratios.price_to_cash_flow_mrq = value
        elif "Price to Free Cash Flow TTM" in field:
            ratios.price_to_free_cash_flow_ttm = value
        elif "Price to Book MRQ" in field:
            ratios.price_to_book_mrq = value
        elif "Price to Tangible Book MRQ" in field:
            ratios.price_to_tangible_book_mrq = value

        # Profitability
        elif "Gross margin TTM" in field:
            ratios.gross_margin_ttm = value
        elif "Gross Margin 5YA" in field:
            ratios.gross_margin_5ya = value
        elif "Operating margin TTM" in field:
            ratios.operating_margin_ttm = value
        elif "Operating margin 5YA" in field:
            ratios.operating_margin_5ya = value
        elif "Pretax margin TTM" in field:
            ratios.pretax_margin_ttm = value
        elif "Pretax margin 5YA" in field:
            ratios.pretax_margin_5ya = value
        elif "Net Profit margin TTM" in field:
            ratios.net_profit_margin_ttm = value
        elif "Net Profit margin 5YA" in field:
            ratios.net_profit_margin_5ya = value

        # Per Share Data
        elif "Revenue/Share TTM" in field:
            ratios.revenue_share_ttm = value
        elif "Basic EPS" in field:
            ratios.basic_eps = value
        elif "Diluted EPS" in field:
            ratios.diluted_eps = value
        elif "Book Value/Share MRQ" in field:
            ratios.book_value_share_mrq = value
        elif "Tangible Book Value/Share MRQ" in field:
            ratios.tangible_book_value_share_mrq = value
        elif "Cash/Share MRQ" in field:
            ratios.cash_share_mrq = value
        elif "Cash Flow/Share TTM" in field:
            ratios.cash_flow_share_ttm = value

        # Management Effectiveness
        elif "Return on Equity TTM" in field:
            ratios.return_on_equity_ttm = value
        elif "Return on Equity 5YA" in field:
            ratios.return_on_equity_5ya = value
        elif "Return on Assets TTM" in field:
            ratios.return_on_assets_ttm = value
        elif "Return on Assets 5YA" in field:
            ratios.return_on_assets_5ya = value
        elif "Return on Investment TTM" in field:
            ratios.return_on_investment_ttm = value
        elif "Return on Investment 5YA" in field:
            ratios.return_on_investment_5ya = value

        # Growth
        elif "EPS(MRQ) vs Qtr. 1 Yr. Ago" in field:
            ratios.eps_mrq_vs_qtr_1_yr_ago = value
        elif "EPS(TTM) vs TTM 1 Yr. Ago" in field:
            ratios.eps_ttm_vs_ttm_1_yr_ago = value
        elif "5 Year EPS Growth" in field:
            ratios.year_5_eps_growth = value
        elif "Sales (MRQ) vs Qtr. 1 Yr. Ago" in field:
            ratios.sales_mrq_vs_qtr_1_yr_ago = value
        elif "Sales (TTM) vs TTM 1 Yr. Ago" in field:
            ratios.sales_ttm_vs_ttm_1_yr_ago = value
        elif "5 Year Sales Growth" in field:
            ratios.year_5_sales_growth = value
        elif "5 Year Capital Spending Growth" in field:
            ratios.year_5_capital_spending_growth = value

        # Financial Strength
        elif "Quick Ratio MRQ" in field:
            ratios.quick_ratio_mrq = value
        elif "Current Ratio MRQ" in field:
            ratios.current_ratio_mrq = value
        elif "LT Debt to Equity MRQ" in field:
            ratios.lt_debt_to_equity_mrq = value
        elif "Total Debt to Equity MRQ" in field:
            ratios.total_debt_to_equity_mrq = value

        # Efficiency
        elif "Asset Turnover TTM" in field:
            ratios.asset_turnover_ttm = value
        elif "Inventory Turnover TTM" in field:
            ratios.inventory_turnover_ttm = value
        elif "Revenue/Employee TTM" in field:
            ratios.revenue_employee_ttm = value
        elif "Net Income/Employee TTM" in field:
            ratios.net_income_employee_ttm = value
        elif "Receivable Turnover TTM" in field:
            ratios.receivable_turnover_ttm = value

        # Dividend
        elif "Dividend Yield" in field:
            ratios.dividend_yield = value
        elif "Dividend Yield 5 Year Avg" in field:
            ratios.dividend_yield_5_year_avg = value
        elif "Dividend Growth Rate" in field:
            ratios.dividend_growth_rate = value
        elif "Payout Ratio" in field:
            ratios.payout_ratio = value

        else:
            log.info(f"Could not find the following field {field}")

        return 0

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
        return -1
