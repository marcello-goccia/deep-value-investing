
# Import the backtrader platform
import backtrader as bt
import math

from backtesting.strategies.basic_strategy import BasicStrategy


# Create a Stratey
class BuyAndHoldStopLoss(BasicStrategy):

    params = ()

    def __init__(self, cash_to_invest_in_asset):

        BasicStrategy.__init__(self, cash_to_invest_in_asset)

        self.percentage_stop_loss = 0.20
        self.already_bought = False
        self.already_sold = False

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close, %.2f' % self.dataclose[0])

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market, otherwise, buy!
        if not self.position and not self.already_bought:

            # BUY, BUY, BUY!!! (with default parameters)
            self.log('BUY CREATE, %.2f' % self.dataclose[0])

            # Keep track of the created order to avoid a 2nd order
            self.num_stocks_bought = round(self.amount_money_invested / self.dataclose[0])
            self.buying_price = self.dataclose[0]
            self.order = self.buy(size=self.num_stocks_bought, price=self.dataclose[0])  #, exectype=bt.Order.StopTrail, trailpercent=0.001)

            self.already_bought = True
            return

        else:  # protect with a stop loss
            if not self.already_sold:
                if self.dataclose[0] < self.buying_price * (1 - self.percentage_stop_loss):
                    # SELL, SELL, SELL!!! (with all possible default parameters)
                    self.log('SELL CREATE, %.2f' % self.dataclose[0])

                    # Keep track of the created order to avoid a 2nd order
                    self.order = self.sell(size=self.num_stocks_bought)
                    self.num_stocks_bought = 0

                    self.already_sold = True
