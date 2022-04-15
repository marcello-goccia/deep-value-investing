
from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float, String, Date, Enum
from data_storing.assets.common import Timespan, MeasureUnit
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name = database.name_table_income_statement


class IncomeStatement(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    equity_id = Column(Integer)
    period_length = Column(Enum(Timespan), default=None)
    period_ending = Column(Date, default=None)
    currency = Column(String(6), default='')

    measure_unit = Column(Enum(MeasureUnit), default=None)

    total_revenue = Column(Float, default=None)
    revenue = Column(Float, default=None)
    other_revenue_total = Column(Float, default=None)
    cost_of_revenue_total = Column(Float, default=None)
    gross_profit = Column(Float, default=None)
    total_operating_expenses = Column(Float, default=None)
    selling_general_admin_expenses_total = Column(Float, default=None)
    research_development = Column(Float, default=None)
    depreciation_amortization = Column(Float, default=None)
    interest_expense_income_net_operating = Column(Float, default=None)
    unusual_expense_income = Column(Float, default=None)
    other_operating_expenses_total = Column(Float, default=None)
    operating_income = Column(Float, default=None)
    interest_income_expense_net_non_operating = Column(Float, default=None)
    gain_loss_on_sale_of_assets = Column(Float, default=None)
    other_net = Column(Float, default=None)

    net_income_before_taxes = Column(Float, default=None)
    provision_for_income_taxes = Column(Float, default=None)
    net_income_after_taxes = Column(Float, default=None)
    minority_interest = Column(Float, default=None)
    equity_in_affiliates = Column(Float, default=None)
    us_gaap_adjustment = Column(Float, default=None)
    net_income_before_extraordinary_items = Column(Float, default=None)
    total_extraordinary_items = Column(Float, default=None)
    net_income = Column(Float, default=None)
    total_adjustments_to_net_income = Column(Float, default=None)
    income_available_to_common_excluding_extraordinary_items = Column(Float, default=None)
    dilution_adjustment = Column(Float, default=None)
    diluted_net_income = Column(Float, default=None)
    diluted_weighted_average_shares = Column(Float, default=None)
    diluted_eps_excluding_extraordinary_items = Column(Float, default=None)
    dps_common_stock_primary_issue = Column(Float, default=None)
    diluted_normalized_eps = Column(Float, default=None)

    # bank related
    net_interest_income = Column(Float, default=None)
    interest_income_bank = Column(Float, default=None)
    total_interest_expense = Column(Float, default=None)
    loan_loss_provision = Column(Float, default=None)
    net_interest_income_after_loan_loss_provision = Column(Float, default=None)
    non_interest_income_bank = Column(Float, default=None)
    non_interest_expense_bank = Column(Float, default=None)

    # insurance related
    total_premiums_earned = Column(Float, default=None)
    net_investment_income = Column(Float, default=None)
    losses_benefits__adjustments_total = Column(Float, default=None)
    amortization_policy_acquisition_costs = Column(Float, default=None)
    realized_gains_losses = Column(Float, default=None)

    # energy related
    fuel_expense = Column(Float, default=None)
    operations_maintenance = Column(Float, default=None)

    fundamentals_id = Column(Integer, ForeignKey(f'{database.name_table_fundamentals}.id'))
    fundamentals = relationship(u'Fundamentals', back_populates=f'{table_name}')
    item_income_statement = relationship("ItemIncomeStatement", back_populates=f'{table_name}', cascade='all, delete-orphan')


    def __repr__(self):
        return f"<{table_name}," \
            f"period_ending={self.period_ending}," \
            f"period_length={self.period_length}>"


def add_single_element(income_statement, field, value):
    """
    In order to use this method the income statement must exist and be defined.
    """
    try:
        if income_statement is None:
            return -2

        if 'Total Revenue' == field:
            income_statement.total_revenue = value
        elif 'Revenue' == field:
            income_statement.revenue = value
        elif 'Other Revenue, Total' == field:
            income_statement.other_revenue_total = value
        elif 'Cost of Revenue, Total' == field:
            income_statement.cost_of_revenue_total = value
        elif 'Gross Profit' == field:
            income_statement.gross_profit = value
        elif 'Total Operating Expenses' == field:
            income_statement.total_operating_expenses = value
        elif 'Selling/General/Admin. Expenses, Total' == field:
            income_statement.selling_general_admin_expenses_total = value
        elif 'Research & Development' == field:
            income_statement.research_development = value
        elif 'Depreciation / Amortization' == field:
            income_statement.depreciation_amortization = value
        elif 'Interest Expense (Income) - Net Operating' == field:
            income_statement.interest_expense_income_net_operating = value
        elif 'Unusual Expense (Income)' == field:
            income_statement.unusual_expense_income = value
        elif 'Other Operating Expenses, Total' == field:
            income_statement.other_operating_expenses_total = value
        elif 'Operating Income' == field:
            income_statement.operating_income = value
        elif 'Interest Income (Expense), Net Non-Operating' == field:
            income_statement.interest_income_expense_net_non_operating = value
        elif 'Gain (Loss) on Sale of Assets' == field:
            income_statement.gain_loss_on_sale_of_assets = value
        elif 'Other, Net' == field:
            income_statement.other_net = value
        elif 'Net Income Before Taxes' == field:
            income_statement.net_income_before_taxes = value
        elif 'Provision for Income Taxes' == field:
            income_statement.provision_for_income_taxes = value
        elif 'Net Income After Taxes' == field:
            income_statement.net_income_after_taxes = value
        elif 'Minority Interest' == field:
            income_statement.minority_interest = value
        elif 'Equity In Affiliates' == field:
            income_statement.equity_in_affiliates = value
        elif 'U.S GAAP Adjustment' == field:
            income_statement.us_gaap_adjustment = value
        elif 'Net Income Before Extraordinary Items' == field:
            income_statement.net_income_before_extraordinary_items = value
        elif 'Total Extraordinary Items' == field:
            income_statement.total_extraordinary_items = value
        elif 'Net Income' == field:
            income_statement.net_income = value
        elif 'Total Adjustments to Net Income' == field:
            income_statement.total_adjustments_to_net_income = value
        elif 'Income Available to Common Excluding Extraordinary Items' == field:
            income_statement.income_available_to_common_excluding_extraordinary_items = value
        elif 'Dilution Adjustment' == field:
            income_statement.dilution_adjustment = value
        elif 'Diluted Net Income' == field:
            income_statement.diluted_net_income = value
        elif 'Diluted Weighted Average Shares' == field:
            income_statement.diluted_weighted_average_shares = value
        elif 'Diluted EPS Excluding Extraordinary Items' == field:
            income_statement.diluted_eps_excluding_extraordinary_items = value
        elif 'DPS - Common Stock Primary Issue' == field:
            income_statement.dps_common_stock_primary_issue = value
        elif 'Diluted Normalized EPS' == field:
            income_statement.diluted_normalized_eps = value

        # Bank related fields
        elif 'Net Interest Income' == field:
            income_statement.net_interest_income = value
        elif 'Interest Income, Bank' == field:
            income_statement.interest_income_bank = value
        elif 'Total Interest Expense' == field:
            income_statement.total_interest_expense = value
        elif 'Loan Loss Provision' == field:
            income_statement.loan_loss_provision = value
        elif 'Net Interest Income After Loan Loss Provision' == field:
            income_statement.net_interest_income_after_loan_loss_provision = value
        elif 'Non-Interest Income, Bank' == field:
            income_statement.non_interest_income_bank = value
        elif 'Non-Interest Expense, Bank' == field:
            income_statement.non_interest_expense_bank = value

        # Insurance related fields
        elif 'Total Premiums Earned' == field:
            income_statement.total_premiums_earned = value
        elif 'Net Investment Income' == field:
            income_statement.net_investment_income = value
        elif 'Losses, Benefits and Adjustments, Total' == field:
            income_statement.losses_benefits__adjustments_total = value
        elif 'Amortization of Policy Acquisition Costs' == field:
            income_statement.amortization_policy_acquisition_costs = value
        elif 'Realized Gains (Losses)' == field:
            income_statement.realized_gains_losses = value

        # energy related
        elif 'Fuel Expense' == field:
            income_statement.fuel_expense = value
        elif 'Operations & Maintenance' == field:
            income_statement.operations_maintenance = value

        else:
            log.info(f"Could not find the following field {field}")

        return 0

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
        return -1
