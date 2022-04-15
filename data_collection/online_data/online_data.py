


class OnlineData:
    """
    The base class which contains all the methods needed to get financial data from
    a known website.
    """
    def __init__(self):
        self.data = None

    def get_data(self, share_code, start=None, end=None, fundamentals=None):
        raise NotImplementedError

    def plot_adjusted_close_prices(self, ticker):
        raise NotImplementedError
