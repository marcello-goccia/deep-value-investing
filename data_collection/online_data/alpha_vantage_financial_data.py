from data_collection.online_data.online_data import OnlineData

# need to install the alpha vantage package.
from alpha_vantage.timeseries import TimeSeries
# from https://www.alphavantage.co

api_code = u'your-api-code'

class AlphaVantageFinanceData(OnlineData):
    """
    The extraction and manipulation of the data extracted from the alpha vantage
    website (https://https://www.alphavantage.co//)
    Free API in json and CSV format.
    """
    def __init__(self):
        OnlineData.__init__(self)

    def get_data(self, share_code, start=None, end=None, fundamentals=None):

        try:

            ts = TimeSeries(key=api_code, output_format='pandas')
            # example with the intra-day data.
            self.data, meta_data = ts.get_intraday(symbol=share_code, interval='1min', outputsize='full')

        except:
            return None
