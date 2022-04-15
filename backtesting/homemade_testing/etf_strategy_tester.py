from utilities.common_methods import Methods as methods
from backtesting.homemade_testing.strategy_tester import StrategyTester
from backtesting.homemade_testing.strategy_tester import StrategyMethods
from utilities.common_methods import getDebugInfo
from backtesting.homemade_testing.commissions.degiro import DeGiro
from utilities import log

starting_capital = 150000
amount_to_add_each_time = 40000
loss_percentage = -0.05
sub_strategy = "buy_the_dip"  #"buy_the_dip"  # "fixed_time"


class EtfStrategyTester(StrategyTester):

    def __init__(self, broker, country='Italy'):
        """
        Initialise the variables of the tester class to backtest the strategy
        Country always italy because I always buy etf from "borsa italiana"
        @param None
        """
        try:
            StrategyTester.__init__(self, starting_capital, broker, country)

            self.purchases_history = []
            self.amount_spent_so_far = 0
            self.number_of_time_increased_position = 0
            self.total_cash_added = 0
            self.final_amount = 0
            self.final_size = 0
            self.total_num_years = 1
            self.compound_return = 0

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def run(self, prices, method=None):
        """
        It runs the strategy to back-test
        @param prices the prices on which the back-test will be performed.
        @param method in case of more techniques, the method defines which one to use.
        @return tbd
        """
        try:
            price_iter = self.define_entry_variables(prices)
            if sub_strategy == "buy_the_dip":
                self.loop_prices_increase_with_buy_the_dip(price_iter)
            elif sub_strategy == "fixed_time":
                self.loop_prices_increase_at_fixed_time(price_iter)

            print(f"")
            print(f"Here are the purchases when they happened:")
            print(*self.purchases_history, sep="\n")
            print(f"Total number of times increased money: {len(self.purchases_history)}")
            print(f"")

            self.defining_exit_variables()
            return self.results

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def add_a_buying_action(self, num_stocks_bought, price):
        """
        Method to add the buying action to keep track of all the purchases during investment history buying the dip
        @param price
        @return Nothing
        """
        # define the buying action as composed ofa pair (size, buying_price)
        num_stocks = int(num_stocks_bought)
        purchasing_price = price.close
        day_of_purchase = price.day
        amount_spent = round(num_stocks * purchasing_price, 2)

        buying_action = (num_stocks, purchasing_price, day_of_purchase, amount_spent)
        self.purchases_history.append(buying_action)

    def purchase_first_time(self, price_iter):
        """
        Run at the beginning od the algorithm to initialise and purchase the first time the share.
        @return the next price
        """
        last_price = self.buying_shares()
        price_next = next(price_iter)
        self.add_a_buying_action(self.size, price_next)
        self.amount_spent_so_far = self.size * self.buying_price
        return price_next

    def loop_prices_increase_at_fixed_time(self, price_iter):
        """
        The method loops through the prices and buys only when the price is below a threshold from the maximum price
        @return Nothing
        """
        try:
            price = self.purchase_first_time(price_iter)
            previous_year = price.day.year

            for price in price_iter:

                last_price = price.close
                print(f'Close, {last_price} in date {price.day}')

                if price.day.year != previous_year:
                    # else if year just changed, it is a new year and I want to increase my position.
                    previous_year = price.day.year
                    self.total_num_years += 1
                    # and do your stuff.

                    # INCREASE POSITION, INCREASE POSITION!!! (with default parameters)
                    num_stocks_bought = round(amount_to_add_each_time / price.close, 0)

                    #####
                    self.add_a_buying_action(num_stocks_bought, price)
                    #####

                    self.amount_spent_so_far += num_stocks_bought * price.close

                    print(f"Now buying at {price.close}. "
                          f"The amount spent on investing so far is: {round(self.amount_spent_so_far, 2)}")
            self.selling_shares(price.close)
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def loop_prices_increase_with_buy_the_dip(self, price_iter):
        """
        The method loops through the prices and buys only when the price is below a threshold from the maximum price
        @return Nothing
        """
        try:
            price = self.purchase_first_time(price_iter)
            maximum_reached = price.close
            previous_year = price.day.year

            purchased_in_the_solar_year = 0

            for price in price_iter:

                last_price = price.close
                print(f'Close, {last_price} in date {price.day}')

                if price.day.year != previous_year:

                    # if not purchased_in_the_solar_year:
                    #     self.purchase_shares(price)

                    # keep tracks of the years changing !!!
                    previous_year = price.day.year
                    self.total_num_years += 1
                    purchased_in_the_solar_year = 0

                # test update the maximum value
                if price.close > maximum_reached:
                    maximum_reached = price.close

                ratio = (price.close / maximum_reached) - 1

                if ratio < loss_percentage:
                    # INCREASE POSITION, INCREASE POSITION!!! (with default parameters)
                    previous_maximum = maximum_reached
                    maximum_reached = price.close

                    #####
                    self.purchase_shares(price)
                    purchased_in_the_solar_year += 1
                    #####

                    print(f"The previous maximum was {previous_maximum}. Now buying at {price.close}. "
                          f"A difference of {round(ratio, 4)}. "
                          f"The amount spent on investing so far is: {round(self.amount_spent_so_far, 2)}\n"
                          f"Here are the purchases when they happened {self.purchases_history}")
            self.selling_shares(price.close)

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def purchase_shares(self, price):
        """
        The method purchases the shares
        :return:
        """
        num_stocks_bought = round(amount_to_add_each_time / price.close, 0)
        self.add_a_buying_action(num_stocks_bought, price)
        self.amount_spent_so_far += num_stocks_bought * price.close

    def selling_shares(self, last_price):
        """
        The method is used when at the end we are selling the shares
        @param last_price the price at which we sell
        @return Nothing
        """
        try:
            self.selling_price = last_price
            self.final_amount = 0
            self.final_size = 0
            self.total_cash_added = 0
            self.number_of_time_increased_position = len(self.purchases_history)
            for purchase in self.purchases_history:
                self.total_cash_added += round(purchase[0] * purchase[1], 2)
                self.final_amount += purchase[0] * self.selling_price
                self.final_size += purchase[0]

            print('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f, Size %d' %
                  (self.selling_price, self.final_amount, self.commission_end, self.final_size))

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def defining_exit_variables(self):
        """
        It sets all the variables that can be used at the end of the algorithm by the calling functions.
        @return Nothing
        """
        try:
            self.starting_capital = self.buying_price * self.size
            self.ending_capital = self.final_amount - self.commission_start - self.commission_end
            self.amount_gained_lost = self.ending_capital - self.starting_capital
            rate = self.ending_capital / self.total_cash_added
            self.rate_gained_lost = rate - 1
            self.compound_return = methods.nth_root(rate, self.total_num_years) - 1

            self.results['starting_capital'] = self.starting_capital
            self.results['total_cash_added'] = self.total_cash_added
            self.results['ending_capital'] = self.final_amount
            self.results['amount_gained_lost'] = round(self.amount_gained_lost, 2)
            self.results['rate_gained_lost'] = round(self.rate_gained_lost, 1)
            self.results['contributions_from_beginning'] = self.amount_spent_so_far
            self.results['number_of_time_increased_position'] = self.number_of_time_increased_position
            self.results['total_num_years'] = self.total_num_years
            self.results['compound_return'] = self.compound_return

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
