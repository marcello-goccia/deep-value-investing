from utilities.common_methods import getDebugInfo
from utilities import log

best_sentiment_evaluation = 'Strong Buy'
max_sentiment_score = 5


class StrongBuy:

    @staticmethod
    def is_met(equity):
        try:
            sentiment = 0
            if equity.overview.fifteen_minutes_sentiment == best_sentiment_evaluation:
                sentiment += 1
            if equity.overview.hourly_sentiment == best_sentiment_evaluation:
                sentiment += 1
            if equity.overview.weekly_sentiment == best_sentiment_evaluation:
                sentiment += 1
            if equity.overview.daily_sentiment == best_sentiment_evaluation:
                sentiment += 1
            if equity.overview.monthly_sentiment == best_sentiment_evaluation:
                sentiment += 1

            if sentiment == max_sentiment_score:
                # buy_it!
                return True
            return False
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
