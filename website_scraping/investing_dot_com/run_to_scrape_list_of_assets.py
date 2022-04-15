import time
import os
import sys
from datetime import datetime
from utilities.log import root_folder_all_code

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_root = dir_path.split(root_folder_all_code, 1)[0]
code_path = os.path.join(dir_root, root_folder_all_code)
sys.path.insert(0, code_path)

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from utilities.common_methods import getDebugInfo
from utilities.common_methods import Methods as methods
from utilities import log

from website_scraping.investing_dot_com.scraping_investing import ScrapingInvesting
from utilities.globals import websites

from website_scraping.investing_dot_com.assets_labels import Labels as labels

# inserting into the database
from data_storing.assets.database_manager import DatabaseManager as db_mngr
from data_storing.assets import tables

name_table_equities = "resultsTable"


class ScrapingAssets(ScrapingInvesting):
    """
    @class ScrapingAssets
    This method look for the link of all the equities available from the website so that we can
    then extract the fundamental data by using the retrieved link.
    """

    def __init__(self):
        """
        @constructor
        Initialise all the needed variables.
        """
        try:
            super(ScrapingAssets, self).__init__()

            self.current_country = u''
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_list_available_countries(self):
        """
        @function get_list_available_countries
        The method finds the list of all the available countries and their code.
        So that we can choose the country and send the corresponding code.
        """
        list_countries_1 = self.look_for_some_element_through_webdriver('ul', 'id', 'countriesUL')
        self.give_web_page_to_beautiful_soup()
        available_countries = self.look_for_some_element_through_soup('ul', 'id', 'countriesUL')
        rows = available_countries.findAll(lambda tag: tag.name == 'li')

        countries_list = {}
        for row in rows:
            country_code = row.attrs['data-value']
            country_code = methods.get_valid_value(country_code)

            country_name = row.text
            country_name = methods.get_valid_value(country_name)

            countries_list[country_name] = country_code

        return countries_list

    @staticmethod
    def get_screener_link(country_code, exchange=''):
        """
        @function get_screener_link
        The method finds the list of all the available countries and their code.
        So that we can choose the country and send the corresponding code.
        """
        if exchange:
            exchange = ''.join(['|exchange::', exchange])

        weblink = ''.join([websites.investing_screener, '/?sp=country::', country_code, '|sector::a',
                           '|industry::a', '|equityType::a', exchange, '%3Ceq_market_cap;'])
        return weblink

    def select_equities_screener_by_country(self, country):
        """
        @function select_equities_screener_by_country
        The method selects from the drop-down menu the chosen country from which we want to retrieve
        the equities.
        """
        try:
            self.current_country = country

            self.close_popup_if_present()
            select_country = self.driver.find_element(By.XPATH, "//input[@placeholder='Select country']")
            self.close_popup_if_present()
            select_country.click()
            self.close_popup_if_present()
            select_country.clear()
            self.close_popup_if_present()
            select_country.send_keys(country)
            time.sleep(0.5)
            self.close_popup_if_present()
            select_country.send_keys(Keys.DOWN)
            time.sleep(0.5)
            self.close_popup_if_present()
            select_country.send_keys(Keys.RETURN)
            self.close_popup_if_present()
            self.wait_until_element_appears_through_id(name_table_equities)
            self.close_popup_if_present()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def select_equities_by_exchange(self, exchange):
        """
        @function select_equities_by_exchange
        The method select from the drop-down menu the chose exchange from which we want to retrieve
        the equities.
        """
        try:
            self.close_popup_if_present()
            select_country = self.driver.find_element(By.XPATH, "//input[@placeholder='Select Exchange']")
            self.close_popup_if_present()
            select_country.click()
            self.close_popup_if_present()
            select_country.clear()
            self.close_popup_if_present()
            select_country.send_keys(exchange)
            time.sleep(0.5)
            self.close_popup_if_present()
            select_country.send_keys(Keys.DOWN)
            time.sleep(0.5)
            self.close_popup_if_present()
            select_country.send_keys(Keys.RETURN)
            self.close_popup_if_present()
            self.wait_until_element_appears_through_id(name_table_equities)
            self.close_popup_if_present()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_number_of_pages_of_equities(self):
        """
        @function get_number_of_pages_of_equities
        The method returns the number of pages where the all equities from a country or from an
        exchange are stored.
        @return the number of pages found.
        """
        try:
            key_word = "js-total-results"
            number_equities_per_page = 50

            self.close_popup_if_present()
            total_results = self.driver.find_element(By.CLASS_NAME, key_word)
            total_results = int(total_results.text)
            leftover_page = int(total_results % number_equities_per_page > 0)
            number_of_pages = int(total_results / number_equities_per_page) + leftover_page
            log.info(f"Found {total_results} equities, overall in {number_of_pages} pages")
            return number_of_pages
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def click_on_the_link_next_page(self, current_page):
        """
        @function click_on_the_link_next_page
        The method clicks on the link to open the next page of equities
        """
        try:
            keyword = u'pagination selected'
            page_selected = int(self.driver.find_element_by_xpath(f"//a[@class='{keyword}']").text)
            time.sleep(0.5)

            max_counter = 6

            for i in range(max_counter):

                try:
                    next_page = self.driver.find_element_by_link_text(u'Next')
                except NoSuchElementException as e:
                    log.info("next not found, trying again.")
                    self.close_popup_if_present()
                    continue

                try:
                    next_page.click()
                except Exception as e:
                    log.info("cannot click try again")
                    self.close_popup_if_present()

                time.sleep(1)
                self.wait_until_element_appears_through_id(name_table_equities)
                new_page_selected = int(self.driver.find_element_by_xpath(f"//a[@class='{keyword}']").text)
                if new_page_selected == (page_selected + 1):
                    log.info(f"going to the next page, page number {new_page_selected}")
                    break
                elif new_page_selected > (page_selected + 1):
                    raise Exception("I have gone to far!!")
                else:
                    log.info("trying clicking next again!")

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def click_on_the_link_clear_all(self):  # example 'Next' or 'Clear All'
        """
        @function open_next_equities_page
        The method clicks on the link to open the page defined by the text as input
        """
        try:
            max_counter = 6

            for i in range(max_counter):
                self.close_popup_if_present()
                try:
                    clear_all = self.driver.find_element_by_link_text("Clear All")
                except Exception as e:
                    log.error("trying again looking for the clear all button")
                    continue
                try:
                    clear_all.click()
                    self.wait_until_element_appears_through_id(name_table_equities)
                    break
                except Exception as e:
                    log.error("trying again to click on the clear all button")
                    pass
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_info_from_table(self):
        """
        @function get_info_from_table
        Function to fill up the table of equities retrieved from the page of the website.
        """
        try:
            all_tables_from_web_page = self.soup.find_all('table', {'id': name_table_equities})

            for table in all_tables_from_web_page:
                ScrapingAssets.retrieve_table(table, self.current_country)

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def retrieve_table(input_table, current_country):
        try:
            rows = input_table.findAll(lambda tag: tag.name == 'tr')

            # # Getting the headers
            # rows[0] has the headers of all the summary of an equity
            # print(rows[0].text)
            header_labels = [th.text for th in rows[0].findAll('th')]

            # each row is a single company
            for row in rows[1:]:
                columns = row.find_all('td')

                info = ScrapingAssets.get_company_company_info(columns)

                # create asset with the dictionary info just retrieved.
                equity = db_mngr.insert_equity_into_asset(symbol_1=info['symbol'], name=info['company'],
                                                          weblink_1=info['link'], exchange=info['exchange'],
                                                          sector=info['sector'], industry=info['industry'],
                                                          country=current_country)
                if not columns:
                    continue

                if len(header_labels) != len(columns):
                    raise Exception("Something wrong, the header labels are not in the same number as the columns.")

                tables.overview.add_single_element(equity.overview, field="Date", value=datetime.now().date())

                for field, value in zip(header_labels[6:], columns[6:]):

                    value = methods.get_valid_value(value.text)

                    if not field or not value:
                        continue

                    tables.overview.add_single_element(equity.overview, field=field, value=value)

                db_mngr.commit_to_database()

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def get_company_company_info(columns):

        try:
            link = None
            company = None
            symbol = None
            exchange = None
            sector = None
            industry = None

            for cell in columns:

                #check all filled:
                if link is not None \
                        and company is not None \
                        and symbol is not None \
                        and exchange is not None \
                        and sector is not None \
                        and industry is not None:
                    break

                if 'data-column-name' in cell.attrs:
                    if cell.attrs['data-column-name'] == 'name_trans':
                        if cell.a is not None:
                            link = websites.investing_dot_com + cell.a['href']
                            company = cell.a['title']
                            text = cell.get_text()  # columns
                            continue
                    if cell.attrs['data-column-name'] == 'viewData.symbol':
                        symbol = cell.text
                        continue
                    if cell.attrs['data-column-name'] == 'exchange_trans':
                        exchange = cell.text
                        continue
                    if cell.attrs['data-column-name'] == 'sector_trans':
                        sector = cell.text
                        continue
                    if cell.attrs['data-column-name'] == 'industry_trans':
                        industry = cell.text
                        continue

            company_info = {'company': company, 'symbol': symbol, 'link': link, 'exchange': exchange,
                            'sector': sector, 'industry': industry}
            return company_info
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            return None


