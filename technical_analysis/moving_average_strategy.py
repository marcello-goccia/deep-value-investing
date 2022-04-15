from technical_analysis.buying_signals import BuyingSignals
from technical_analysis.technical_analysis import TechnicalAnalysis
from utilities import log

class MovingAverageStrategy:

    def __init__(self, ticker):
        self.ticker = ticker

    def buying_signal_moving_averages(self, data, mas):

        mas['200'] = TechnicalAnalysis.get_ema(data, 200)
        mas['50']  = TechnicalAnalysis.get_ema(data, 50)

        if (BuyingSignals.ma_buying_signal(mas, '50', '200')):
            self.buy_or_not(True)
            return True, mas
        else:
            self.buy_or_not(False)
            return False, mas

    def buy_or_not(self, buy):
        if (buy):
            print(f"It is time to buy {self.ticker}")
        else:
            print(f"Wait to buy {self.ticker} it is not time yet")

