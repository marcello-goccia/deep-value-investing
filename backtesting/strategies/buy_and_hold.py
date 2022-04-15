
# Import the backtrader platform
import backtrader as bt
import math

from backtesting.strategies.basic_strategy import BasicStrategy


# Create a Stratey
class BuyAndHold(BasicStrategy):

    params = ()

    def __init__(self, cash_to_invest_in_asset):

        BasicStrategy.__init__(self, cash_to_invest_in_asset)

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market, otherwise, buy!
        if not self.position:

            # BUY, BUY, BUY!!! (with default parameters)
            self.log('BUY CREATE, %.2f' % self.dataclose[0])

            # Keep track of the created order to avoid a 2nd order
            self.num_stocks_bought = round(self.amount_money_invested / self.dataclose[0])
            self.order = self.buy(size=self.num_stocks_bought, price=self.dataclose[0]) # , exectype=bt.Order.StopTrail, trailpercent=0.001)
            return