def scan_through_screener_pages(scraping, weblink):
    try:
        scraping.open_link_list_of_assets(weblink + '1')

        num_pages = scraping.get_number_of_pages_of_equities()

        for i in range(num_pages):
            current_page = i + 1
            if current_page != 1:
                scraping.open_link_list_of_assets(weblink + str(current_page))
            scraping.give_web_page_to_beautiful_soup()
            log.info(f"Getting info from page {current_page}")
            scraping.get_info_from_table()

        log.info("Successfully scraped the country equities.")

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")


def main():
    try:
        log.info("-------------------------------------")
        log.info("Started 'run_to_scrape_list of assets'.")
        start_time_process_equities = time.monotonic()

        scraping = ScrapingAssets()
        scraping.instantiate_driver(invisible=True)
        scraping.open_website(websites.investing_screener, websites.investing_title)

        countries_list = scraping.get_list_available_countries()

        for current_country in labels.countries:

            country_code = countries_list[current_country]
            scraping.current_country = current_country

            log.info("")
            log.info("#######################################")
            log.info(f"selected the country: {current_country}")

            if current_country == u'United States':
                for exchange in labels.us_exchanges:
                    log.info(f"selected the exchange {exchange}")
                    weblink = scraping.get_screener_link(country_code, exchange)
                    scan_through_screener_pages(scraping, weblink)
                continue

            elif current_country == u'Germany':
                for exchange in labels.de_exchanges:
                    log.info(f"selected the exchange {exchange}")
                    weblink = scraping.get_screener_link(country_code, exchange)
                    scan_through_screener_pages(scraping, weblink)
                continue

            weblink = scraping.get_screener_link(country_code)
            scan_through_screener_pages(scraping, weblink)

        elapsed_time_process_equities = time.monotonic() - start_time_process_equities
        message = f"Terminated: the time spent to retrieve all the equities links is {elapsed_time_process_equities}"
        log.info(message)

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")


