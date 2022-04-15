import time

from datetime import datetime, date

from selenium.common.exceptions import NoSuchElementException

from website_scraping.scraping import Scraping
from website_scraping.investing_dot_com.scraping_investing import ScrapingInvesting
from website_scraping.investing_dot_com.common_investing_com import InvestingPages as links
from website_scraping.investing_dot_com.common_investing_com import Timers as timers

from data_storing.assets.database_manager import DatabaseManager as db_mngr
from data_storing.assets import tables
from data_storing.assets.common import Timespan, MeasureUnit

from utilities.common_methods import getDebugInfo
from utilities.common_methods import Methods as methods
from utilities.common_methods import NA
from utilities import log


class ScrapingFundamentals(ScrapingInvesting):
    """
    @class ScrapingFundamentals
    This method look for the link of all the equities available from the database so that we can
    then extract the fundamental data by using the retrieved link.
    """

    def __init__(self):
        """
        @constructor
        Initialises all the needed variables.
        """
        try:
            super(ScrapingFundamentals, self).__init__()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def retrieve_overview(self, equity):
        """
        @function retrieve_overview
        Retrieves the data from the overview page of the equity.
        """
        try:
            self.give_web_page_to_beautiful_soup()

            last_element = self.look_for_some_element_through_soup('span', 'id', 'last_last')
            last_value = last_element.text
            tables.overview.add_single_element(equity.overview, field='Last', value=last_value)

            substring1 = 'Currency in '
            substring2 = ' ( Disclaimer )'
            overview_box = self.look_for_some_element_through_soup('div', 'class', 'overViewBox')
            text = overview_box.text
            currency = text[(text.index(substring1) + len(substring1)):text.index(substring2)]
            assert(len(currency) == 3)
            tables.overview.add_single_element(equity.overview, field='Currency', value=currency)

            div_tag = self.soup.find_all("div", {"class": "clear overviewDataTable overviewDataTableWithTooltip"})

            if div_tag is None:
                raise Exception("div_tag is for some reason None")

            for tag in div_tag:
                divs = tag.find_all("div", class_="inlineblock")
                for div in divs:
                    try:
                        key = div.contents[0].text  # checking they exist
                        value = div.contents[1].text  # checking they exist
                    except Exception as e:
                        continue

                    value = methods.get_valid_value(value)
                    if value is None:
                        continue

                    if key == 'Shares Outstanding' or \
                            key == 'Next Earnings Date' or \
                            key == 'Market Cap':
                        tables.overview.add_single_element(equity.overview, field=key, value=value)

            db_mngr.commit_to_database()
            pass

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def add_parameter_to_equity(self, equity, parameter, key, value):
        try:
            if parameter in key:
                if 'Employees' in key:
                    value = float(value)
                Scraping.check_ok(tables.equity.add_single_element(equity, parameter, value),
                                  expected=0, identifier=parameter)
            return
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def retrieve_company_profile(self, equity):
        """
        @function retrieve_company_profile
        Retrieves the data from the company profile page of the equity.
        """
        try:
            link_to_open = self.get_correct_link_financials(equity.weblink_1, links.profile)
            self.open_website(link_to_open, 'Company Profile')
            self.wait_until_appears_part_of_text_through_my_way('.float_lang_base_1.inlineblock', 'Company Profile')
            self.give_web_page_to_beautiful_soup()

            div_tag = self.soup.find_all("div", {"class": "companyProfileHeader"})
            for tag in div_tag:
                divs = tag.find_all("div")
                for div in divs:
                    try:
                        key = div.contents[0]  # checking they exist
                        value = div.contents[1].text  # checking they exist
                    except Exception as e:
                        continue

                    value = methods.get_valid_value(value)
                    if value is None:
                        continue

                    self.add_parameter_to_equity(equity, 'Industry', key, value)
                    self.add_parameter_to_equity(equity, 'Sector', key, value)
                    self.add_parameter_to_equity(equity, 'Employees', key, value)
                    self.add_parameter_to_equity(equity, 'Equity Type', key, value)

            try:
                value = self.driver.find_element_by_xpath("//span[@itemprop='addressCountry']").text
            except NoSuchElementException as e:
                value = None
            self.add_parameter_to_equity(equity, 'HQ country',  'HQ country', value)

            try:
                value = self.driver.find_element_by_xpath("//span[@itemprop='telephone']").text
            except NoSuchElementException as e:
                value = None
            self.add_parameter_to_equity(equity, 'Telephone', 'Telephone', value)

            db_mngr.commit_to_database()

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def open_financials(self):
        """
        @function open_financials
        It open the financial page by clicking on the correct link
        """
        try:
            self.try_clicking_on_link("Financials")
            self.close_popup_if_present()
            self.check_page_contains_element("rsdiv")
            self.close_popup_if_present()

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def retrieve_financial(self, equity_id, period_span):
        try:
            if period_span == 'quarterly':
                button = 'Interim'
                time_span = Timespan.quarterly
            elif period_span == 'annual':
                button = 'Annual'
                time_span = Timespan.annual
            else:
                raise Exception('Problems with the definition of the financial period span')

            log.info(f"reading {period_span} financial")

            #######################
            timeout = time.time() + 6  # 1 minutes from now
            while True:
                if time.time() > timeout:
                    break

                element_to_click = None
                for i in range(timers.times_clicking_on_button):
                    try:
                        #element_to_click = self.driver.find_element_by_link_text(period_span.title())
                        #time.sleep(5)
                        element_to_click = self.driver.find_element_by_xpath(f"//a[@data-ptype='{button}']")  # 'Interim' for quarterly
                        break
                    except NoSuchElementException as e:
                        time.sleep(timers.waiting_short)
                        continue
                if not element_to_click:
                    log.info("It seems the table is not present in this page. Going on to the next section.")
                    return

                try:
                    element_to_click.click()
                    break
                except Exception as e:
                    time.sleep(2)
            #######################

            time.sleep(timers.waiting_medium)
            table = self.loop_locators_to_find_correct_one(links.financial_locators)
            self.read_table(equity_id, time_span, table)
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code clicking on {period_span}!: {e}\n{getDebugInfo()}")

    def read_table(self, equity_id, time_span, table):
        try:
            rows = table.findAll(lambda tag: tag.name == 'tr')

            numcols = 0
            for i in rows[0].contents:
                if 'th' in str(i):
                    numcols += 1

            # deal with the period ending dates.
            temp = [th.text for th in rows[0].findAll('th')]
            header_dates = []
            for value in temp:
                if "Period Ending" in value:
                    continue
                elif value in NA or not value:
                    header_dates.append('-')
                else:
                    header_dates.append(datetime.strptime(value, '%Y%d/%m').date())

            self.read_elements_of_table(equity_id, time_span, rows, numcols, header_dates)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_the_table_my_way(self, tag, attrib, attrib_value):
        try:
            self.give_web_page_to_beautiful_soup()
            attempts = timers.times_loop_to_load_page_appears_table
            for i in range(attempts):
                table = self.soup.find(tag, {attrib: attrib_value})
                if table is not None:
                    return table
                log.info(f"trying again to find {attrib}: {attrib_value}")
                self.give_web_page_to_beautiful_soup()
                time.sleep(timers.atomical_sleep)
            return None

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            return None


    def read_elements_of_table(self, equity_id, time_span, rows, numcols, header_dates):
        try:
            pass
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_measure_unit_and_currency(self):
        try:
            text_in_page = self.look_for_some_text_through_webdriver('div', '(except for per share items)').text
            text_in_page = text_in_page.replace('* In ', '')
            text_in_page = text_in_page.replace(' of ', ' ')
            text_in_page = text_in_page.replace(' (except for per share items)', '')
            strings = text_in_page.split()

            num_values = len(strings)

            if not num_values:
                return None, None
            elif num_values == 1:
                measure_unit = strings[0]
                currency = None
            elif num_values == 2:
                measure_unit = strings[0]
                currency = strings[1]
            else:
                raise Exception("problem with reading measure unit and currency")

            if "billion" in measure_unit.lower():
                measure_unit = MeasureUnit.billion
            elif "million" in measure_unit.lower():
                measure_unit = MeasureUnit.million
            elif "thousand" in measure_unit.lower():
                measure_unit = MeasureUnit.thousand
            else:
                measure_unit = MeasureUnit.plain

            return measure_unit, currency
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")



