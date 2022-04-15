
from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float, String, Date, Enum
from data_storing.assets.common import Timespan, MeasureUnit
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name = database.name_table_balance_sheet


class BalanceSheet(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    equity_id = Column(Integer)

    period_length = Column(Enum(Timespan), default=None)
    period_ending = Column(Date, default=None)
    measure_unit = Column(Enum(MeasureUnit), default=None)
    currency = Column(String(6), default='')

    total_current_assets = Column(Float, default=None)
    total_assets = Column(Float, default=None)
    cash_due_from_banks = Column(Float, default=None)
    other_earning_assets_total = Column(Float, default=None)
    net_loans = Column(Float, default=None)
    property_plant_equipment_total_net = Column(Float, default=None)
    property_plant_equipment_total_gross = Column(Float, default=None)
    accumulated_depreciation_total = Column(Float, default=None)
    goodwill_net = Column(Float, default=None)
    intangibles_net = Column(Float, default=None)
    long_term_investments = Column(Float, default=None)
    other_long_term_assets_total = Column(Float, default=None)
    other_assets_total = Column(Float, default=None)
    total_current_liabilities = Column(Float, default=None)
    total_liabilities = Column(Float, default=None)
    accounts_payable = Column(Float, default=None)
    payable_accrued = Column(Float, default=None)
    accrued_expenses = Column(Float, default=None)
    total_deposits = Column(Float, default=None)
    other_bearing_liabilities_total = Column(Float, default=None)
    total_short_term_borrowings = Column(Float, default=None)
    current_port_of_lt_debt_capital_leases = Column(Float, default=None)
    other_current_liabilities_total = Column(Float, default=None)
    total_long_term_debt = Column(Float, default=None)
    long_term_debt = Column(Float, default=None)
    capital_lease_obligations = Column(Float, default=None)
    total_debt = Column(Float, default=None)
    deferred_income_tax = Column(Float, default=None)
    minority_interest = Column(Float, default=None)
    other_liabilities_total = Column(Float, default=None)
    total_equity = Column(Float, default=None)
    redeemable_preferred_stock_total = Column(Float, default=None)
    preferred_stock_non_redeemable_net = Column(Float, default=None)
    common_stock_total = Column(Float, default=None)
    additional_paid_in_capital = Column(Float, default=None)
    retained_earnings_accumulated_deficit = Column(Float, default=None)
    treasury_stock_common = Column(Float, default=None)
    esop_debt_guarantee = Column(Float, default=None)
    unrealized_gain_loss = Column(Float, default=None)
    other_equity_total = Column(Float, default=None)
    total_liabilities_shareholders_equity = Column(Float, default=None)
    total_common_shares_outstanding = Column(Float, default=None)
    total_preferred_shares_outstanding = Column(Float, default=None)

    # bank related
    cash_and_short_term_investments = Column(Float, default=None)
    cash_and_equivalents = Column(Float, default=None)
    short_term_investments = Column(Float, default=None)
    total_receivables_net = Column(Float, default=None)
    accounts_receivables_trade_net = Column(Float, default=None)
    total_inventory = Column(Float, default=None)
    other_current_assets_total = Column(Float, default=None)
    cash = Column(Float, default=None)
    prepaid_expenses = Column(Float, default=None)
    notes_payable_short_term_debt = Column(Float, default=None)

    # insurance related
    note_receivable_long_term = Column(Float, default=None)
    insurance_receivables = Column(Float, default=None)
    deferred_policy_acquisition_costs = Column(Float, default=None)
    policy_liabilities = Column(Float, default=None)

    # energy related
    total_utility_plant_net = Column(Float, default=None)

    fundamentals_id = Column(Integer, ForeignKey(f'{database.name_table_fundamentals}.id'))
    fundamentals = relationship(u'Fundamentals', back_populates=f'{table_name}')
    item_balance_sheet = relationship("ItemBalanceSheet", back_populates=f'{table_name}', cascade='all, delete-orphan')


    def __repr__(self):
        return f"<{table_name}," \
            f"period_ending={self.period_ending}," \
            f"period_length={self.period_length}>"


def add_single_element(balance_sheet, field, value):
    try:
        if balance_sheet is None:
            return -2

        if "Total Current Assets" == field:
            balance_sheet.total_current_assets = value
        elif "Total Assets" == field:
            balance_sheet.total_assets = value
        elif "Cash & Due from Banks" == field:
            balance_sheet.cash_due_from_banks = value
        elif "Other Earning Assets, Total" == field:
            balance_sheet.other_earning_assets_total = value
        elif "Net Loans" == field:
            balance_sheet.net_loans = value
        elif "Property/Plant/Equipment, Total - Net" == field:
            balance_sheet.property_plant_equipment_total_net = value
        elif "Property/Plant/Equipment, Total - Gross" == field:
            balance_sheet.property_plant_equipment_total_gross = value
        elif "Accumulated Depreciation, Total" == field:
            balance_sheet.accumulated_depreciation_total = value
        elif "Goodwill, Net" == field:
            balance_sheet.goodwill_net = value
        elif "Intangibles, Net" == field:
            balance_sheet.intangibles_net = value
        elif "Long Term Investments" == field:
            balance_sheet.long_term_investments = value
        elif "Other Long Term Assets, Total" == field:
            balance_sheet.other_long_term_assets_total = value
        elif "Other Assets, Total" == field:
            balance_sheet.other_assets_total = value
        elif "Total Current Liabilities" == field:
            balance_sheet.total_current_liabilities = value
        elif "Total Liabilities" == field:
            balance_sheet.total_liabilities = value
        elif "Accounts Payable" == field:
            balance_sheet.accounts_payable = value
        elif "Payable/Accrued" == field:
            balance_sheet.payable_accrued = value
        elif "Accrued Expenses" == field:
            balance_sheet.accrued_expenses = value
        elif "Total Deposits" == field:
            balance_sheet.total_deposits = value
        elif "Other Bearing Liabilities, Total" == field:
            balance_sheet.other_bearing_liabilities_total = value
        elif "Total Short Term Borrowings" == field:
            balance_sheet.total_short_term_borrowings = value
        elif "Current Port. of LT Debt/Capital Leases" == field:
            balance_sheet.current_port_of_lt_debt_capital_leases = value
        elif "Other Current liabilities, Total" == field:
            balance_sheet.other_current_liabilities_total = value
        elif "Total Long Term Debt" == field:
            balance_sheet.total_long_term_debt = value
        elif "Long Term Debt" == field:
            balance_sheet.long_term_debt = value
        elif "Capital Lease Obligations" == field:
            balance_sheet.capital_lease_obligations = value
        elif "Total Debt" == field:
            balance_sheet.total_debt = value
        elif "Deferred Income Tax" == field:
            balance_sheet.deferred_income_tax = value
        elif "Minority Interest" == field:
            balance_sheet.minority_interest = value
        elif "Other Liabilities, Total" == field:
            balance_sheet.other_liabilities_total = value
        elif "Total Equity" == field:
            balance_sheet.total_equity = value
        elif "Redeemable Preferred Stock, Total" == field:
            balance_sheet.redeemable_preferred_stock_total = value
        elif "Preferred Stock - Non Redeemable, Net" == field:
            balance_sheet.preferred_stock_non_redeemable_net = value
        elif "Common Stock, Total" == field:
            balance_sheet.common_stock_total = value
        elif "Additional Paid-In Capital" == field:
            balance_sheet.additional_paid_in_capital = value
        elif "Retained Earnings (Accumulated Deficit)" == field:
            balance_sheet.retained_earnings_accumulated_deficit = value
        elif "Treasury Stock - Common" == field:
            balance_sheet.treasury_stock_common = value
        elif "ESOP Debt Guarantee" == field:
            balance_sheet.esop_debt_guarantee = value
        elif "Unrealized Gain (Loss)" == field:
            balance_sheet.unrealized_gain_loss = value
        elif "Other Equity, Total" == field:
            balance_sheet.other_equity_total = value
        elif "Total Liabilities & Shareholders' Equity" == field:
            balance_sheet.total_liabilities_shareholders_equity = value
        elif "Total Common Shares Outstanding" == field:
            balance_sheet.total_common_shares_outstanding = value
        elif "Total Preferred Shares Outstanding" == field:
            balance_sheet.total_preferred_shares_outstanding = value

        # bank related
        elif "Cash and Short Term Investments" == field:
            balance_sheet.cash_and_short_term_investments = value
        elif "Cash & Equivalents" == field:
            balance_sheet.cash_and_equivalents = value
        elif "Short Term Investments" == field:
            balance_sheet.short_term_investments = value
        elif "Total Receivables, Net" == field:
            balance_sheet.total_receivables_net = value
        elif "Accounts Receivables - Trade, Net" == field:
            balance_sheet.accounts_receivables_trade_net = value
        elif "Total Inventory" == field:
            balance_sheet.total_inventory = value
        elif "Other Current Assets, Total" == field:
            balance_sheet.other_current_assets_total = value
        elif "Cash" == field:
            balance_sheet.cash = value
        elif "Prepaid Expenses" == field:
            balance_sheet.prepaid_expenses = value
        elif "Notes Payable/Short Term Debt" == field:
            balance_sheet.notes_payable_short_term_debt = value

        # insurance related
        elif "Note Receivable - Long Term" == field:
            balance_sheet.note_receivable_long_term = value
        elif "Insurance Receivables" == field:
            balance_sheet.insurance_receivables = value
        elif "Deferred Policy Acquisition Costs" == field:
            balance_sheet.deferred_policy_acquisition_costs = value
        elif "Policy Liabilities" == field:
            balance_sheet.policy_liabilities = value

        # energy related
        elif "Total Utility Plant, Net" == field:
            balance_sheet.total_utility_plant_net = value

        else:
            log.info(f"Could not find the following field {field}")

        return 0

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
        return -1
