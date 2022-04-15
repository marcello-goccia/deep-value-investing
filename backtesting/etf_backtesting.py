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
from utilities.globals import paths

import fundamentals.miscellaneous as fund_utils
from backtesting.homemade_testing import etf_strategy_tester as st

import datetime
from website_scraping.investing_dot_com.scraping_prices import ScrapingPrices

strategy_method = st.StrategyMethods.buy_and_old
broker = "degiro"

def get_equity_historical_data_path(equity):
    name_data_file = ''.join([equity.symbol_1, " Historical Data.csv"])
    current_equity_historical_date_csv_path = os.path.join(paths.downloads, name_data_file)
    if os.path.exists(current_equity_historical_date_csv_path):
        os.remove(current_equity_historical_date_csv_path)  # going to get the newer version, so delete the old.
    return current_equity_historical_date_csv_path


def main():

    try:
        print(f"processing the etf index")

        import os
        for file in os.listdir(paths.backtesting_etf):
            if file.endswith(".csv"):
                # here we have the csv file with the historical data.
                path_file = os.path.join(paths.backtesting_etf, file)

                dates = dict()
                dates['start_date'] = datetime.date(2007, 3, 1)
                dates['end_date'] = datetime.date(2020, 2, 25)

                prices_between_dates = methods.get_prices_in_range_of_dates_from_file(path_file, dates)

                if not prices_between_dates:
                    continue

                strategy = st.EtfStrategyTester(broker)
                results = strategy.run(prices_between_dates, strategy_method)

                starting_capital = results['starting_capital']
                ending_capital = results['ending_capital']
                total_cash_added = results['total_cash_added']
                amount_earned = results['amount_gained_lost'] - total_cash_added
                rate_gained_lost = round(results['rate_gained_lost'] * 100, 2)
                contributions_from_beginning = results['contributions_from_beginning']
                number_of_time_increased_position = results['number_of_time_increased_position']
                total_num_years = results['total_num_years']
                compound_return = round(results['compound_return'] * 100, 2)

                color_fore, color_back, keyword = fund_utils.gm.get_color_and_keyword_gain_loss(amount_earned)
                log.info(f"{color_back}{color_fore}The equity {keyword} {rate_gained_lost}%.\n"
                         f"We started with a capital of {round(starting_capital, 2)} dollar.\n"
                         f"The capital is now {round(ending_capital, 2)} dollars.\n"
                         f"The contribution of cash was {round(contributions_from_beginning, 2)} dollars including the initial amount.\n"
                         f"Without the initial amount the contribution of cash was {round(contributions_from_beginning - starting_capital, 2)} dollars.\n"
                         f"The number of times I contributed with cash was {number_of_time_increased_position}\n"
                         f"We invested for a total of {total_num_years} years\n"
                         f"We achieved a compound return of {compound_return}%\n"
                         f"Total {keyword}: {round(amount_earned, 2)} dollars {Style.RESET_ALL}")

                if os.path.exists(paths.historical_data_csv):
                    os.remove(paths.historical_data_csv)  # remove the justly processed file.

                log.info(f"my portfolio is now {ending_capital}, processed the etf {file}")

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

# run the program
if __name__ == "__main__":
    main()



################################
# import time
# import datetime
# import os
# #import math
# from colorama import Fore, Back, Style
#
# from utilities import log
# from utilities.common_methods import getDebugInfo
# from utilities.globals import websites, paths
# #from data_storing.assets.database_manager import DatabaseManager as db_mngr
#
# from backtesting import backtest_strategy as bs
# from website_scraping.investing_dot_com.scraping_prices import ScrapingPrices
#
#
# def get_equity_historical_data_path(equity):
#     name_data_file = ''.join([equity.symbol_1, " Historical Data.csv"])
#     current_equity_historical_date_csv_path = os.path.join(paths.downloads, name_data_file)
#     if os.path.exists(current_equity_historical_date_csv_path):
#         os.remove(current_equity_historical_date_csv_path)  # going to get the newer version, so delete the old.
#     return current_equity_historical_date_csv_path
#
#
# def main():
#
#     start_porfolio_value = 15000  # dollars(?)
#     ending_portfolio_value = start_porfolio_value
#     max_number_of_equities_invested_in = 10
#
#     try:
#         start_time_process_equities = time.monotonic()
#
#         # percent_to_invest = 0.20
#         # or equally divided among equities
#         # amount_to_invest_in_each_etf = math.ceil(start_porfolio_value / num_shares)
#
#         counter_positive = 0
#
#         # scraping = ScrapingPrices()
#         # scraping.instantiate_driver(invisible=False)
#         # scraping.add_cookies(websites.investing_dot_com)
#
#         print(f"processing the etf index")
#
#         import os
#         for file in os.listdir(paths.backtesting_etf):
#             if file.endswith(".csv"):
#                 # here we have the csv file with the historical data.
#                 path_file = os.path.join(paths.backtesting_etf, file)
#                 ScrapingPrices.get_historical_date_csv_file(path_file, paths.historical_data_csv)
#
#                 fromdate = datetime.date(2010, 1, 1)
#                 todate = datetime.date(2020, 2, 25)
#                 amount_to_invest = 15000
#
#                 # log.info(f"backtesting the equity: {equity.name}, with symbol: {equity.symbol_1}, "
#                 #          f"investing: {amount_to_invest_in_each_equity}")
#
#                 backtest = bs.BackTestStrategy(file, fromdate, todate, start_porfolio_value, amount_to_invest)
#                 amount_earned, rate_earned = backtest.run()
#
#                 if amount_earned > 0:
#                     counter_positive += 1
#                 ending_portfolio_value = ending_portfolio_value + amount_earned
#
#                 if ending_portfolio_value > start_porfolio_value:
#                     color_back = Back.GREEN
#                     color_fore = Fore.BLACK
#                 elif ending_portfolio_value < start_porfolio_value:
#                     color_back = Back.RED
#                     color_fore = Fore.WHITE
#                 else:  # The same
#                     color_back = ""
#                     color_fore = ""
#
#                 log.info(f"{color_back}{color_fore}The current final portfolio is: {ending_portfolio_value}{Style.RESET_ALL}")
#
#                 if os.path.exists(paths.historical_data_csv):
#                     os.remove(paths.historical_data_csv)  # remove the justly processed file.
#
#                 log.info(f"my portfolio is now {ending_portfolio_value}, processed the etf {file}")
#
#     except Exception as e:
#         log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
#
# # run the program
# if __name__ == "__main__":
#     main()
