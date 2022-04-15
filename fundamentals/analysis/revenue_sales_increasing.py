
import fundamentals.miscellaneous as fund_utils
from utilities.common_methods import getDebugInfo
from utilities import log


class RevenueSalesIncreasing:
    """
    class RevenueSalesIncreasing
    It checks if the revenue (called sales in the Invested book) is increasing by a certain percentage each year.
    The revenue can be found in the income statement. It is also called sales.
    """
    @staticmethod
    def is_met(equity):
        try:
            financial_statements = equity.fundamentals.income_statement
            financial_key = 'revenue'

            # sort the equities according to the ending year.
            financial_statements.sort(key=lambda x: x.period_ending.year)

            if fund_utils.increasing_by_certain_percentage.is_met(financial_statements, financial_key, fund_utils.gv.perc_improv):
                return True
            else:
                return False

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
