
import fundamentals.miscellaneous as fund_utils
from utilities.common_methods import getDebugInfo
from utilities import log


class CashFromOperatingActivitiesIncreasing:
    """
    class CashFromOperatingActivitiesIncreasing
    It checks if the cash from operating activities is increasing by a certain percentage each year.
    The cash from operating activities can be found in the cash flow.
    """
    @staticmethod
    def is_met(equity):
        try:
            financial_statements = equity.fundamentals.cash_flow
            financial_key = 'cash_from_operating_activities'

            # sort the equities according to the ending year.
            financial_statements.sort(key=lambda x: x.period_ending.year)

            if fund_utils.increasing_by_certain_percentage.is_met(
                    financial_statements, financial_key,
                    fund_utils.gv.perc_improv):
                return True
            else:
                return False

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
