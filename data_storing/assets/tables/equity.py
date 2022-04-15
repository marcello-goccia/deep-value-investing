
from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float,  String, Boolean
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name = database.name_table_equity


class Equity(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    symbol_1 = Column(String(20), default='')
    symbol_2 = Column(String(20), default='')
    symbol_3 = Column(String(20), default='')

    name = Column(String(80), default='')

    weblink_1 = Column(String(300), default='')
    weblink_2 = Column(String(300), default='')
    weblink_3 = Column(String(300), default='')

    exchange = Column(String(20), default='')

    sector = Column(String(16), default='')
    industry = Column(String(16), default='')

    country = Column(String(16), default='')
    num_employees = Column(Float, default=None)
    equity_type = Column(String(16), default='')
    hq_country = Column(String(16), default='')
    telephone = Column(String(16), default='')

    all_done = Column(Boolean, default=False)

    overview = relationship("Overview", uselist=False, back_populates=f'{table_name}', cascade='all, delete-orphan')
    fundamentals = relationship("Fundamentals", uselist=False, back_populates=f'{table_name}', cascade='all, delete-orphan')
    technical_analysis = relationship("TechnicalAnalysis", uselist=False, back_populates=f'{table_name}', cascade='all, delete-orphan')
    prices = relationship("Prices", back_populates=f'{table_name}', cascade='all, delete-orphan')
    item_equity = relationship("ItemEquity", back_populates=f'{table_name}', cascade='all, delete-orphan')


    def __repr__(self):
        return f"<{self.symbol_1}, name={self.name}, exchange={self.exchange}>"


def add_single_element(equity, field, value):
    """
    @function add_single_element
    It adds a single element but it does not perform the commit to save it to the database
    """
    try:
        if equity is None:
            return -2

        if 'Name' in field:
            equity.name = value
        elif 'Symbol' in field:
            equity.symbol_1 = value
        elif 'weblink_investing' in field:
            equity.weblink_1 = value
        elif 'weblink_yahoo' in field:
            equity.weblink_2 = value
        elif 'weblink_something_else' in field:
            equity.weblink_3 = value
        elif 'Exchange' in field:
            equity.exchange = value
        elif 'Sector' in field:
            equity.sector = value
        elif 'Industry' in field:
            equity.industry = value
        elif 'Country' in field:
            equity.country = value

        elif 'Market Cap' in field:
            equity.market_cap = value
        elif 'Employees' in field:
            equity.num_employees = value
        elif 'Equity Type' in field:
            equity.equity_type = value
        elif 'HQ country' in field:
            equity.hq_country = value
        elif 'Telephone' in field:
            equity.telephone = value

        elif 'all done' in field:
            equity.all_done = value

        else:
            log.info(f"Could not find the following field {field}")

        return 0

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
        return -1
