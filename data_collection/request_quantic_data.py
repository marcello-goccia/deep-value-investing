import datetime
import time
from utilities import log

from data_collection.online_data import *


class RequestQuanticData:

    def __init__(self):

        self.requested = YahooFinanceData()
        self.requested = QuandlFinanceData()
        pass

    def get_requested_data(self, share_code, start, end=None, dividend=None):
        if end == None:
            end = self.get_today_date()

        try:
            self.requested.get_data(share_code,
                                            start=start, end=end,
                                            # download dividend + stock splits data
                                            # (optional, default is None)
                                            # options are:
                                            #   - True (returns history + actions)
                                            #   - 'only' (actions only)
                                            dividend=dividend)

            if self.requested.data is not None:
                ok = True
            else:
                time.sleep(0.5)
                raise Exception(u'data not collected')

        except:
            print("Cannot get the data from the server. Trying with the next ticket.")
            return


    @staticmethod
    def get_today_date():
        try:
            return datetime.datetime.today().strftime('%Y-%m-%d')
        except:
            print("Cannot define the current date.")
            return None
