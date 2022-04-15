
from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float, Date, String
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name = database.name_table_pivot_point


class PivotPoint(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    equity_id = Column(Integer, ForeignKey(f'{database.name_table_equity}.id'))
    technical_analysis_id = Column(Integer, ForeignKey(f'{database.name_table_technical_analysis}.id'))
    technical_analysis = relationship(u'TechnicalAnalysis', back_populates=f'{table_name}')

    day = Column(Date, default=None)        # the day it was measured
    name = Column(String(20), default=None) # its name: classic, fibonacci, camarilla, woodies, demarks,  etc.
    price_levels = Column(String(10), default=None)  # support S1, S2, S3 or resistance R1, R2, R3 or pivot_points PP
    value = Column(Float, default=None)     # the value of the pivot point

    def __repr__(self):
        return f"<{table_name}," \
            f"day: {self.day}," \
            f"name: {self.name}>"
