
from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float, Date, String, Boolean
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name = database.name_table_fundamentals


class Fundamentals(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    equity_id = Column(Integer, ForeignKey(f'{database.name_table_equity}.id'))

    #no_financial_available = Column(Boolean, default=False)

    equity = relationship(u'Equity', back_populates=f'{table_name}')
    balance_sheet = relationship("BalanceSheet", back_populates=f'{table_name}', cascade='all, delete-orphan')
    income_statement = relationship("IncomeStatement", back_populates=f'{table_name}', cascade='all, delete-orphan')
    cash_flow = relationship("CashFlow", back_populates=f'{table_name}', cascade='all, delete-orphan')
    ratios = relationship("Ratios", back_populates=f'{table_name}', cascade='all, delete-orphan')
    dividends = relationship("Dividends", back_populates=f'{table_name}', cascade='all, delete-orphan')
    earnings = relationship("Earnings", back_populates=f'{table_name}', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Fundamentals of asset with id {self.equity_id}>"
