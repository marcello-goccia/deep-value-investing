import time
import os
import sys
from datetime import datetime
from urllib.request import urlopen, URLError
import subprocess
from utilities.log import root_folder_all_code

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_root = dir_path.split(root_folder_all_code, 1)[0]
code_path = os.path.join(dir_root, root_folder_all_code)
sys.path.insert(0, code_path)

from utilities.common_methods import getDebugInfo
from utilities.common_methods import Methods as methods
from utilities.globals import websites
from utilities.common_methods import EthernetProblems as eth_problems
from utilities import log

from website_scraping.investing_dot_com.scraping_fundamentals import ScrapingFundamentals
from website_scraping.investing_dot_com.scraping_income_statement import ScrapingIncomeStatement
from website_scraping.investing_dot_com.scraping_balance_sheet import ScrapingBalanceSheet
from website_scraping.investing_dot_com.scraping_cash_flow import ScrapingCashFlow
from website_scraping.investing_dot_com.scraping_ratios import ScrapingRatios
from website_scraping.investing_dot_com.scraping_dividends import ScrapingDividends
from website_scraping.investing_dot_com.scraping_earnings import ScrapingEarnings
from website_scraping.investing_dot_com.scraping_prices import ScrapingPrices
from website_scraping.investing_dot_com.assets_labels import Labels as labels

from data_storing.assets.database_manager import DatabaseManager as db_mngr


def print_time_spent(starting_time, num_equities):
    if num_equities == 0:
        message = f"Time spent to process is zero, because there were not equities available in the database"
    else:
        # profiling code messages
        elapsed_time_process_equities = time.monotonic() - starting_time
        num_seconds_spent = methods.truncate(elapsed_time_process_equities, 2)
        seconds_per_equity = methods.truncate(elapsed_time_process_equities / num_equities, 2)
        message = f"The time spent to process {num_equities} equities " \
            f"is {num_seconds_spent} seconds. Overall the software " \
            f"took {seconds_per_equity} seconds to retrieve info for each equity"
    log.info(message)
    # end of profiling code messages


def restart_webdriver(scraping, scrape_income_statement, scrape_balance_sheet, scrape_cash_flow,
                      scrape_ratios, scrape_dividends, scrape_earnings, scrape_historical_data=None, invisible=False):
    log.info("Quitting webdriver")
    scraping.driver.quit()
    scraping.instantiate_driver(invisible=invisible)
    log.info("And restarted!")

    scraping.instantiate_driver(invisible=invisible)
    scrape_income_statement.set_driver(scraping.driver)
    scrape_balance_sheet.set_driver(scraping.driver)
    scrape_cash_flow.set_driver(scraping.driver)
    scrape_ratios.set_driver(scraping.driver)
    scrape_dividends.set_driver(scraping.driver)
    scrape_earnings.set_driver(scraping.driver)
    scrape_historical_data.set_driver(scraping.driver)


