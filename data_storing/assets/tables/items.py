
from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float, Date, String
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name_item_equity = database.name_table_item_equity
table_name_item_overview = database.name_table_item_overview
table_name_item_income_statement = database.name_table_item_income_statement
table_name_item_balance_sheet = database.name_table_item_balance_sheet
table_name_item_cash_flow = database.name_table_item_cash_flow
table_name_item_ratios = database.name_table_item_ratios
table_name_item_dividends = database.name_table_item_dividends
table_name_item_earnings = database.name_table_item_earnings
table_name_item_prices = database.name_table_item_prices


class ItemEquity(Base):
    __tablename__ = table_name_item_equity

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    equity_id = Column(Integer, ForeignKey(f'{database.name_table_equity}.id'))
    equity = relationship(u'Equity', back_populates=f'{table_name_item_equity}')

    field = Column(String(20), default=None)        # the name of the variable
    type = Column(String(10), default=None)         # the type of the variable (string, date, float, integer, etc.)
    value_flt = Column(Float, default=None)         # the value of the variable if it is a float
    value_str = Column(String(50), default=None)    # the value of the variable if it is not a float

    def __repr__(self):
        return f"<{table_name_item_equity}, {self.field}: {self.type}>"


class ItemOverview(Base):
    __tablename__ = table_name_item_overview

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    overview_id = Column(Integer, ForeignKey(f'{database.name_table_overview}.id'))
    overview = relationship(u'Overview', back_populates=f'{table_name_item_overview}')

    field = Column(String(20), default=None)        # the name of the variable
    type = Column(String(10), default=None)         # the type of the variable (string, date, float, integer, etc.)
    value_flt = Column(Float, default=None)         # the value of the variable if it is a float
    value_str = Column(String(50), default=None)    # the value of the variable if it is not a float

    def __repr__(self):
        return f"<{table_name_item_overview}, {self.field}: {self.type}>"


class ItemIncomeStatement(Base):
    __tablename__ = table_name_item_income_statement

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    income_statement_id = Column(Integer, ForeignKey(f'{database.name_table_income_statement}.id'))
    income_statement = relationship(u'IncomeStatement', back_populates=f'{table_name_item_income_statement}')

    field = Column(String(20), default=None)        # the name of the variable
    type = Column(String(10), default=None)         # the type of the variable (string, date, float, integer, etc.)
    value_flt = Column(Float, default=None)         # the value of the variable if it is a float
    value_str = Column(String(50), default=None)    # the value of the variable if it is not a float

    def __repr__(self):
        return f"<{table_name_item_income_statement}, {self.field}: {self.type}>"


class ItemBalanceSheet(Base):
    __tablename__ = table_name_item_balance_sheet

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    balance_sheet_id = Column(Integer, ForeignKey(f'{database.name_table_balance_sheet}.id'))
    balance_sheet = relationship(u'BalanceSheet', back_populates=f'{table_name_item_balance_sheet}')

    field = Column(String(20), default=None)        # the name of the variable
    type = Column(String(10), default=None)         # the type of the variable (string, date, float, integer, etc.)
    value_flt = Column(Float, default=None)         # the value of the variable if it is a float
    value_str = Column(String(50), default=None)    # the value of the variable if it is not a float

    def __repr__(self):
        return f"<{table_name_item_balance_sheet}, {self.field}: {self.type}>"


class ItemCashFlow(Base):
    __tablename__ = table_name_item_cash_flow

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    cash_flow_id = Column(Integer, ForeignKey(f'{database.name_table_cash_flow}.id'))
    cash_flow = relationship(u'CashFlow', back_populates=f'{table_name_item_cash_flow}')

    field = Column(String(20), default=None)        # the name of the variable
    type = Column(String(10), default=None)         # the type of the variable (string, date, float, integer, etc.)
    value_flt = Column(Float, default=None)         # the value of the variable if it is a float
    value_str = Column(String(50), default=None)    # the value of the variable if it is not a float

    def __repr__(self):
        return f"<{table_name_item_cash_flow}, {self.field}: {self.type}>"


class ItemRatios(Base):
    __tablename__ = table_name_item_ratios

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    ratios_id = Column(Integer, ForeignKey(f'{database.name_table_ratios}.id'))
    ratios = relationship(u'Ratios', back_populates=f'{table_name_item_ratios}')

    field = Column(String(20), default=None)        # the name of the variable
    type = Column(String(10), default=None)         # the type of the variable (string, date, float, integer, etc.)
    value_flt = Column(Float, default=None)         # the value of the variable if it is a float
    value_str = Column(String(50), default=None)    # the value of the variable if it is not a float

    def __repr__(self):
        return f"<{table_name_item_ratios}, {self.field}: {self.type}>"


class ItemDividends(Base):
    __tablename__ = table_name_item_dividends

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    dividends_id = Column(Integer, ForeignKey(f'{database.name_table_dividends}.id'))
    dividends = relationship(u'Dividends', back_populates=f'{table_name_item_dividends}')

    field = Column(String(20), default=None)        # the name of the variable
    type = Column(String(10), default=None)         # the type of the variable (string, date, float, integer, etc.)
    value_flt = Column(Float, default=None)         # the value of the variable if it is a float
    value_str = Column(String(50), default=None)    # the value of the variable if it is not a float

    def __repr__(self):
        return f"<{table_name_item_dividends}, {self.field}: {self.type}>"


class ItemEarnings(Base):
    __tablename__ = table_name_item_earnings

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    earnings_id = Column(Integer, ForeignKey(f'{database.name_table_earnings}.id'))
    earnings = relationship(u'Earnings', back_populates=f'{table_name_item_earnings}')

    field = Column(String(20), default=None)        # the name of the variable
    type = Column(String(10), default=None)         # the type of the variable (string, date, float, integer, etc.)
    value_flt = Column(Float, default=None)         # the value of the variable if it is a float
    value_str = Column(String(50), default=None)    # the value of the variable if it is not a float

    def __repr__(self):
        return f"<{table_name_item_earnings}, {self.field}: {self.type}>"


class ItemPrices(Base):
    __tablename__ = table_name_item_prices

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    prices_id = Column(Integer, ForeignKey(f'{database.name_table_prices}.id'))
    prices = relationship(u'Prices', back_populates=f'{table_name_item_prices}')

    field = Column(String(20), default=None)        # the name of the variable
    type = Column(String(10), default=None)         # the type of the variable (string, date, float, integer, etc.)
    value_flt = Column(Float, default=None)         # the value of the variable if it is a float
    value_str = Column(String(50), default=None)    # the value of the variable if it is not a float

    def __repr__(self):
        return f"<{table_name_item_prices}, {self.field}: {self.type}>"



