from datetime import datetime

from website_scraping.investing_dot_com.scraping_fundamentals import ScrapingFundamentals
from website_scraping.scraping import Scraping
from website_scraping.investing_dot_com.common_investing_com import InvestingPages as links

from data_storing.assets.database_manager import DatabaseManager as db_mngr
from data_storing.assets.common import DividendType

from utilities.common_methods import getDebugInfo
from utilities.common_methods import Methods as methods
from utilities import log

id_name = 'dividendsHistoryData'


class ScrapingDividends(ScrapingFundamentals):
    """
    @class ScrapingDividends
    This method look for the link of all the equities available from the database so that we can
    then extract the dividends data by using the retrieved link.
    """

    def __init__(self):
        """
        @constructor
        Initialises all the needed variables.
        """
        try:
            super(ScrapingDividends, self).__init__()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def retrieve_company_dividends(self, equity):
        """
        @function retrieve_company_dividends
        Retrieves the data from the company financial page of the equity.
        """
        try:
            page_to_open = 'Dividends'
            link_to_open = self.get_correct_link_financials(equity.weblink_1, links.dividends)
            log.info(f"opening {page_to_open}")
            self.open_website(link_to_open)
            self.wait_until_appears_part_of_text_through_my_way('.float_lang_base_1.inlineblock', page_to_open)

            print(f"debug: dividends.retrieve_company_dividends: going to find all dividends")
            self.click_on_link_until_found("Show more")
            print(f"debug: in dividends.retrieve_company_dividends: finished finding all dividends")

            if self.look_for_some_text_through_webdriver('div', 'No data to display'):
                # Check first the page contains data.
                log.info(f"The equity with id: {equity.id} seems it does not have any dividends")
                return
            else:
                # Otherwise waits for the table to appear.
                self.wait_until_appears_part_of_attribute_through_css("table", "id", id_name)
                self.close_popup_if_present()
                self.read_dividends_table(equity.id)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def read_dividends_table(self, equity_id):
        try:
            self.give_web_page_to_beautiful_soup()

            table = self.look_for_some_element_through_soup('table', 'id', id_name)
            if table is None:
                log.info(f"The equity with id: {equity_id} seems it does not have any dividends")
                return

            rows = table.findAll(lambda tag: tag.name == 'tr')

            numcols = len(self.driver.find_elements_by_xpath(f"//table[@id='{table.attrs['id']}']/thead/tr/th"))

            # deal with the period ending dates.
            temp = [th.text for th in rows[0].findAll('th')]
            header_values = []
            for value in temp:
                header_values.append(value)

            self.read_elements_of_table(equity_id, '', rows, numcols, header_values)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def read_elements_of_table(self, equity_id, time_span, rows, numcols, header_values):
        try:
            debug_counter = 0
            for row in rows[1:]:

                debug_counter += 1
                print(f"debug: in dividends.read_elements_of_table counter: {debug_counter}")

                values = [td.text for td in row.findAll('td')]

                if values[0] != '--':
                    ex_dividend_date = datetime.strptime(values[0], '%b %d, %Y').date()
                else:
                    ex_dividend_date = None

                dividend_value = methods.get_valid_value(values[1])
                dividend_value = methods.convert_to_float(dividend_value)

                dividend_type = row.contents[5].contents[1]['title']
                dividend_type = dividend_type.replace('_', '')
                if dividend_type == 'Monthly':
                    dividend_type = DividendType.monthly
                elif dividend_type == u'Quarterly':
                    dividend_type = DividendType.quarterly
                elif dividend_type == u'Semi-Annual':
                    dividend_type = DividendType.semiannual
                elif dividend_type == u'Annual':
                    dividend_type = DividendType.annual
                elif dividend_type == u'Trailing Twelve Months':
                    dividend_type = DividendType.ttm

                if values[3] != '--':
                    payment_date = datetime.strptime(values[3], '%b %d, %Y').date()
                else:
                    payment_date = None

                yield_value = methods.get_valid_value(values[4])
                yield_value = methods.remove_character(yield_value, '%')
                yield_value = methods.convert_to_float(yield_value)
                yield_value = methods.from_percent_to_decimal(yield_value)

                if yield_value is None:
                    pass

                # if the dividend is already present in the database, we do not insert them and break
                inserted = db_mngr.insert_dividend_into_asset(equity_id,
                                                              ex_dividend_date=ex_dividend_date,
                                                              dividend_value=dividend_value,
                                                              dividend_type=dividend_type,
                                                              payment_date=payment_date,
                                                              yield_value=yield_value)
                if not inserted:
                    break
            db_mngr.commit_to_database()
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
