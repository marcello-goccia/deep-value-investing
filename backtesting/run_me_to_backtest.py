import os, sys
import math
from colorama import Style
from utilities.log import root_folder_all_code

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_root = dir_path.split(root_folder_all_code, 1)[0]
code_path = os.path.join(dir_root, root_folder_all_code)
sys.path.insert(0, code_path)

from utilities import log
from utilities.common_methods import getDebugInfo
from utilities.common_methods import Methods as methods

import fundamentals.miscellaneous as fund_utils

from backtesting.homemade_testing import strategy_tester as st

# Strategies to choose from ...
# from fundamentals.strategies import StockPickingForWhatWorksWallStreet as StockPicking
# from fundamentals.strategies import StockPickingForAcquirersMultiple as StockPicking
# from fundamentals.strategies import StockPickingPiotrosky as StockPicking
from fundamentals.strategies import StockPickingIncubator as StockPicking


start_portfolio_value_ = 15000
max_number_of_equities_invested_in = 25  # 25
investing_years = [2015, 2016, 2017, 2018]  #2015, 2016, 2017, 2018, 2019

# countries = ['Greece', 'Singapore']
countries = [
    'United States',
    'Canada',
    # 'Mexico',
    'Austria',
    'Belgium',
    'Denmark',
    'France',
    'Germany',
    'Greece',
    # 'Israel',
    'Italy',
    'Netherlands',
    'Norway',
    # 'Portugal',
    # 'Spain',
    'Sweden',
    'Switzerland',
    'United Kingdom',
    'Australia',
    # 'Hong Kong',
    # 'Japan',
    # 'Singapore'
]

score_or_rank = ["rank"]  # "score"
strategy_method = st.StrategyMethods.buy_and_old

scraping_prices = False

enable_momentum = True
percentage_momentum = .2  # How much percentage of the overall equity number to select for the momentum phase

factors = [
    'acquirers_multiple',
    'price_to_book_ratio',
    # 'price_to_earnings_ratio',
    # 'price_to_sales',
    # 'ebitda_ev_ratio',
    'price_to_cash_flow',
    # 'shareholder_yield',
    # 'piotrosky_score',
]
# 'extra_factor',

methods_momentum = [
    #'price_appreciation',
    # 'price_distribution',
    'sma',
    # 'appreciation_to_market',
]

brokers_by_country = {
    'United States': 'degiro',
    'Canada': 'degiro',
    'Mexico': 'degiro',
    'Austria': 'degiro',
    'Belgium': 'degiro',
    'Denmark': 'degiro',
    'France': 'degiro',
    'Germany': 'degiro',
    'Greece': 'degiro',
    'Israel': 'degiro',
    'Italy': 'degiro',
    'Netherlands': 'degiro',
    'Norway': 'degiro',
    'Portugal': 'degiro',
    'Spain': 'degiro',
    'Sweden': 'degiro',
    'Switzerland': 'degiro',
    'United Kingdom': 'degiro',
    'Australia': 'degiro',
    'Hong Kong': 'degiro',
    'Japan': 'degiro',
    'Singapore': 'degiro'}


