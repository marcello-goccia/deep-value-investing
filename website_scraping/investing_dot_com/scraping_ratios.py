import datetime

from website_scraping.investing_dot_com.scraping_fundamentals import ScrapingFundamentals
from website_scraping.scraping import Scraping
from website_scraping.investing_dot_com.common_investing_com import InvestingPages as links

from data_storing.assets.database_manager import DatabaseManager as db_mngr
from data_storing.assets import tables
from data_storing.assets.common import Benchmark

from utilities.common_methods import getDebugInfo
from utilities.common_methods import Methods as methods
from utilities import log


class ScrapingRatios(ScrapingFundamentals):
    """
    @class ScrapingIncomeStatement
    This method look for the link of all the equities available from the database so that we can
    then extract the income statement data by using the retrieved link.
    """

    def __init__(self):
        """
        @constructor
        Initialises all the needed variables.
        """
        try:
            super(ScrapingRatios, self).__init__()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def retrieve_company_ratios(self, equity):
        """
        @function retrieve_company_ratios
        Retrieves the data from the company financial page of the equity.
        """
        try:
            page_to_open = 'Ratios'
            link_to_open = self.get_correct_link_financials(equity.weblink_1, links.ratios)
            log.info(f"opening {page_to_open}")
            self.open_website(link_to_open)
            self.wait_until_appears_part_of_text_through_my_way('.float_lang_base_1.inlineblock', page_to_open)

            # sometimes rrtable can be with capital t or not
            table = self.loop_locators_to_find_correct_one(links.ratios_locators)

            if not table:
                log.info('It seem the table is not present, it does not matter, move to the next section')
                return

            self.read_ratios_table(equity.id, table)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def read_ratios_table(self, equity_id, table):
        try:
            # it will open the Financial summary
            self.give_web_page_to_beautiful_soup()

            rows = table.findAll(lambda tag: tag.name == 'tr')

            numcols = 0
            for i in rows[0].contents:
                if 'th' in str(i):
                    numcols += 1

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
            ratios = []

            today = datetime.date.today()
            current_period = datetime.date(today.year, today.month, 1)

            for header in header_values[1:]:

                if 'Company' in header:
                    benchmark = Benchmark.company
                elif 'Industry' in header:
                    benchmark = Benchmark.industry
                else:
                    raise Exception("Cannot find the benchmark of the ratios")

                ratios.append(db_mngr.insert_ratios_into_asset(equity_id=equity_id,
                                                               current_period=current_period,
                                                               benchmark=benchmark))

            # deal with the values in the table
            for row in rows[1:]:
                values = [td.text for td in row.findAll('td')]
                if len(values) > numcols:
                    continue

                if len(values) == 1:
                    continue

                self.add_row_to_ratios(ratios, values[0], values[1:])

            db_mngr.commit_to_database()
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def add_row_to_ratios(ratios, field, values):
        try:
            num_ratios = len(ratios)
            assert(num_ratios == len(values))
            assert(len(values) == 2)  # two, 1 for company and 1 for industry

            value_company = values[0]
            value_industry = values[1]

            ScrapingRatios.add_ratio(ratios[0], field=field, value=value_company)
            ScrapingRatios.add_ratio(ratios[1], field=field, value=value_industry)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def add_ratio(ratio_entity, field, value):
        try:
            value = methods.get_valid_value(value)
            if value is None:
                return

            fvalue = methods.convert_to_float(value)

            Scraping.check_ok(tables.ratios.add_single_element(ratio_entity, field=field, value=fvalue),
                                  expected=0, identifier=field)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
