import talib
import numpy as np
from utilities import log

# Documentation of ta-lib in:
# https://mrjbq7.github.io/ta-lib/func.html

#import ta
# from ta import trend
# when importing this library, here is an example on how to use it:
# ema = trend.ema_indicator(dataframe, n, fillna)  # n = ema window

class TechnicalAnalysis:

    def __init__(self):
        pass

    @staticmethod
    def get_sma(values_array, n=12, fillna=True):
        """
        @function get_sma
        Gets the simple moving average.
        @return the simple moving average just computed
        """
        sma = talib.SMA(np.array(values_array), n)
        return sma

    @staticmethod
    def get_ema(values_array, n=12, fillna=True):
        """
        @function get_ema
        Gets the exponential moving average.
        @return the exponential moving average just computed
        """
        ema = talib.EMA(np.array(values_array), n)
        return ema


