
# Import the backtrader platform
import backtrader as bt
import math

from backtesting.strategies.basic_strategy import BasicStrategy


# Create a Stratey
class ExponentialMovingAverage(BasicStrategy):

    params = (
        # period for the fast Moving Average
        ('p1', 50),
        # period for the slow moving average
        ('p2', 200),
    )

    def __init__(self, cash_to_invest_in_asset):

        BasicStrategy.__init__(self, cash_to_invest_in_asset)

        # For the moving average strategy
        sma1 = bt.indicators.EMA(period=self.p.p1)
        sma2 = bt.indicators.EMA(period=self.p.p2)
        self.lines.signal = sma1 - sma2


    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            if self.lines.signal > 0:
                # BUY, BUY, BUY!!! (with default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.num_stocks_bought = math.ceil(self.amount_money_invested / self.dataclose[0])
                self.order = self.buy(size=self.num_stocks_bought)

        else:
            if self.lines.signal < 0:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=self.num_stocks_bought)
                self.num_stocks_bought = 0
