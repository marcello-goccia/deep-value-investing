import datetime

from website_scraping.investing_dot_com.scraping_fundamentals import ScrapingFundamentals
from website_scraping.scraping import Scraping
from website_scraping.investing_dot_com.common_investing_com import InvestingPages as links

from data_storing.assets.database_manager import DatabaseManager as db_mngr
from data_storing.assets.common import MeasureUnit
from data_storing.assets import tables

from utilities.common_methods import getDebugInfo
from utilities.common_methods import Methods as methods
from utilities.common_methods import NA
from utilities import log


class ScrapingIncomeStatement(ScrapingFundamentals):
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
            super(ScrapingIncomeStatement, self).__init__()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def retrieve_company_income_statement(self, equity):
        """
        @function retrieve_company_income_statement
        Retrieves the data from the company financial page of the equity.
        """
        try:
            page_to_open = 'Income Statement'
            link_to_open = self.get_correct_link_financials(equity.weblink_1, links.income_statement)
            log.info(f"opening {page_to_open}")
            self.open_website(link_to_open)
            self.wait_until_appears_part_of_text_through_my_way('.float_lang_base_1.inlineblock', page_to_open)

            self.retrieve_financial(equity.id, 'quarterly')
            self.close_popup_if_present()
            self.retrieve_financial(equity.id, 'annual')

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def read_elements_of_table(self, equity_id, time_span, rows, numcols, header_dates):
        try:
            measure_unit, currency = self.get_measure_unit_and_currency()

            income_statements = []
            for header_date in header_dates:
                if type(header_date) is not datetime.date:
                    income_statements.append(None)
                else:
                    income_statement = db_mngr.insert_income_statement_into_asset(equity_id=equity_id,
                                                        period_length=time_span, period_ending=header_date,
                                                        measure_unit=measure_unit, currency=currency)
                    if not income_statement:
                        income_statements.append(None)
                    else:
                        income_statements.append(income_statement)

            if all(v is None for v in income_statements):
                return

            # deal with the values in the table
            for row in rows[1:]:
                values = [td.text for td in row.findAll('td')]
                if len(values) > numcols:
                    continue

                self.add_row_to_income_statement(income_statements, values[0], values[1:])

            db_mngr.commit_to_database()
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def add_row_to_income_statement(income_statements, field, values):
        try:
            #values = list(filter(lambda v: v not in NA, values))
            num_income_statements = len(income_statements)
            assert(num_income_statements == len(values))

            for i in range(num_income_statements):

                if not income_statements[i]:
                    continue

                value = values[i]

                value = methods.get_valid_value(value)
                if value is None:
                    continue

                try:
                    fvalue = float(value)
                except ValueError:
                    log.error(f"{field}={value} cannot be converted to float")
                    continue

                Scraping.check_ok(tables.income_statement.add_single_element(income_statements[i],
                                                           field=field, value=fvalue), expected=0, identifier=field)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
