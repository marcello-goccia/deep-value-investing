from data_collection.online_data.online_data import OnlineData

from pandas_datareader import data as data_reader
from data_plotting import matplotlib_plotting as plt
#import fix_yahoo_finance as yf
import yfinance as yf
yf.pdr_override()  # <== that's all it takes :-)


class YahooFinanceData(OnlineData):
    """
    The extraction and manipulation of the data extracted from the yahoo financial
    website
    """
    def __init__(self):
        OnlineData.__init__(self)

    def get_data(self, share_code, start=None, end=None, dividend=None):

        try:
            self.data = data_reader.get_data_yahoo(share_code,
                                                    start=start, end=end,
                                                    # download dividend + stock splits data
                                                    # (optional, default is None)
                                                    # options are:
                                                    #   - True (returns history + actions)
                                                    #   - 'only' (actions only)
                                                    actions=dividend)
            # data returned as data reader.
            return self.data

        except:
            print(u'Data not collected from yahoo finance')
            return None

    # Call it the following way
    #quantitative.requested.plot_adjusted_close_prices(ticker)
    def plot_adjusted_close_prices(self, ticker):
        try:
            close = self.data['Adj Close']
            plt.PlotLine(close, title=ticker, labelx=u'dates', labely=u'price')
        except:
            print(u'Problems plotting the closing prices of yahoo finance!')
            return None

    # Call it the following way
    # quantitative.requested.plot_volumes_prices(ticker)
    def plot_volumes_prices(self, ticker):
        try:
            volumes = self.data['Volume']
            plt.PlotLine(volumes, title=ticker, labelx=u'dates', labely=u'price')
        except:
            print(u'Problems plotting the volumes prices of yahoo finance!')
            return None

