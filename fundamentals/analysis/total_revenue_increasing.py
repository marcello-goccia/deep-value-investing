
import fundamentals.miscellaneous as fund_utils
from utilities.common_methods import getDebugInfo
from utilities import log


class TotalRevenueIncreasing:
    """
    class TotalRevenueIncreasing
    It checks if the total revenue is increasing by a certain percentage each year
    """
    @staticmethod
    def is_met(equity):
        try:
            financial_statements = equity.fundamentals.income_statement
            financial_key = 'total_revenue'

            # sort the equities according to the ending year.
            financial_statements.sort(key=lambda x: x.period_ending.year)

            # for this one we just care it increased, so percentage_improvement = 0.0
            if fund_utils.increasing_by_certain_percentage.is_met(financial_statements,
                                                                  financial_key,
                                                                  percentage_improvement=0.0):
                return True
            else:
                return False

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