if __name__ == "__main__":
    main()
    pass

"""
# name
# symbol
# exchange
# sector
# industry
last
change_perc
market_cap
volumes
pe_ratio
macd_12_26_1d
revenue
average_vol_3m
eps
beta
dividend
dividend_yield
fifteen_minutes_sentiment
hourly_sentiment
daily_sentiment
weekly_sentiment
monthly_sentiment
daily_return
one_week_return
one_month_return
ytd_return
one_year_return
three_years_return
one_year_change
dividend_yield_perc
pe_ratio_ttm
price_to_sales_ttm
price_to_cash_flow_mrq
price_to_free_cash_flow_ttm
price_to_book_mrq
price_to_tangible_book_mrq
eps_mrq_vs_qtr_1_yr_ago
eps_ttm_vs_ttm_1_yr_ago
five_year_eps_growth
sales_mrq_vs_qtr_1_yr_ago
sales_ttm_vs_ttm_1_yr_ago_ttm
five_year_sales_growth
five_year_capital_spending_growth
asset_turnover_ttm
inventory_turnover_ttm
revenue_employee_ttm
net_income_employee_ttm
receivable_turnover_ttm
fiftytwo_wk_range_high
fiftytwo_wk_range_low
perc_change_from_52_wk_high
perc_change_from_52_wk_low
previous_month_perc_change
gross_margin_ttm
gross_margin_5ya
operating_margin_ttm
operating_margin_5ya
pretax_margin_ttm
pretax_margin_5ya
net_profit_margin_ttm
net_profit_margin_5ya
quick_ratio_mrq
current_ratio_mrq
lt_debt_to_equity_mrq
total_debt_to_equity
dividend_yield_5_year_avg
dividend_growth_rate
payout_ratio
adx_14_1d
atr_14_1d
bull_bear_power_13_1d
cci_14_1d
highs_lows_14_1d
roc_1d
rsi_14_1d
stoch_14_1d
stochrsi_14_1d
ultimate_oscillator_14_1d
williams_perc_R_1d



# Name
# Symbol
# Exchange
# Sector
# Industry
Last
Chg. %
Market Cap
Vol.
P/E Ratio
MACD (12,26 / 1D)
Revenue
Average Vol. (3m)
EPS
Beta
Dividend
Yield
15 Minutes
Hourly
Daily
Weekly
Monthly
Daily
1 Week
1 Month
YTD
1 Year
3 Years
1-Year Change
Dividend Yield (%)
P/E Ratio (TTM)
Price to Sales (TTM)
Price to Cash Flow (MRQ)
Price to Free Cash Flow (TTM)
Price to Book (MRQ)
Price to Tangible Book (MRQ)
EPS(MRQ) vs Qtr. 1 Yr. Ago
EPS(TTM) vs TTM 1 Yr. Ago
5 Year EPS Growth
Sales (MRQ) vs Qtr. 1 Yr. Ago
Sales (TTM) vs TTM 1 Yr. Ago (TTM)
5 Year Sales Growth
5 Year Capital Spending Growth
Asset Turnover (TTM)
Inventory Turnover (TTM)
Revenue/Employee (TTM)
Net Income/Employee (TTM)
Receivable Turnover (TTM)
52 wk Range - High
52 wk Range - Low
% Change from 52 wk High
% Change from 52 wk Low
Previous Month % Change
Gross margin (TTM)
Gross Margin (5YA)
Operating margin (TTM)
Operating margin (5YA)
Pretax margin (TTM)
Pretax margin (5YA)
Net Profit margin (TTM)
Net Profit margin (5YA)
Quick Ratio (MRQ)
Current Ratio (MRQ)
LT Debt to Equity (MRQ)
Total Debt to Equity
Dividend Yield 5 Year Avg.
Dividend Growth Rate
Payout Ratio
ADX (14 / 1D)
ATR (14 / 1D)
Bull/Bear Power (13 / 1D)
CCI (14 / 1D)
Highs/Lows (14 / 1D)
ROC (1D)
RSI (14 / 1D)
STOCH (14 / 1D)
STOCHRSI (14 / 1D)
Ultimate Oscillator (14 /1D)
Williams %R (1D)
"""

