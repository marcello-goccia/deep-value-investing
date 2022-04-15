import time
# import csv
from datetime import datetime
from datetime import date

# import fundamentals.miscellaneous as fund_utils

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By

from website_scraping.investing_dot_com.scraping_fundamentals import ScrapingFundamentals
from website_scraping.scraping import Scraping
from website_scraping.investing_dot_com.common_investing_com import InvestingPages as links

from data_storing.assets.database_manager import DatabaseManager as db_mngr

from utilities.common_methods import Methods as methods
from utilities.common_methods import getDebugInfo
from utilities import log

id_name = ''


class ScrapingPrices(ScrapingFundamentals):
    """
    @class ScrapingEarnings
    This method look for the link of all the equities available from the database so that we can
    then extract the historical data data by using the retrieved link.
    """

    def __init__(self):
        """
        @constructor
        Initialises all the needed variables.
        """
        try:
            super(ScrapingPrices, self).__init__()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def open_historical_date_page(self, equity):
        """
        @function open_historical_date_page
        It opens the page with the historical data and if checks if the page
        has successfully open.
        """
        try:
            page_to_open = 'Historical Data'
            link_to_open = self.get_correct_link_financials(equity.weblink_1, links.prices)
            log.info(f"opening {page_to_open}")
            self.open_website(link_to_open)
            self.wait_until_appears_part_of_text_through_my_way('.float_lang_base_1.inlineblock', page_to_open)
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def retrieve_company_historical_data(self, equity):
        """
        @function retrieve_company_historical_data
        Retrieves the data from the company financial page of the equity.
        """
        try:
            self.open_historical_date_page(equity)

            table = self.loop_locators_to_find_correct_one(links.prices_locators)
            self.read_historical_data_table(equity.id, table)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def retrieve_monthly_company_historical_data(self, equity, starting_date=None, update_prices=True):
        """
        The method retrieves the montly historical data of the company passed as input variable
        @param equity the equity to retrieve the historical data
        @param starting_date the date when to start scrpaing prices
        @param update_prices is false the prices will not be updated.
        @return Nothing
        """
        try:
            default_start_date_str = "01/01/2014"
            date_time_obj = datetime.strptime(default_start_date_str, "%m/%d/%Y").date()

            if not update_prices:
                return

            if equity.prices:
                # if some prices are available
                from datetime import date
                newest_date = max(equity.prices, key=lambda price: price.day)
                oldest_date = min(equity.prices, key=lambda price: price.day)

                # get the correct latest date
                starting_date = newest_date.day.strftime("%m/01/%Y")
                db_mngr.delete_item(newest_date)

                # check we effectively have the dates starting from the default_start_date_str
                if oldest_date.day > date_time_obj:
                    # if not get it again!
                    db_mngr.delete_list_of_items(equity.prices)

            if not starting_date:
                starting_date = default_start_date_str

            self.open_historical_date_page(equity)

            # set the monthly prices
            self.driver.find_element_by_xpath("//select[@id='data_interval']/option[text()='Monthly']").click()

            # set the starting date for the prices to a few years ago
            self.download_all_historical_date(starting_date=starting_date, download=False)

            table = self.loop_locators_to_find_correct_one(links.prices_locators)
            self.read_historical_data_table(equity.id, table)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def read_historical_data_table(self, equity_id, table):
        try:

            rows = table.findAll(lambda tag: tag.name == 'tr')

            numcols = 0
            for i in rows[0].contents:
                if 'th' in str(i):
                    numcols += 1

            # deal with the period ending dates.
            header_labels = [th.text for th in rows[0].findAll('th')]

            self.read_elements_of_table(equity_id, '', rows, numcols, header_labels)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def read_elements_of_table(self, equity_id, time_span, rows, numcols, header_labels):
        try:
            for row in rows[1:]:
                values = [td.text for td in row.findAll('td')]

                if 'No results found' in values:
                    return

                # Date
                index = 0
                day = None
                if 'Date' in header_labels[index]:
                    try:
                        # try different kind of dates
                        day = datetime.strptime(values[index], '%b %d, %Y').date()
                    except ValueError:
                        day = datetime.strptime(values[index], '%b %y').date()

                # Price
                index = 1
                close_price = None
                if 'Price' in header_labels[index]:
                    close_price = methods.get_valid_value(values[index])
                    close_price = methods.convert_to_float(close_price)

                # Open
                index = 2
                open_price = None
                if 'Open' in header_labels[index]:
                    open_price = methods.get_valid_value(values[index])
                    open_price = methods.convert_to_float(open_price)

                # High
                index = 3
                high_price = None
                if 'High' in header_labels[index]:
                    high_price = methods.get_valid_value(values[index])
                    high_price = methods.convert_to_float(high_price)

                # Low
                index = 4
                low_price = None
                if 'Low' in header_labels[index]:
                    low_price = methods.get_valid_value(values[index])
                    low_price = methods.convert_to_float(low_price)

                #Volume
                index = 5
                volume = None
                if 'Vol' in header_labels[index]:
                    volume = methods.get_valid_value(values[index])
                    volume = methods.convert_to_float(volume)

                db_mngr.insert_price_into_asset(equity_id,
                                                day=day,
                                                close=close_price,
                                                open=open_price,
                                                high=high_price,
                                                low=low_price,
                                                volume=volume)
            db_mngr.commit_to_database()
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def get_historical_date_csv_file(path_original_csv, path_reversed_csv, equity=None, dates=None):
        try:
            with open(path_original_csv) as f, open(path_reversed_csv, 'w') as fout:
                # reverse the file
                headers = f.readline()
                reversed_lines = list(reversed(f.readlines()))

                if not reversed_lines:
                    log.error(f"Some problem? I could not read anything from file {path_original_csv}")
                    return False

                reversed_lines.pop(0)
                fout.writelines(headers)
                fout.writelines(reversed_lines)
            return True

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

        # try:
        #     starting_date = dates['start_date_str']
        #     ending_date = dates['end_date_str']
        #
        #     timeout = time.time() + 60  # 1 minutes from now
        #     while True:
        #         self.open_historical_date_page(equity)
        #         # set the monthly prices
        #         self.driver.find_element_by_xpath("//select[@id='data_interval']/option[text()='Weekly']").click()
        #         self.download_all_historical_date(starting_date=starting_date, ending_date=ending_date)
        #
        #         if time.time() > timeout:
        #             return False
        #
        #         try:
        #             with open(path_original_csv) as f, open(path_reversed_csv, 'w') as fout:
        #                 # reverse the file
        #                 headers = f.readline()
        #                 reversed_lines = list(reversed(f.readlines()))
        #
        #                 if not reversed_lines:
        #                     log.error(f"Timing issue? I could not read anything from file {path_original_csv}")
        #                     return False
        #
        #                 reversed_lines.pop(0)
        #                 fout.writelines(headers)
        #                 fout.writelines(reversed_lines)
        #             return True
        #
        #         except IOError:
        #             continue
        # except Exception as e:
        #     log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

        # try:
        #     destination_path = path_reversed_csv
        #
        #     with open(destination_path, mode='w') as file_out:
        #
        #         file_writer = csv.writer(file_out, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        #
        #         header = ['Date', 'Price', 'Open', 'High', 'Low Vol.', 'Change %']
        #         file_writer.writerow(header)
        #
        #         for price in equity.prices:
        #             if dates['start_date'] <= price.day <= dates['end_date']:
        #                 price_date = price.day.strftime('%b %d, %Y')
        #                 closep = str(methods.validate(price.close))
        #                 openp = str(methods.validate(price.open))
        #                 highp = str(methods.validate(price.high))
        #                 lowp = str(methods.validate(price.low))
        #                 volume = str(methods.validate(price.volume))
        #                 change = '0.0%'
        #                 file_writer.writerow([price_date, closep, openp, highp, lowp, volume, change])
        #         return True
        #
        # except Exception as e:
        #     log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
        #     return False

    def download_all_historical_date(self, starting_date='', ending_date='', download=True):
        try:
            timing = 1
            actions = ActionChains(self.driver)

            if not starting_date:
                starting_date = "1/1/2000"

            time.sleep(0.1)
            link_text = self.driver.find_element_by_id('widgetFieldDateRange')
            actions.move_to_element(link_text)
            actions.click(link_text)
            actions.perform()
            time.sleep(timing)

            tag = 'input'
            attribute = 'id'
            value = 'startDate'
            input = self.driver.find_element_by_css_selector(f"{tag}[{attribute}*='{value}']")
            input.clear()
            input.send_keys(starting_date)  # input.send_keys("01/01/2014")
            time.sleep(timing)

            if ending_date:  # if the ending date variable is defined
                value = 'endDate'
                input = self.driver.find_element_by_css_selector(f"{tag}[{attribute}*='{value}']")
                input.clear()
                input.send_keys(ending_date)
                time.sleep(timing)

            #self.driver.find_elements_by_xpath("//a[@id='applyBtn' and @value='Python']")[0]
            apply_button = self.driver.find_elements_by_xpath("//a[@id='applyBtn']")[0]
            apply_button.click()
            time.sleep(timing)

            if download:
                tag = 'a'
                attribute = 'title'
                value = 'Download Data'
                download = self.driver.find_element_by_css_selector(f"{tag}[{attribute}*='{value}']")
                actions.move_to_element(download)
                actions.click(download)
                actions.perform()
                time.sleep(timing)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

