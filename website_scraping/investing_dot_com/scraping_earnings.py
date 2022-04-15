from datetime import datetime

from website_scraping.investing_dot_com.scraping_fundamentals import ScrapingFundamentals
from website_scraping.scraping import Scraping
from website_scraping.investing_dot_com.common_investing_com import InvestingPages as links

from data_storing.assets.database_manager import DatabaseManager as db_mngr


from utilities.common_methods import Methods as methods
from utilities.common_methods import getDebugInfo
from utilities import log

id_name = 'earningsHistory'


class ScrapingEarnings(ScrapingFundamentals):
    """
    @class ScrapingEarnings
    This method look for the link of all the equities available from the database so that we can
    then extract the earnings data by using the retrieved link.
    """

    def __init__(self):
        """
        @constructor
        Initialises all the needed variables.
        """
        try:
            super(ScrapingEarnings, self).__init__()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def retrieve_company_earnings(self, equity):
        """
        @function retrieve_company_earnings
        Retrieves the data from the company financial page of the equity.
        """
        try:
            page_to_open = 'Earnings'
            link_to_open = self.get_correct_link_financials(equity.weblink_1, links.earnings)
            log.info(f"opening {page_to_open}")
            self.open_website(link_to_open)
            self.wait_until_appears_part_of_text_through_my_way('.float_lang_base_1.inlineblock', page_to_open)

            print(f"debug: earnings.retrieve_company_earnings: going to find all earnings")
            self.click_on_link_until_found("Show more")
            print(f"debug: in earnings.retrieve_company_earnings: finished finding all earnings")

            if self.look_for_some_text_through_webdriver('div', 'No data to display'):
                # Check first the page contains data.
                log.info(f"The equity with id: {equity.id} seems it does not have any earnings")
                return
            else:
                # Otherwise waits for the table to appear.
                self.wait_until_appears_part_of_attribute_through_css("table", "id", id_name)
                self.close_popup_if_present()
                self.read_earnings_table(equity.id)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def read_earnings_table(self, equity_id):
        try:
            self.give_web_page_to_beautiful_soup()

            table = self.look_for_some_element_through_soup('table', 'id', id_name)
            if table is None:
                log.info(f"The equity with id: {equity_id} seems it does not have any earnings")
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
                print(f"debug: in earnings.read_elements_of_table counter: {debug_counter}")

                values = [td.text for td in row.findAll('td')]

                release_date = datetime.strptime(values[0], '%b %d, %Y').date()
                period_end = datetime.strptime(values[1], '%m/%Y').date()

                eps = methods.get_valid_value(values[2])
                eps = methods.convert_to_float(eps)

                eps_forecast = methods.remove_character(values[3], '/')
                if '--' in eps_forecast:
                    eps_forecast = None
                eps_forecast = methods.get_valid_value(eps_forecast)
                eps_forecast = methods.convert_to_float(eps_forecast)

                revenue = methods.get_valid_value(values[4])
                revenue = methods.convert_to_float(revenue)

                revenue_forecast = methods.remove_character(values[5], '/')
                if '--' in revenue_forecast:
                    revenue_forecast = None
                revenue_forecast = methods.get_valid_value(revenue_forecast)
                revenue_forecast = methods.convert_to_float(revenue_forecast)

                # if the earning is already present in the database, we do not insert them and break
                inserted = db_mngr.insert_earning_into_asset(equity_id,
                                                             release_date=release_date,
                                                             period_end=period_end,
                                                             eps=eps,
                                                             eps_forecast=eps_forecast,
                                                             revenue=revenue,
                                                             revenue_forecast=revenue_forecast)
                if not inserted:
                    break
            db_mngr.commit_to_database()
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
