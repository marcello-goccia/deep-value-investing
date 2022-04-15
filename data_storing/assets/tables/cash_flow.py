
from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float, String, Date, Enum
from data_storing.assets.common import Timespan, MeasureUnit
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name = database.name_table_cash_flow


class CashFlow(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    equity_id = Column(Integer)
    period_length = Column(Enum(Timespan), default=None)
    period_ending = Column(Date, default=None)
    measure_unit = Column(Enum(MeasureUnit), default=None)
    currency = Column(String(6), default='')
    time_span = Column(String(12), default='')

    net_income_starting_line = Column(Float, default=None)
    cash_from_operating_activities = Column(Float, default=None)
    depreciation_depletion = Column(Float, default=None)
    amortization = Column(Float, default=None)
    deferred_taxes = Column(Float, default=None)
    non_cash_items = Column(Float, default=None)
    cash_receipts = Column(Float, default=None)
    cash_payments = Column(Float, default=None)
    cash_taxes_paid = Column(Float, default=None)
    cash_interest_paid = Column(Float, default=None)
    changes_in_working_capital = Column(Float, default=None)
    cash_from_investing_activities = Column(Float, default=None)
    capital_expenditures = Column(Float, default=None)
    other_investing_cash_flow_items_total = Column(Float, default=None)
    cash_from_financing_activities = Column(Float, default=None)
    financing_cash_flow_items = Column(Float, default=None)
    total_cash_dividends_paid = Column(Float, default=None)
    issuance_retirement_of_stock_net = Column(Float, default=None)
    issuance_retirement_of_debt_net = Column(Float, default=None)
    foreign_exchange_effects = Column(Float, default=None)
    net_change_in_cash = Column(Float, default=None)

    fundamentals_id = Column(Integer, ForeignKey(f'{database.name_table_fundamentals}.id'))
    fundamentals = relationship(u'Fundamentals', back_populates=f'{table_name}')
    item_cash_flow = relationship("ItemCashFlow", back_populates=f'{table_name}', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<{table_name}," \
            f"period_ending={self.period_ending}," \
            f"period_length={self.period_length}>"


def add_single_element(cash_flow, field, value):
    try:
        if cash_flow is None:
            raise Exception("Cash flow is None, there is something wrong here!")

        if "Period Length:" == field:
            cash_flow.time_span = value
        elif "Net Income/Starting Line" == field:
            cash_flow.net_income_starting_line = value
        elif "Cash From Operating Activities" == field:
            cash_flow.cash_from_operating_activities = value
        elif "Depreciation/Depletion" == field:
            cash_flow.depreciation_depletion = value
        elif "Amortization" == field:
            cash_flow.amortization = value
        elif "Deferred Taxes" == field:
            cash_flow.deferred_taxes = value
        elif "Non-Cash Items" == field:
            cash_flow.non_cash_items = value
        elif "Cash Receipts" == field:
            cash_flow.cash_receipts = value
        elif "Cash Payments" == field:
            cash_flow.cash_payments = value
        elif "Cash Taxes Paid" == field:
            cash_flow.cash_taxes_paid = value
        elif "Cash Interest Paid" == field:
            cash_flow.cash_interest_paid = value
        elif "Changes in Working Capital" == field:
            cash_flow.changes_in_working_capital = value
        elif "Cash From Investing Activities" == field:
            cash_flow.cash_from_investing_activities = value
        elif "Capital Expenditures" == field:
            cash_flow.capital_expenditures = value
        elif "Other Investing Cash Flow Items, Total" == field:
            cash_flow.other_investing_cash_flow_items_total = value
        elif "Cash From Financing Activities" == field:
            cash_flow.cash_from_financing_activities = value
        elif "Financing Cash Flow Items" == field:
            cash_flow.financing_cash_flow_items = value
        elif "Total Cash Dividends Paid" == field:
            cash_flow.total_cash_dividends_paid = value
        elif "Issuance (Retirement) of Stock, Net" == field:
            cash_flow.issuance_retirement_of_stock_net = value
        elif "Issuance (Retirement) of Debt, Net" == field:
            cash_flow.issuance_retirement_of_debt_net = value
        elif "Foreign Exchange Effects" == field:
            cash_flow.foreign_exchange_effects = value
        elif "Net Change in Cash" == field:
            cash_flow.net_change_in_cash = value

        # bank related
        # insurance related

        else:
            log.info(f"Could not find the following field {field}")

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
        raise
