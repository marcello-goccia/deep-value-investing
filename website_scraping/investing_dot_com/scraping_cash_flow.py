import datetime

from website_scraping.investing_dot_com.scraping_fundamentals import ScrapingFundamentals
from website_scraping.scraping import Scraping
from website_scraping.investing_dot_com.common_investing_com import InvestingPages as links

from data_storing.assets.database_manager import DatabaseManager as db_mngr
from data_storing.assets import tables

from utilities.common_methods import getDebugInfo
from utilities.common_methods import Methods as methods
from utilities import log


class ScrapingCashFlow(ScrapingFundamentals):
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
            super(ScrapingCashFlow, self).__init__()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def retrieve_company_cash_flow(self, equity):
        """
        @function retrieve_company_cash_flow
        Retrieves the data from the company financial page of the equity.
        """
        try:
            page_to_open = 'Cash Flow'
            link_to_open = self.get_correct_link_financials(equity.weblink_1, links.cash_flow)
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

            cash_flows = []
            for header_date in header_dates:
                if type(header_date) is not datetime.date:
                    cash_flows.append(None)
                else:
                    cash_flow = db_mngr.insert_cash_flow_into_asset(equity_id=equity_id,
                                                        period_length=time_span, period_ending=header_date,
                                                        measure_unit=measure_unit, currency=currency)
                    if not cash_flow:
                        cash_flows.append(None)
                    else:
                        cash_flows.append(cash_flow)

            if all(v is None for v in cash_flows):
                return

            # deal with the Period Length.
            durations = [th.text for th in rows[1].findAll('th')]
            self.add_row_to_cash_flow(cash_flows, durations[0], durations[1:])

            # deal with the values in the table
            for row in rows[2:]:
                values = [td.text for td in row.findAll('td')]
                if len(values) > numcols:
                    continue

                self.add_row_to_cash_flow(cash_flows, values[0], values[1:])

            db_mngr.commit_to_database()
        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def add_row_to_cash_flow(cash_flows, field, values):
        try:
            num_cash_flows = len(cash_flows)
            assert(num_cash_flows == len(values))

            for i in range(num_cash_flows):

                if cash_flows[i] is None:
                    continue

                value = values[i]

                value = methods.get_valid_value(value)
                if value is None:
                    continue

                if "Period Length" in field:
                    tables.cash_flow.add_single_element(cash_flows[i], field=field, value=value)
                    continue

                try:
                    fvalue = float(value)
                except ValueError:
                    log.error(f"{field}={value} cannot be converted to float")
                    continue

                tables.cash_flow.add_single_element(cash_flows[i], field=field, value=fvalue)

        except Exception as e:
            Scraping.exception_raised = True
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

