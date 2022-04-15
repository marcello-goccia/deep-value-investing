from utilities.common_methods import getDebugInfo
from utilities import log


class NpmHigherThanIndustry():
    """
    class NpmHigherThanIndustry
    It checks if the net profit margin in the previous 5 years is higher thant the industry average.
    """
    @staticmethod
    def is_met(equity):
        try:
            equity_npm_5y_average = equity.fundamentals.ratios[0].net_profit_margin_5ya
            industry_npm_5y_average = equity.fundamentals.ratios[1].net_profit_margin_5ya
            equity_npm_ttm = equity.fundamentals.ratios[0].net_profit_margin_ttm
            industry_npm_ttm = equity.fundamentals.ratios[1].net_profit_margin_ttm

            if equity_npm_5y_average > industry_npm_5y_average and \
                    equity_npm_ttm > industry_npm_ttm:
                return NpmHigherThanIndustry.equity_npm_is_increasing(equity_npm_ttm, equity_npm_5y_average)
            else:
                return False

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def equity_npm_is_increasing(equity_npm_ttm, equity_npm_5y_average):
        if equity_npm_ttm > equity_npm_5y_average:
            return True
        else:
            return False
