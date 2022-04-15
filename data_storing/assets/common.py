import enum


class Timespan(enum.Enum):
    annual = u'annual'
    quarterly = u'quarterly'


class MeasureUnit(enum.Enum):
    billion = u'billion'
    million = u'million'
    thousand = u'thousand'
    plain = u'plain'


class Benchmark(enum.Enum):
    company = u'company'
    industry = 'industry'


class DividendType(enum.Enum):
    monthly = 'Monthly'
    quarterly = u'Quarterly'
    semiannual = u'Semi-Annual'
    annual = u'Annual'
    ttm = u'Trailing Twelve Months'


class TimeFrame(enum.Enum):
    daily = 'Daily'
    weekly = 'Weekly'
    monthly = 'Monthly'
