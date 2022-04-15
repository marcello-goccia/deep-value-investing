from utilities import log
from utilities.common_methods import getDebugInfo
from backtesting.strategies.basic_strategy import BasicStrategy

loss_percentage = -0.06

# start with
# 14,724
# end cash invested is 50506 (added 35782)
# is like every year I add 3578.2

# Create a Strategy
class DollarCostAveraging(BasicStrategy):

    params = ()

    def __init__(self, cash_to_invest_in_asset):

        BasicStrategy.__init__(self, cash_to_invest_in_asset)

        self.already_bought = False
        self.already_sold = False
        self.current_maximum = 0
        self.amount_spent_so_far = 1
        self.number_times_add_cash = 0

    def next(self):
        try:
            # Simply log the closing price of the series from the reference
            message_to_write = f'Close, {self.dataclose[0]}, number of times added cash = {self.number_times_add_cash}'
            self.log(message_to_write)
            #self.log('Close, %.2f' % self.dataclose[0])

            # Check if an order is pending ... if yes, we cannot send a 2nd one
            if self.order:
                return

            if self.dataclose[0] > self.current_maximum:
                self.current_maximum = self.dataclose[0]

            # Check if we are in the market, otherwise, buy!
            if not self.position and not self.already_bought:

                # BUY, BUY, BUY!!! (with default parameters)
                self.log('BUY CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.num_stocks_bought = round(self.amount_money_invested / self.dataclose[0])
                self.buying_price = self.dataclose[0]
                self.order = self.buy(size=self.num_stocks_bought, price=self.dataclose[0])  #, exectype=bt.Order.StopTrail, trailpercent=0.001)

                self.already_bought = True

                self.amount_spent_so_far = self.buying_price * self.num_stocks_bought
                print(f"The amount spent on investing so far is: {self.amount_spent_so_far}")
                return

            else:
                ratio = self.dataclose[0] / self.current_maximum - 1
                if ratio < loss_percentage:
                    # BUY, BUY, BUY!!! (with default parameters)
                    previous_maximum = self.current_maximum
                    buying_price = self.dataclose[0]

                    self.current_maximum = buying_price
                    self.num_stocks_bought = 1
                    self.buying_price = buying_price
                    amount_added = 15000
                    #self.broker.add_cash(s elf.buying_price * self.num_stocks_bought)
                    self.broker.add_cash(amount_added)
                    self.number_times_add_cash += 1
                    self.amount_spent_so_far += amount_added
                    print(f"The previous maximum was {previous_maximum}. Now buying at {buying_price}. "
                          f"A difference of {round(ratio, 4)}. "
                          f"The amount spent on investing so far is: {round(self.amount_spent_so_far, 2)}")
                    return
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