def main():
    start_portfolio_value = start_portfolio_value_  # dollars(?)
    first_time_portfolio_value = start_portfolio_value
    first_time_run_flag = True
    final_capital = 0

    investing_month = 2 # January

    minus_valenza = 0

    try:
        # initialise the algorithm which is entitled to pick the stocks of interest.
        stock_picking = StockPicking(max_number_of_equities_invested_in=max_number_of_equities_invested_in,
                                     percentage_momentum=percentage_momentum,
                                     enable_momentum=enable_momentum,
                                     countries=countries,
                                     score_or_rank=score_or_rank,
                                     path_pickles="../downloads/test/",
                                     scraping_prices_from_internet=scraping_prices)

        for investing_year in investing_years:

            dates = fund_utils.gm.get_testing_year_date_range(investing_year, investing_month)
            stock_picking.set_investing_year(investing_year)
            stock_picking.set_investing_month(investing_month)
            stock_picking.set_investing_dates(dates)

            # percent_to_invest = 0.20 or equally divided among equities
            amount_to_invest_in_each_equity = math.ceil(start_portfolio_value / max_number_of_equities_invested_in)
            stock_picking.set_max_price_per_share(amount_to_invest_in_each_equity)

            # ###############################
            # This will run the algorithm to choose the good equities
            # ###############################
            chosen_equities = stock_picking.run_algorithm()

            if not chosen_equities:
                continue

            initial_capital = 0
            final_capital = 0

            #################
            # Starting the back-test!!!
            #################

            for counter, equity in enumerate(chosen_equities):

                if equity.symbol_1 in fund_utils.gv.list_stocks_to_exclude:
                    continue

                log.info(f"counter: {counter}. Back-testing the equity: {equity.name}, "
                         f"with symbol: {equity.exchange}:{equity.symbol_1}, "
                         f"investing: {amount_to_invest_in_each_equity} dollars")

                prices_in_dates = methods.get_prices_in_range_of_dates(equity, dates)

                if not prices_in_dates:
                    continue

                country = equity.country
                broker_string = brokers_by_country[country]

                strategy = st.StrategyTester(amount_to_invest_in_each_equity, broker_string, equity)
                results = strategy.run(prices_in_dates, strategy_method)

                starting_capital = results['starting_capital']
                ending_capital = results['ending_capital']
                amount_gained_lost = results['amount_gained_lost']
                rate_earned = round(results['rate_gained_lost'] * 100, 2)
                # amount_gained_after_tax = results['amount_gained_after_tax']
                # starting_capital = results['ending_capital_after_tax']

                initial_capital += starting_capital
                final_capital += ending_capital

                color_fore, color_back, keyword = fund_utils.gm.get_color_and_keyword_gain_loss(amount_gained_lost)
                log.info(f"{color_back}{color_fore}The equity {keyword} {rate_earned}%. "
                         f"Total {round(amount_gained_lost, 2)} dollars {Style.RESET_ALL}")

            if first_time_run_flag:
                first_time_run_flag = False
                first_time_portfolio_value = initial_capital

            # ######### TAXES ##################
            capital_gain = final_capital - initial_capital
            taxable_amount = capital_gain + minus_valenza
            if taxable_amount < 0:
                minus_valenza = taxable_amount
                capital_gain_taxed = 0
            else:
                minus_valenza = 0
                capital_gain_taxed = taxable_amount * 0.26
            final_capital_after_tax = final_capital - capital_gain_taxed
            # ######### GONE ##########

            color_fore, color_back, keyword = \
                fund_utils.gm.get_color_and_keyword_gain_loss(final_capital - initial_capital)
            percent_gain = round((final_capital / initial_capital - 1) * 100, 2)
            log.info("----------------------------------------------------------")
            log.info(f"{color_back}{color_fore}The final portfolio for the  year "
                     f"{investing_year} is: {round(final_capital, 2)} dollars.\n"
                     f"We started with a portfolio of {round(initial_capital, 2)} dollar.\n"
                     f"We {keyword} {percent_gain}%.\n"
                     f"After taxes the final portfolio is now {round(final_capital_after_tax, 2)}"
                     f"{Style.RESET_ALL}")
            log.info("----------------------------------------------------------")
            log.info("----------------------------------------------------------")

            start_portfolio_value = final_capital_after_tax  # final_capital
            final_capital = final_capital_after_tax

        # END RESULTS
        color_fore, color_back, keyword = \
            fund_utils.gm.get_color_and_keyword_gain_loss(final_capital - first_time_portfolio_value)
        gain = final_capital / first_time_portfolio_value
        percent_gain = round((gain - 1) * 100, 2)
        num_years = investing_years[-1] - investing_years[0] + 1
        compound_return = round((methods.nth_root(gain, num_years) - 1) * 100, 2)
        log.info("**********************************************************")
        log.info(f"{color_back}{color_fore}The final portfolio for the years from {investing_years[0]} "
                 f"to {investing_years[-1]} is: {round(final_capital, 2)} dollars.\n"
                 f"We started with a portfolio of {round(first_time_portfolio_value, 2)} dollar.\n"
                 f"We {keyword} {percent_gain}% which corresponds to a compounded return of {compound_return}% "
                 f"{Style.RESET_ALL}")

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")


# run the program
if __name__ == "__main__":
    main()

# ######################################################################################################################


# def get_equity_historical_data_path(equity):
#     name_data_file = ''.join([equity.symbol_1, " Historical Data.csv"])
#     current_equity_historical_date_csv_path = os.path.join(paths.downloads, name_data_file)
#     if os.path.exists(current_equity_historical_date_csv_path):
#         os.remove(current_equity_historical_date_csv_path)  # going to get the newer version, so delete the old.
#     return current_equity_historical_date_csv_path


def old_back_tester():
    # successful = False
    # timeout = time.time() + 120  # 1 minutes from now
    # while not successful:
    #
    #     if time.time() > timeout:
    #         time.sleep(2)
    #         break
    #
    #     current_equity_historical_date_csv_path = get_equity_historical_data_path(equity)
    #     # It inverts the data from the current_equity_historical_date_csv_path
    #     # to the paths.historical_data_csv
    #     found = stock_picking.scraping_prices.get_historical_date_csv_file(equity,
    #                     current_equity_historical_date_csv_path, paths.historical_data_csv, dates=dates)
    #     if not found:
    #         log.error(f"Cannot get historical data for the equity {equity.exchange}:{equity.symbol_1}")
    #         break
    #
    #     if os.path.getsize(paths.historical_data_csv) < 100:  # Try again?
    #         time.sleep(2)
    #         continue
    #
    #     back_test = bs.BackTestStrategy(equity.symbol_1,
    #                                    dates['start_date'],
    #                                    dates['end_date'],
    #                                    start_portfolio_value,
    #                                    amount_to_invest_in_each_equity)
    #     amount_earned, rate_earned = back_test.run()
    # ending_portfolio_value = ending_portfolio_value + amount_earned
    # color_fore, color_back =
    #               fund_utils.gm.get_color_and_keyword_gain_loss(ending_portfolio_value - start_portfolio_value)
    # ending_portfolio_value = round(ending_portfolio_value, 2)
    # percent_gain = round((ending_portfolio_value / start_portfolio_value - 1) * 100, 2)
    # log.info(f"{color_back}{color_fore}The current final portfolio is: {ending_portfolio_value}, "
    #          f"with a gain (loss) of {percent_gain}%{Style.RESET_ALL}")
    # if os.path.exists(paths.historical_data_csv):
    #     os.remove(paths.historical_data_csv)  # remove the justly processed file.
    # successful = True
    # start_portfolio_value = ending_portfolio_value
    pass