
from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float, String, Date, Enum
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name = database.name_table_earnings


class Earnings(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    equity_id = Column(Integer)

    release_date = Column(Date, default=None)
    period_end = Column(Date, default=None)
    eps = Column(Float, default=None)
    eps_forecast = Column(Float, default=None)
    revenue = Column(Float, default=None)
    revenue_forecast = Column(Float, default=None)

    fundamentals_id = Column(Integer, ForeignKey(f'{database.name_table_fundamentals}.id'))
    fundamentals = relationship(u'Fundamentals', back_populates=f'{table_name}')
    item_earnings = relationship("ItemEarnings", back_populates=f'{table_name}', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<{table_name}, release_date: {self.release_date}"

