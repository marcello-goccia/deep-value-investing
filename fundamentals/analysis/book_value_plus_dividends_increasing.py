import fundamentals.miscellaneous as fund_utils
from data_storing.assets.common import Timespan
from utilities.common_methods import getDebugInfo
from colorama import Fore, Back, Style
from utilities import log
from utilities.common_methods import Methods as methods


class BookValuePlusDividendsIncreasing:
    """
    class BookValuePlusDividendsIncreasing
    It checks if the total equity (book value) plus the total cash dividends paid is increasing by a certain
    percentage each year.
    Book value can be found in the balance sheet, dividends in the cash flow statement.
    """
    @staticmethod
    def is_met(equity):
        try:
            balance_sheets = equity.fundamentals.balance_sheet
            cash_flows = equity.fundamentals.cash_flow

            # sort the equities according to the ending year.
            balance_sheets.sort(key=lambda x: x.period_ending.year)
            cash_flows.sort(key=lambda x: x.period_ending.year)

            previous = 0
            good_fundamentals_counter = 0
            number_years = 0
            complementary_percentage = 1 - fund_utils.gv.perc_improv

            if not balance_sheets:
                return False
            if not cash_flows:
                return False

             # scanning through the financial statements.
            for balance_sheet, cash_flow in zip(balance_sheets, cash_flows):

                if balance_sheet.period_ending.year != cash_flow.period_ending.year:
                    log.info(f'{Back.RED}{Fore.WHITE} The examined year for the balance sheet and '
                             f'the cash flow statement of the equity with symbol {equity.exchange}:{equity.symbol_1} '
                             f'are not coincident. Moving the the next equity{Style.RESET_ALL}')
                    return False

                if balance_sheet.period_length == Timespan.annual and \
                        cash_flow.period_length == Timespan.annual:

                    number_years += 1  # keep tracks of how many financial statements I have.

                    cash_dividends_paid = methods.validate(cash_flow.total_cash_dividends_paid)
                    total_equity = methods.validate(balance_sheet.total_equity)
                    current = total_equity + cash_dividends_paid

                    if current:  # if it is not None
                        current_minus_improvement = current * complementary_percentage
                        if previous < current_minus_improvement:
                            good_fundamentals_counter += 1
                        previous = current

            if good_fundamentals_counter == number_years:  # increased every year
                return True
            else:
                return False

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
