from datetime import datetime

from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log
from utilities.common_methods import Methods as methods

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float, Date, String, Boolean
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name = database.name_table_overview


class Overview(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    equity_id = Column(Integer, ForeignKey(f'{database.name_table_equity}.id'))

    currency = Column(String(6), default=None)

    date = Column(Date, default=None)
    last = Column(Float, default=None)
    change_perc = Column(Float, default=None)
    market_cap = Column(Float, default=None)
    volumes = Column(Float, default=None)
    pe_ratio = Column(Float, default=None)
    macd_12_26_1d = Column(Float, default=None)
    revenue = Column(Float, default=None)
    average_vol_3m = Column(Float, default=None)
    eps = Column(Float, default=None)
    beta = Column(Float, default=None)
    dividend = Column(Float, default=None)
    dividend_yield = Column(Float, default=None)
    fifteen_minutes_sentiment = Column(String(15), default='')
    hourly_sentiment = Column(String(15), default='')
    daily_sentiment = Column(String(15), default='')
    weekly_sentiment = Column(String(15), default='')
    monthly_sentiment = Column(String(15), default='')
    daily_return = Column(Float, default=None)
    one_week_return = Column(Float, default=None)
    one_month_return = Column(Float, default=None)
    ytd_return = Column(Float, default=None)
    one_year_return = Column(Float, default=None)
    three_years_return = Column(Float, default=None)
    one_year_change = Column(Float, default=None)
    dividend_yield_perc = Column(Float, default=None)
    pe_ratio_ttm = Column(Float, default=None)
    price_to_sales_ttm = Column(Float, default=None)
    price_to_cash_flow_mrq = Column(Float, default=None)
    price_to_free_cash_flow_ttm = Column(Float, default=None)
    price_to_book_mrq = Column(Float, default=None)
    price_to_tangible_book_mrq = Column(Float, default=None)
    eps_mrq_vs_qtr_1_yr_ago = Column(Float, default=None)
    eps_ttm_vs_ttm_1_yr_ago = Column(Float, default=None)
    five_year_eps_growth = Column(Float, default=None)
    sales_mrq_vs_qtr_1_yr_ago = Column(Float, default=None)
    sales_ttm_vs_ttm_1_yr_ago_ttm = Column(Float, default=None)
    five_year_sales_growth = Column(Float, default=None)
    five_year_capital_spending_growth = Column(Float, default=None)
    asset_turnover_ttm = Column(Float, default=None)
    inventory_turnover_ttm = Column(Float, default=None)
    revenue_employee_ttm = Column(Float, default=None)
    net_income_employee_ttm = Column(Float, default=None)
    receivable_turnover_ttm = Column(Float, default=None)
    fiftytwo_wk_range_high = Column(Float, default=None)
    fiftytwo_wk_range_low = Column(Float, default=None)
    perc_change_from_52_wk_high = Column(Float, default=None)
    perc_change_from_52_wk_low = Column(Float, default=None)
    previous_month_perc_change = Column(Float, default=None)
    gross_margin_ttm = Column(Float, default=None)
    gross_margin_5ya = Column(Float, default=None)
    operating_margin_ttm = Column(Float, default=None)
    operating_margin_5ya = Column(Float, default=None)
    pretax_margin_ttm = Column(Float, default=None)
    pretax_margin_5ya = Column(Float, default=None)
    net_profit_margin_ttm = Column(Float, default=None)
    net_profit_margin_5ya = Column(Float, default=None)
    quick_ratio_mrq = Column(Float, default=None)
    current_ratio_mrq = Column(Float, default=None)
    lt_debt_to_equity_mrq = Column(Float, default=None)
    total_debt_to_equity = Column(Float, default=None)
    dividend_yield_5_year_avg = Column(Float, default=None)
    dividend_growth_rate = Column(Float, default=None)
    payout_ratio = Column(Float, default=None)
    adx_14_1d = Column(Float, default=None)
    atr_14_1d = Column(Float, default=None)
    bull_bear_power_13_1d = Column(Float, default=None)
    cci_14_1d = Column(Float, default=None)
    highs_lows_14_1d = Column(Float, default=None)
    roc_1d = Column(Float, default=None)
    rsi_14_1d = Column(Float, default=None)
    stoch_14_1d = Column(Float, default=None)
    stochrsi_14_1d = Column(Float, default=None)
    ultimate_oscillator_14_1d = Column(Float, default=None)
    williams_perc_R_1d = Column(Float, default=None)

    shares_outstanding = Column(Float, default=None)
    next_earnings_date = Column(Date, default=None)

    valuable_company = Column(Boolean, default=0, nullable=False)
    intrinsic_value = Column(Float, default=None)

    equity = relationship(u'Equity', back_populates=f'{table_name}')
    item_overview = relationship("ItemOverview", back_populates=f'{table_name}', cascade='all, delete-orphan')


    def __repr__(self):
        return f"<Overview of asset with id {self.equity_id}>"


def add_single_element(overview, field, value):
    try:
        if overview is None:
            raise Exception("Overview is none there is something wrong here")

        if "Date" == field:
            overview.date = value
        elif "Last" == field:
            value = methods.convert_to_float(value)
            overview.last = value
        elif "Currency" == field:
            overview.currency = value
        elif "Chg. %" == field:
            value = methods.convert_to_float(value)
            overview.change_perc = value
        elif "Market Cap" == field:
            value = methods.convert_to_float(value)
            overview.market_cap = value
        elif "Vol." == field:
            value = methods.convert_to_float(value)
            overview.volumes = value
        elif "P/E Ratio" == field:
            value = methods.convert_to_float(value)
            overview.pe_ratio = value
        elif "MACD (12,26 / 1D)" == field:
            value = methods.convert_to_float(value)
            overview.macd_12_26_1d = value
        elif "Revenue" == field:
            value = methods.convert_to_float(value)
            overview.revenue = value
        elif "Average Vol. (3m)" == field:
            value = methods.convert_to_float(value)
            overview.average_vol_3m = value
        elif "EPS" == field:
            value = methods.convert_to_float(value)
            overview.eps = value
        elif "Beta" == field:
            value = methods.convert_to_float(value)
            overview.beta = value
        elif "Dividend" == field:
            value = methods.convert_to_float(value)
            overview.dividend = value
        elif "Yield" == field:
            value = methods.convert_to_float(value)
            overview.dividend_yield = value
        elif "15 Minutes" == field:
            overview.fifteen_minutes_sentiment = value
        elif "Hourly" == field:
            overview.hourly_sentiment = value
        elif "Daily" == field:
            try:
                float(value)
                value = methods.convert_to_float(value)
                overview.daily_return = value
            except ValueError:
                overview.daily_sentiment = value
        elif "Weekly" == field:
            overview.weekly_sentiment = value
        elif "Monthly" == field:
            overview.monthly_sentiment = value
        elif "1 Week" == field:
            value = methods.convert_to_float(value)
            overview.one_week_return = value
        elif "1 Month" == field:
            value = methods.convert_to_float(value)
            overview.one_month_return = value
        elif "YTD" == field:
            value = methods.convert_to_float(value)
            overview.ytd_return = value
        elif "1 Year" == field:
            value = methods.convert_to_float(value)
            overview.one_year_return = value
        elif "3 Years" == field:
            value = methods.convert_to_float(value)
            overview.three_years_return = value
        elif "1-Year Change" == field:
            value = methods.convert_to_float(value)
            overview.one_year_change = value
        elif "Dividend Yield (%)" == field:
            value = methods.convert_to_float(value)
            overview.dividend_yield_perc = value
        elif "P/E Ratio (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.pe_ratio_ttm = value
        elif "Price to Sales (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.price_to_sales_ttm = value
        elif "Price to Cash Flow (MRQ)" == field:
            value = methods.convert_to_float(value)
            overview.price_to_cash_flow_mrq = value
        elif "Price to Free Cash Flow (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.price_to_free_cash_flow_ttm = value
        elif "Price to Book (MRQ)" == field:
            value = methods.convert_to_float(value)
            overview.price_to_book_mrq = value
        elif "Price to Tangible Book (MRQ)" == field:
            value = methods.convert_to_float(value)
            overview.price_to_tangible_book_mrq = value
        elif "EPS(MRQ) vs Qtr. 1 Yr. Ago" == field:
            value = methods.convert_to_float(value)
            overview.eps_mrq_vs_qtr_1_yr_ago = value
        elif "EPS(TTM) vs TTM 1 Yr. Ago" == field:
            value = methods.convert_to_float(value)
            overview.eps_ttm_vs_ttm_1_yr_ago = value
        elif "5 Year EPS Growth" == field:
            value = methods.convert_to_float(value)
            overview.five_year_eps_growth = value
        elif "Sales (MRQ) vs Qtr. 1 Yr. Ago" == field:
            value = methods.convert_to_float(value)
            overview.sales_mrq_vs_qtr_1_yr_ago = value
        elif "Sales (TTM) vs TTM 1 Yr. Ago (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.sales_ttm_vs_ttm_1_yr_ago_ttm = value
        elif "5 Year Sales Growth" == field:
            value = methods.convert_to_float(value)
            overview.five_year_sales_growth = value
        elif "5 Year Capital Spending Growth" == field:
            value = methods.convert_to_float(value)
            overview.five_year_capital_spending_growth = value
        elif "Asset Turnover (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.asset_turnover_ttm = value
        elif "Inventory Turnover (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.inventory_turnover_ttm = value
        elif "Revenue/Employee (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.revenue_employee_ttm = value
        elif "Net Income/Employee (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.net_income_employee_ttm = value
        elif "Receivable Turnover (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.receivable_turnover_ttm = value
        elif "52 wk Range - High" == field:
            value = methods.convert_to_float(value)
            overview.fiftytwo_wk_range_high = value
        elif "52 wk Range - Low" == field:
            value = methods.convert_to_float(value)
            overview.fiftytwo_wk_range_low = value
        elif "% Change from 52 wk High" == field:
            value = methods.convert_to_float(value)
            overview.perc_change_from_52_wk_high = value
        elif "% Change from 52 wk Low" == field:
            value = methods.convert_to_float(value)
            overview.perc_change_from_52_wk_low = value
        elif "Previous Month % Change" == field:
            value = methods.convert_to_float(value)
            overview.previous_month_perc_change = value
        elif "Gross margin (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.gross_margin_ttm = value
        elif "Gross Margin (5YA)" == field:
            value = methods.convert_to_float(value)
            overview.gross_margin_5ya = value
        elif "Operating margin (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.operating_margin_ttm = value
        elif "Operating margin (5YA)" == field:
            value = methods.convert_to_float(value)
            overview.operating_margin_5ya = value
        elif "Pretax margin (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.pretax_margin_ttm = value
        elif "Pretax margin (5YA)" == field:
            value = methods.convert_to_float(value)
            overview.pretax_margin_5ya = value
        elif "Net Profit margin (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.net_profit_margin_ttm = value
        elif "Net Profit margin (5YA)" == field:
            value = methods.convert_to_float(value)
            overview.net_profit_margin_5ya = value
        elif "Quick Ratio (MRQ)" == field:
            value = methods.convert_to_float(value)
            overview.quick_ratio_mrq = value
        elif "Current Ratio (MRQ)" == field:
            value = methods.convert_to_float(value)
            overview.current_ratio_mrq = value
        elif "LT Debt to Equity (MRQ)" == field:
            value = methods.convert_to_float(value)
            overview.lt_debt_to_equity_mrq = value
        elif "Total Debt to Equity" == field:
            value = methods.convert_to_float(value)
            overview.total_debt_to_equity = value
        elif "Dividend Yield 5 Year Avg. (5YA)" == field:
            value = methods.convert_to_float(value)
            overview.dividend_yield_5_year_avg = value
        elif "Dividend Growth Rate (ANN)" == field:
            value = methods.convert_to_float(value)
            overview.dividend_growth_rate = value
        elif "Payout Ratio (TTM)" == field:
            value = methods.convert_to_float(value)
            overview.payout_ratio = value
        elif "ADX (14 / 1D)" == field:
            value = methods.convert_to_float(value)
            overview.adx_14_1d = value
        elif "ATR (14 / 1D)" == field:
            value = methods.convert_to_float(value)
            overview.atr_14_1d = value
        elif "Bull/Bear Power (13 / 1D)" == field:
            value = methods.convert_to_float(value)
            overview.bull_bear_power_13_1d = value
        elif "CCI (14 / 1D)" == field:
            value = methods.convert_to_float(value)
            overview.cci_14_1d = value
        elif "Highs/Lows (14 / 1D)" == field:
            value = methods.convert_to_float(value)
            overview.highs_lows_14_1d = value
        elif "ROC (1D)" == field:
            value = methods.convert_to_float(value)
            overview.roc_1d = value
        elif "RSI (14 / 1D)" == field:
            value = methods.convert_to_float(value)
            overview.rsi_14_1d = value
        elif "STOCH (14 / 1D)" == field:
            value = methods.convert_to_float(value)
            overview.stoch_14_1d = value
        elif "STOCHRSI (14 / 1D)" == field:
            value = methods.convert_to_float(value)
            overview.stochrsi_14_1d = value
        elif "Ultimate Oscillator (14 /1D)" == field:
            value = methods.convert_to_float(value)
            overview.ultimate_oscillator_14_1d = value
        elif "Williams %R (1D)" == field:
            value = methods.convert_to_float(value)
            overview.williams_perc_R_1d = value
        elif "Shares Outstanding" == field:
            value = methods.convert_to_float(value)
            overview.shares_outstanding = value
        elif "Next Earnings Date" == field:
            value = datetime.strptime(value, '%b %d, %Y').date()
            overview.next_earnings_date = value

        else:
            log.info(f"Could not find the following field {field}")

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
        raise
