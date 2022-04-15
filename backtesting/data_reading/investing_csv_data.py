from datetime import datetime
import backtrader as bt
from backtrader import feed, TimeFrame
from backtrader.utils import date2num
from backtrader.utils.py3 import integer_types, string_types

from utilities.common_methods import Methods as methods
from utilities import log
from utilities.common_methods import getDebugInfo

class InvestingCSVData(bt.feeds.GenericCSVData):

    params = (
        ('nullvalue', float('NaN')),
        ('dtformat', '"%b %d, %Y'),
        ('tmformat', '%H:%M:%S'),

        ('separator', '","'),

        ('datetime', 0),
        ('close', 1),
        ('open', 2),
        ('high', 3),
        ('low', 4),
        ('volume', 5),
        ('time', -1),
        ('openinterest', -1),
    )

    def start(self):
        super(InvestingCSVData, self).start()

        if isinstance(self.p.dtformat, string_types):
            self._dtstr = True
        elif isinstance(self.p.dtformat, integer_types):
            self._dtstr = False
            idt = int(self.p.dtformat)
            if idt == 1:
                self._dtconvert = lambda x: datetime.utcfromtimestamp(int(x))
            elif idt == 2:
                self._dtconvert = lambda x: datetime.utcfromtimestamp(float(x))

        else:  # assume callable
            self._dtconvert = self.p.dtformat

    def _loadline(self, linetokens):
        try:
            # Datetime needs special treatment
            dtfield = linetokens[self.p.datetime]
            if self._dtstr:
                dtformat = self.p.dtformat

                if self.p.time >= 0:
                    # add time value and format if it's in a separate field
                    dtfield += 'T' + linetokens[self.p.time]
                    dtformat += 'T' + self.p.tmformat

                dt = datetime.strptime(dtfield, dtformat)
            else:
                dt = self._dtconvert(dtfield)

            if self.p.timeframe >= TimeFrame.Days:
                # check if the expected end of session is larger than parsed
                if self._tzinput:
                    dtin = self._tzinput.localize(dt)  # pytz compatible-ized
                else:
                    dtin = dt

                dtnum = date2num(dtin)  # utc'ize

                dteos = datetime.combine(dt.date(), self.p.sessionend)
                dteosnum = self.date2num(dteos)  # utc'ize

                if dteosnum > dtnum:
                    self.lines.datetime[0] = dteosnum
                else:
                    # Avoid reconversion if already converted dtin == dt
                    self.l.datetime[0] = date2num(dt) if self._tzinput else dtnum
            else:
                self.lines.datetime[0] = date2num(dt)

            # The rest of the fields can be done with the same procedure
            for linefield in (x for x in self.getlinealiases() if x != 'datetime'):
                # Get the index created from the passed params
                csvidx = getattr(self.params, linefield)

                if csvidx is None or csvidx < 0:
                    # the field will not be present, assignt the "nullvalue"
                    csvfield = self.p.nullvalue
                else:
                    # get it from the token
                    csvfield = linetokens[csvidx]

                if csvfield == '':
                    # if empty ... assign the "nullvalue"
                    csvfield = self.p.nullvalue

                # get the corresponding line reference and set the value
                line = getattr(self.lines, linefield)

                if csvfield == '-':
                    csvfield = '0'

                if isinstance(csvfield, str):
                    csvfield = csvfield.replace('%"', '')
                    value = methods.convert_to_float(csvfield)
                else:
                    value = csvfield
                line[0] = float(float(value))

            return True

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
