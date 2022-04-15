
from utilities.config import database
from utilities import log

from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Boolean
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name = database.name_table_etf


class Etf(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    symbol_1 = Column(String(20), default='')
    symbol_2 = Column(String(20), default='')
    symbol_3 = Column(String(20), default='')

    isin = Column(String(12), default='')
    name = Column(String(80), default='')

    weblink_1 = Column(String(300), default='')
    weblink_2 = Column(String(300), default='')
    weblink_3 = Column(String(300), default='')

    benchmark = Column(String(20), default='')
    exchange = Column(String(20), default='')
    issuer = Column(String(30), default='')
    sector = Column(String(20), default='')
    harmonised = Column(Boolean, default=False)
    country = Column(String(20), default='')
    manage_costs = Column(String(20), default='')

    def __repr__(self):
        return f"<{self.symbol_1}, isin={self.isin}>"
