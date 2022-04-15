
import fundamentals.miscellaneous as fund_utils
from utilities.common_methods import getDebugInfo
from utilities import log


class TotalEquityIncreasing:
    """
    class TotalEquityIncreasing
    It checks if the total equity is increasing by a certain percentage each year.
    It can be found in the balance sheet.
    The total equity in the book Invested (Danielle Town) is called book value)
    """
    @staticmethod
    def is_met(equity):
        try:
            financial_statements = equity.fundamentals.balance_sheet
            financial_key = 'total_equity'

            # sort the equities according to the ending year.
            financial_statements.sort(key=lambda x: x.period_ending.year)

            if fund_utils.increasing_by_certain_percentage.is_met(
                    financial_statements,
                    financial_key, fund_utils.gv.perc_improv):
                return True
            else:
                return False

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
