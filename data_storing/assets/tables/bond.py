
from utilities.config import database
from utilities import log

from datetime import date
from sqlalchemy import Column
from sqlalchemy.types import Integer, String, Date
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name = database.name_table_bond


class Bond(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    isin = Column(String(12), default='')
    name = Column(String(80), default='')
    weblink_1 = Column(String(300), default='')
    weblink_2 = Column(String(300), default='')
    weblink_3 = Column(String(300), default='')
    market = Column(String(20), default='')
    coupon_yield = Column(String(15), default='')
    coupon_type = Column(String(15), default='')
    expiry_date = Column(Date, default=date(1900, 1, 1))
    rating = Column(String(10), default='')
    country = Column(String(16), default='')

    def __repr__(self):
        return f"<{self.name}, isin={self.isin}>"
