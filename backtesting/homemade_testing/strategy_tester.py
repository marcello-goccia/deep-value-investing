import math
import fundamentals.miscellaneous as fund_utils
from utilities.common_methods import Methods as methods
from utilities.common_methods import getDebugInfo
from backtesting.homemade_testing.commissions.degiro import DeGiro
from utilities import log


class StrategyMethods:
    buy_and_old = "buy_and_old"
    stop_loss = "stop_loos"
    trailing_stop_loss = "trailing_stop_loss"


class StrategyTester:

    def __init__(self, amount_instantiated, broker_string, equity):
        """
        Initialise the variables of the tester class to backtest the strategy
        @param None
        """
        try:
            self.buying_price = 0
            self.selling_price = 0
            self.commission_start = 0
            self.commission_end = 0
            self.starting_capital = 0
            self.ending_capital = 0
            self.amount_gained_lost = 0
            self.rate_gained_lost = 0
            self.size = 0
            self.results = {}

            self.broker = self.define_broker(broker_string)
            self.equity = equity
            currency = methods.validate(self.equity.overview.currency)
            self.exchange_rate = fund_utils.gm.get_exchange_rate(currency, self.equity)
            self.country = equity.country
            self.percentage_overdraft = 15  # percent
            self.amount_instantiated = amount_instantiated

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def set_amount_overdraft(self):
        """
        The amount instantiated to purchase stocked will be a higher percentage of the amount originally instantiated.
        @return Nothing
        """
        try:
            self.percentage_overdraft /= 100
            self.percentage_overdraft += 1
            self.amount_instantiated *= self.percentage_overdraft
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def define_broker(self, broker_string):
        """
        Method used to define the broker object.
        @param broker_string the string which defines the broker to be used.
        @return Nothing
        """
        try:
            if broker_string == "degiro":
                return DeGiro()
            elif broker_string == 'directa':
                return None

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def define_commission(self, broker_string, country):
        """
        It sets the commission according to the country you would like to invest in.
        @param country the country you are investing in.
        @return Nothing
        """
        try:
            self.broker.set_country(country)
            self.commission_start = self.broker.get_commission(size=self.size, buying_price=self.buying_price)

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def run(self, prices, method_investing):
        """
        It runs the strategy to back-test
        @param prices the prices on which the back-test will be performed.
        @return tbd
        """
        try:
            price_iter = self.define_entry_variables(prices)

            if method_investing == StrategyMethods.buy_and_old:
                self.loop_prices_buy_hold(price_iter)
            elif method_investing == StrategyMethods.stop_loss:
                self.loop_prices_stop_loss(price_iter)
            elif method_investing == StrategyMethods.trailing_stop_loss:
                self.loop_prices_trailing_stop_loss(price_iter)

            self.defining_exit_variables()

            return self.results

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def loop_prices_buy_hold(self, price_iter):
        """
        The method loops through the prices to decide when to buy and sell
        @return Nothing
        """
        try:
            last_price = self.buying_shares()

            for price in price_iter:
                last_price = self.get_price_close(price)
                print('Close, %.2f' % last_price)

            self.selling_shares(last_price)

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def loop_prices_stop_loss(self, price_iter):
        """
        The method loops through the prices and sells only when the price are below a threshold from the buying price
        @return Nothing
        """
        try:
            last_price = self.buying_shares()

            threshold = 0.20
            threshold_price = self.buying_price * (1 - threshold)

            for price in price_iter:
                last_price = self.get_price_close(price)
                print('Close, %.2f' % last_price)
                if last_price < threshold_price:
                    print('The stop loss was triggered !!!')
                    break

            self.selling_shares(last_price)

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def loop_prices_trailing_stop_loss(self, price_iter):
        """
        The method loops through the prices and sells only when the price are below a threshold from the buying price
        @return Nothing
        """
        try:
            last_price = self.buying_shares()

            threshold = 0.20
            maximum_reached = 0
            threshold_price = 0

            for price in price_iter:
                last_price = self.get_price_close(price)
                print('Close, %.2f' % last_price)

                if last_price > maximum_reached:
                    maximum_reached = last_price
                    threshold_price = maximum_reached * (1- threshold)

                if last_price < threshold_price:
                    print('The trailing stop loss was triggered !!!')
                    break

            self.selling_shares(last_price)

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def buying_shares(self):
        """
        The method is used when at the beginning we are buying the shares
        @return the last price
        """
        try:
            # define which is the last price, because I am selling of the end of the set of prices.
            last_price = self.buying_price

            print('BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, Size %d' %
                  (self.buying_price, self.buying_price * self.size, self.commission_start, self.size))

            return last_price

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def selling_shares(self, last_price):
        """
        The method is used when at the end we are selling the shares
        @param last_price the price at which we sell
        @return Nothing
        """
        try:
            self.selling_price = last_price

            self.commission_end = self.broker.get_commission(size=self.size, buying_price=self.selling_price)

            print('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, Size %d' %
                  (self.selling_price, self.selling_price * self.size, self.commission_end, self.size))

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def define_entry_variables(self, prices):
        """
        It defines the variables used by the algorithm
        @param prices the list of prices to use in the backtest algorithm
        @return the iterator to the prices list
        """
        try:
            # buy at the first day of the sequence
            price_iter = iter(prices)
            price = next(price_iter)
            self.buying_price = self.get_price_close(price)

            if math.floor(self.amount_instantiated / self.buying_price) < 2:
                self.set_amount_overdraft()

            self.size = self.amount_instantiated // self.buying_price
            self.define_commission(self.broker, self.country)

            return price_iter
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def defining_exit_variables(self):
        """
        It sets all the variables that can be used at the end of the algorithm by the calling functions.
        @return Nothing
        """
        try:
            self.starting_capital = self.buying_price * self.size
            self.ending_capital = self.selling_price * self.size - self.commission_start - self.commission_end
            self.amount_gained_lost = self.ending_capital - self.starting_capital
            self.rate_gained_lost = self.ending_capital / self.starting_capital - 1

            self.results['starting_capital'] = self.starting_capital
            self.results['total_cash_added'] = 0
            self.results['ending_capital'] = self.ending_capital
            self.results['amount_gained_lost'] = self.amount_gained_lost
            self.results['rate_gained_lost'] = self.rate_gained_lost
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_price_close(self, price):
        """
        It returns the price close wth certain rules
        @param price the equity close price
        @return the wanted price
        """
        try:
            return price.close * self.exchange_rate

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