def check_there_is_internet_connection():
    try:
        p = subprocess.Popen(['nslookup', 'google.com'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        stdout, stderr = p.communicate()
        #print(stdout)
        #print(stderr)

        # nslookup google.com in address there is the google ipaddress.
        urlopen('http://216.58.192.142', timeout=1)
        return True
    except URLError as err:
        return False


def are_there_ethernet_problems(scraping):
    if eth_problems.connection_problems:
        scraping.driver.quit()
        eth_problems.connection_problems = False
        eth_problems.counter_connection_problems = 0
        time.sleep(5)  # wait 5 seconds and try again
        return True
    else:
        return False


def equity_still_exists(equity):
    existing_page = True
    for item in equity.item_equity:
        if item.field == 'link_problems':
            existing_page = False
            break
    return existing_page


def is_equity_existing_in_investing_com(equity):
    """
    if the fundamentals have not been filled, need to check, it is a new equity or
    there is not information in investing.com
    @param equity the equity to analyse
    @return False if not existing in investing.com
    """
    try:
        if not equity.fundamentals.balance_sheet and \
                not equity.fundamentals.income_statement and \
                not equity.fundamentals.cash_flow:
            # if the fundamentals have not been filled, we need to check,
            # it could be a new equity or there is not information in investing.com
            # - if it is new equity we still need to do all the scraping, it exists (return True)
            # - if there is not information, we say, at least in the stock exchange it does not exist (return False)

            # check it is a new equity:
            # the following checks that some info was already filled (the equity type in this case)
            # if it was already filled, it means, if we are here, there are not fundamentals for that equity!!!
            # ergo I do not want to investigate further this equity
            if equity.equity_type:  # if the field exists
                # it means it was already scraped previously but we did not get anything.
                # it seems there is not information in investing.com
                # equity.all_done = True
                # db_mngr.commit_to_database()  # wait for the following, I want to do more tests.
                # return false because there is the overview but not any fundamental information is avaiable
                return False
            else:
                # it is just a new equity and we can keep on scraping the info.
                return True
        else:
            return True
    except Exception as e:
        log.error(f"There is a problem in the code when checking the equity is new or it does "
                  f"not exist in investing.com!: {e}\n{getDebugInfo()}")
        return True


def scraping_all(equity, counter_processed_equities, scraping, scrape_income_statement, scrape_balance_sheet,
                 scrape_cash_flow, scrape_ratios, scrape_dividends, scrape_earnings, scrape_historical_data=None):
    """
    returns -1 if ethernet_problems (break in the not-refactored version)
    returns -2 if exception_raised (continue in the not-refactored version)
    returns -3 if fundamental data for the equity is not present in the website investing.com
    """
    if not is_equity_existing_in_investing_com(equity):
        return -3

    scraping.retrieve_overview(equity)
    scraping.close_popup_if_present()
    scraping.retrieve_company_profile(equity)
    scraping.close_popup_if_present()
    if are_there_ethernet_problems(scraping):
        return -1

    # INCOME STATEMENT
    scrape_income_statement.retrieve_company_income_statement(equity)
    if scraping.exception_raised:
        scraping.set_equity_extraction_completed(equity)
        counter_processed_equities += 1
        return -2
    if are_there_ethernet_problems(scraping):
        return -1

    # BALANCE SHEET
    scrape_balance_sheet.retrieve_company_balance_sheet(equity)
    if scraping.exception_raised:
        scraping.set_equity_extraction_completed(equity)
        counter_processed_equities += 1
        return -2
    if are_there_ethernet_problems(scraping):
        return -1

    # CASH FLOW
    scrape_cash_flow.retrieve_company_cash_flow(equity)
    if scraping.exception_raised:
        scraping.set_equity_extraction_completed(equity)
        counter_processed_equities += 1
        return -2
    if are_there_ethernet_problems(scraping):
        return -1

    # COMPANY RATIOS
    scrape_ratios.retrieve_company_ratios(equity)
    if scraping.exception_raised:
        scraping.set_equity_extraction_completed(equity)
        counter_processed_equities += 1
        return -2
    if are_there_ethernet_problems(scraping):
        return -1

    # DIVIDENDS
    scrape_dividends.retrieve_company_dividends(equity)
    if scraping.exception_raised:
        scraping.set_equity_extraction_completed(equity)
        counter_processed_equities += 1
        return -2
    if are_there_ethernet_problems(scraping):
        return -1

    # EARNINGS
    scrape_earnings.retrieve_company_earnings(equity)
    if scraping.exception_raised:
        scraping.set_equity_extraction_completed(equity)
        counter_processed_equities += 1
        return -2
    if are_there_ethernet_problems(scraping):
        return -1

    # HISTORICAL DATA
    scrape_historical_data.retrieve_monthly_company_historical_data(equity, starting_date="01/01/2014")


def main():

    equity_string_id = ''
    from_scratch = 'new'
    update = 'update'
    start_time_process_equities = time.monotonic()
    counter_processed_equities = 0
    number_maximum_equities_each_session = 80
    invisible_browser = False

    try:
        # get the equities according to some well defined key!!!
        equities = db_mngr.query_all_equities_by()  # country="United States" 'Bahrain')

        # ASK USER WHAT TO DO
        user_input = input(f"Input '{from_scratch}' to get all full companies from scratch. "
                           f"Input '{update}' to update according to the next earning date. "
                           f"Any choice different from {update} will be treated as {from_scratch}:\n")
        # user_input = 'new'

        log.info("-------------------------------------")
        if user_input == from_scratch or not user_input:
            user_input = from_scratch
            log.info("Started to scrape all the companies from scratch or get the missed ones.")
        elif user_input == update:
            log.info("Started to update the equity according to the next earning date.")

        while True:

            scraping = ScrapingFundamentals()
            scrape_income_statement = ScrapingIncomeStatement()
            scrape_balance_sheet = ScrapingBalanceSheet()
            scrape_cash_flow = ScrapingCashFlow()
            scrape_ratios = ScrapingRatios()
            scrape_dividends = ScrapingDividends()
            scrape_earnings = ScrapingEarnings()
            scrape_historical_data = ScrapingPrices()

            scraping.instantiate_driver(invisible=invisible_browser)
            #scraping.get_cookies(websites.investing_dot_com)
            scraping.add_cookies(websites.investing_dot_com)
            scrape_income_statement.set_driver(scraping.driver)
            scrape_balance_sheet.set_driver(scraping.driver)
            scrape_cash_flow.set_driver(scraping.driver)
            scrape_ratios.set_driver(scraping.driver)
            scrape_dividends.set_driver(scraping.driver)
            scrape_earnings.set_driver(scraping.driver)
            scrape_historical_data.set_driver(scraping.driver)

            start_time_process_equities = time.monotonic()
            counter_processed_equities = 0

            session_counter = 0

            total_number_of_equities_in_db = len(equities)
            counter_global_equities = 0

            for equity in equities:

                counter_global_equities += 1

                #print(f"TEST: {equity.exchange}:{equity.symbol_1} id: {equity.id}")

                if equity.all_done or equity.country in labels.to_exclude_countries:
                    # Correctly filled up, go on with the next equity.
                    continue
                elif user_input == update:
                    next_earnings_date = equity.overview.next_earnings_date
                    if next_earnings_date > datetime.now().date():
                        continue
                    # elif not next_earnings_date:  # if we do not have earning date update anyway.
                    #     # Need to scrape only if there is an updated income statement, balance sheet or cash flow.
                    #     pass

                if are_there_ethernet_problems(scraping):
                    break

                if not equity_still_exists(equity):
                    continue

                # if not check_there_is_internet_connection():
                #     sys.exit()

                successful = False
                timeout = time.time() + 90  # 1 minutes from now
                while not successful:

                    if time.time() > timeout:
                        time.sleep(5)
                        break

                    session_counter += 1
                    if session_counter > number_maximum_equities_each_session:
                        eth_problems.connection_problems = True
                        session_counter = 0
                        log.error("Session Terminated. Restarting the webdriver.")
                        break

                    # restart_webdriver(scraping, scrape_income_statement, scrape_balance_sheet, scrape_cash_flow,
                    #                   scrape_ratios, scrape_dividends, scrape_earnings, invisible=invisible_browser)

                    scraping.open_website(equity.weblink_1, websites.investing_title)
                    scraping.close_popup_if_present()

                    equity_string_id = f"{equity.exchange}:{equity.symbol_1} id: {equity.id}"
                    log.info(f"opening website of {equity_string_id}")
                    log.info(f"*******               *****        *****")
                    log.info(f"process equity number {counter_global_equities} out of {total_number_of_equities_in_db}")
                    log.info(f"*******               *****        *****")

                    # Check the website was not a "page not found" in that case or de-listed or problems with link.
                    try:
                        scraping.driver.find_element_by_css_selector(f"div[class*='error404']")
                    except Exception as e:
                        pass
                    else:
                        log.info(f"The equity {equity_string_id} seems it cannot be found, could have been delisted!")
                        db_mngr.add_not_found_page_to_equity(equity)
                        continue

                    output = scraping_all(equity, counter_processed_equities, scraping, scrape_income_statement,
                                          scrape_balance_sheet, scrape_cash_flow, scrape_ratios, scrape_dividends,
                                          scrape_earnings, scrape_historical_data)
                    if output == -1:
                        break
                    elif output == -2:
                        continue
                    elif output == -3:
                        pass

                    scraping.set_equity_extraction_completed(equity)
                    counter_processed_equities += 1
                    successful = True

            print_time_spent(start_time_process_equities, counter_processed_equities)
            log.info("Terminated 'run_to_scrape_full_company'.")

    except KeyboardInterrupt as e:
        log.error(f"Scraping interrupted by the user: {e}\n{getDebugInfo()}")
        print_time_spent(start_time_process_equities, counter_processed_equities)

    except Exception as e:
        log.error(f"There is a problem in the code when parsing equity {equity_string_id}!: {e}\n{getDebugInfo()}")


if __name__ == "__main__":
    main()
    pass
