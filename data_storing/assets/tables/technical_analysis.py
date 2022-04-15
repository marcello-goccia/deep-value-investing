
from utilities.config import database
from utilities.common_methods import getDebugInfo
from utilities import log

from sqlalchemy import Column, ForeignKey
from sqlalchemy.types import Integer, Float, Date, String
from sqlalchemy.orm import relationship
from data_storing.assets.base import Base

table_name = database.name_table_technical_analysis


class TechnicalAnalysis(Base):

    __tablename__ = table_name

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    equity_id = Column(Integer, ForeignKey(f'{database.name_table_equity}.id'))

    equity = relationship(u'Equity', back_populates=f'{table_name}')
    moving_average = relationship("MovingAverage", back_populates=f'{table_name}', cascade='all, delete-orphan')
    indicator = relationship("Indicator", back_populates=f'{table_name}', cascade='all, delete-orphan')
    pivot_point = relationship("PivotPoint", back_populates=f'{table_name}', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Technical analysis, asset id {self.equity_id}>"


def add_single_element(technical_analysis, field, value):
    try:
        if technical_analysis is None:
            return None

        if 'Something' in field:
            technical_analysis.something = value

        else:
            log.info(f"Could not find the following field {field}")

        return technical_analysis

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
        raise
