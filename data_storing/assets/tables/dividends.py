
from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float, String, Date, Enum
from data_storing.assets.common import DividendType
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name = database.name_table_dividends


class Dividends(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    equity_id = Column(Integer)

    ex_dividend_date = Column(Date, default=None)
    dividend_value = Column(Float, default=None)
    dividend_type = Column(Enum(DividendType), default=None)
    payment_date = Column(Date, default=None)
    yield_value = Column(Float, default=None)

    fundamentals_id = Column(Integer, ForeignKey(f'{database.name_table_fundamentals}.id'))
    fundamentals = relationship(u'Fundamentals', back_populates=f'{table_name}')
    item_dividends = relationship("ItemDividends", back_populates=f'{table_name}', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<{table_name}, dividend_date: {self.ex_dividend_date}"

