from utilities.common_methods import getDebugInfo
from utilities import log


class RoeHigherThanIndustry():
    """
    class RoeHigherThanIndustry
    It checks if the roe in the previous 5 years is higher thant the industry average.
    """
    @staticmethod
    def is_met(equity):
        try:
            equity_roe_5y_average = equity.fundamentals.ratios[0].return_on_equity_5ya
            industry_roe_5y_average = equity.fundamentals.ratios[1].return_on_equity_5ya
            equity_roe_ttm = equity.fundamentals.ratios[0].return_on_equity_ttm
            industry_roe_ttm = equity.fundamentals.ratios[1].return_on_equity_ttm

            if equity_roe_5y_average > industry_roe_5y_average and \
                    equity_roe_ttm > industry_roe_ttm:
                return RoeHigherThanIndustry.equity_roe_is_increasing(equity_roe_ttm, equity_roe_5y_average)
            else:
                return False

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def equity_roe_is_increasing(equity_roe_ttm, equity_roe_5y_average):
        if equity_roe_ttm > equity_roe_5y_average:
            return True
        else:
            return False
