
from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float, Date, String
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name = database.name_table_moving_average


class MovingAverage(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    equity_id = Column(Integer, ForeignKey(f'{database.name_table_equity}.id'))
    technical_analysis_id = Column(Integer, ForeignKey(f'{database.name_table_technical_analysis}.id'))
    technical_analysis = relationship(u'TechnicalAnalysis', back_populates=f'{table_name}')

    day = Column(Date, default=None)        # the day it was measured
    type = Column(String(15), default=None)     # simple or exponential
    period = Column(Float, default=None)   # 5 - 10 - 20 - 200 etc.
    value = Column(Float, default=None)     # the value of the moving average

    def __repr__(self):
        return f"<{table_name}," \
            f"day: {self.day}," \
            f"type: {self.type}>"
