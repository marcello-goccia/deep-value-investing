
from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float, Date, Enum
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base
from data_storing.assets.common import TimeFrame

table_name = database.name_table_prices


class Prices(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    equity_id = Column(Integer, ForeignKey(f'{database.name_table_equity}.id'))
    equity = relationship(u'Equity', back_populates=f'{table_name}')

    time_frame = Column(Enum(TimeFrame), default=None)

    day = Column(Date, default=None)
    open = Column(Float, default=None)
    close = Column(Float, default=None)
    high = Column(Float, default=None)
    low = Column(Float, default=None)
    volume = Column(Float, default=None)

    item_prices = relationship("ItemPrices", back_populates=f'{table_name}', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Prices day: {self.day} of asset id: {self.equity_id}, close: {self.close}>"


def add_single_element(prices, field, value):
    try:
        if prices is None:
            return None

        if 'Something' in field:
            prices.something = value

        else:
            log.info(f"Could not find the following field {field}")

        return prices

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
        raise
