from data_collection.online_data.online_data import OnlineData

from pandas_datareader import data as data_reader
from data_plotting import matplotlib_plotting as plt
import quandl

quandl.ApiConfig.api_key = 'not-disclosed'


class QuandlFinanceData(OnlineData):
    """
    The extraction and manipulation of the data extracted from the quandl
    website (https://www.quandl.com/)
    """
    def __init__(self):
        OnlineData.__init__(self)

    def get_data(self, share_code, start=None, end=None, dividend=None):

        try:
            ticker = ''.join([u'WIKI/', share_code])
            self.data = quandl.get(ticker, start_date=start, end_date=end, authtoken= '5fzXmY5syu-JT4AsWyeR')
            self.data.head()
            return self.data
        except:
            return None

    def plot_adjusted_close_prices(self, ticker):
        try:


            temp_data = self.data["Adj. Close"]
            #close = self.data['adj_close']
            plt.PlotLine(temp_data, title=ticker, labelx=u'dates', labely=u'price')

        except:
            print(u'Problems plotting the closing prices of quandl!')
            return None

    def plot_volumes_prices(self, ticker):
        try:
            temp_data = self.data['Volume']
            plt.PlotLine(temp_data, title=ticker, labelx=u'dates', labely=u'price')
        except:
            print(u'Problems plotting the volumes prices of yahoo finance!')
            return None
