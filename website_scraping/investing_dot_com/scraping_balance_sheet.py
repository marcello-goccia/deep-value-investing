import datetime

from website_scraping.investing_dot_com.scraping_fundamentals import ScrapingFundamentals
from website_scraping.scraping import Scraping
from website_scraping.investing_dot_com.common_investing_com import InvestingPages as links

from data_storing.assets.database_manager import DatabaseManager as db_mngr
from data_storing.assets import tables

from utilities.common_methods import getDebugInfo
from utilities.common_methods import Methods as methods
from utilities import log


class ScrapingBalanceSheet(ScrapingFundamentals):
    """
    @class ScrapingBalanceSheet
    This method look for the link of all the equities available from the database so that we can
    then extract the balance sheet data by using the retrieved link.
    """

    def __init__(self):
        """
        @constructor
        Initialises all the needed variables.
        """
        try:
            super(ScrapingBalanceSheet, self).__init__()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def retrieve_company_balance_sheet(self, equity):
        """
        @function retrieve_company_balance_sheet
        Retrieves the data from the company financial page of the equity.
        """
        try:
            page_to_open = 'Balance Sheet'
            link_to_open = self.get_correct_link_financials(equity.weblink_1, links.balance_sheet)
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

            balance_sheets = []
            for header_date in header_dates:
                if type(header_date) is not datetime.date:
                    balance_sheets.append(None)
                else:
                    balance_sheet = db_mngr.insert_balance_sheet_into_asset(equity_id=equity_id,
                                                                    period_length=time_span, period_ending=header_date,
                                                                    measure_unit=measure_unit, currency=currency)
                    if not balance_sheet:
                        balance_sheets.append(None)
                    else:
                        balance_sheets.append(balance_sheet)

            if all(v is None for v in balance_sheets):
                return

            # deal with the values in the table
            for row in rows[1:]:
                values = [td.text for td in row.findAll('td')]
                if len(values) > numcols:
                    continue

                self.add_row_to_balance_sheet(balance_sheets, values[0], values[1:])

            db_mngr.commit_to_database()
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def add_row_to_balance_sheet(balance_sheets, field, values):
        try:
            num_balance_sheets = len(balance_sheets)
            assert(num_balance_sheets == len(values))

            for i in range(num_balance_sheets):

                if not balance_sheets[i]:
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

                Scraping.check_ok(tables.balance_sheet.add_single_element(balance_sheets[i], field=field, value=fvalue),
                                  expected=0, identifier=field)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