"""
Name = Ahli United Bank
Symbol = AUBB
Exchange = Bahrain
Sector = Financial
Industry = Regional Banks
Last = 0.835
Chg. % = 1.21%
Market Cap = 7.31B
Vol. = 797.60K
P/E Ratio = 11.03
MACD (12,26 / 1D) = 0.02
Revenue = 990.16M
Average Vol. (3m) = 3.18M
EPS = 0.08
Beta = 1.49
Dividend = 0.04
Yield = -
15 Minutes = -
Hourly = -
Daily = Strong Buy
Weekly = Strong Buy
Monthly = Strong Buy
Daily = 1.21
1 Week = 0.60
1 Month = 10.74
YTD = 34.03
1 Year = 45.72
3 Years = 58.14
1-Year Change = 48.05
Dividend Yield (%) = 4.67%
P/E Ratio (TTM) = 11.03
Price to Sales (TTM) = 6.02
Price to Cash Flow (MRQ) = 3.47
Price to Free Cash Flow (TTM) = 2.97
Price to Book (MRQ) = 1.62
Price to Tangible Book (MRQ) = 1.82
EPS(MRQ) vs Qtr. 1 Yr. Ago = 8.66
EPS(TTM) vs TTM 1 Yr. Ago = 11.70
5 Year EPS Growth = 1.33
Sales (MRQ) vs Qtr. 1 Yr. Ago = 13.72
Sales (TTM) vs TTM 1 Yr. Ago (TTM) = 20.05
5 Year Sales Growth = 8.65
5 Year Capital Spending Growth = 7.35
Asset Turnover (TTM) = -
Inventory Turnover (TTM) = -
Revenue/Employee (TTM) = -
Net Income/Employee (TTM) = -
Receivable Turnover (TTM) = -
52 wk Range - High = 0.85
52 wk Range - Low = 0.527
% Change from 52 wk High = -1.76
% Change from 52 wk Low = 58.44
Previous Month % Change = 7.91%
Gross margin (TTM) = -
Gross Margin (5YA) = -
Operating margin (TTM) = 65.43
Operating margin (5YA) = 59.59
Pretax margin (TTM) = 65.43
Pretax margin (5YA) = 59.59
Net Profit margin (TTM) = 61.83
Net Profit margin (5YA) = 55.62
Quick Ratio (MRQ) = -
Current Ratio (MRQ) = -
LT Debt to Equity (MRQ) = 4.27
Total Debt to Equity = 44.91
Dividend Yield 5 Year Avg. = 6.42
Dividend Growth Rate = 7.00
Payout Ratio = 60.30
ADX (14 / 1D) = 45.36
ATR (14 / 1D) = 0.01
Bull/Bear Power (13 / 1D) = 0.03
CCI (14 / 1D) = 73.80
Highs/Lows (14 / 1D) = 0.01
ROC (1D) = 5.56
RSI (14 / 1D) = 68.45
STOCH (14 / 1D) = 70.76
STOCHRSI (14 / 1D) = 18.60
Ultimate Oscillator (14 /1D) = 59.22
Williams %R (1D) = -25.00
"""