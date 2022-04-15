import time
import datetime
from data_storing.assets.database_manager import DatabaseManager as db_mngr
from data_collection.online_data import YahooFinanceData
from data_monitoring.email_sender import EmailSender
from website_scraping.yahoo_finance.fill_up_yahoo_tickers_symbols import manual_check_yahoo_symbol_exists
from utilities.common_methods import Methods as methods
from utilities import log
from utilities.common_methods import getDebugInfo


def data_test_generation(input):
    """
    Little snipped to create fake companies to monitor for testing
    these companies then need to be bought back to the original value
    if input = 1 modify the values
    if input = 0 back to the original values
    """
    aapl_equity = db_mngr.query_equity_by_symbol_1_and_exchange(exchange='NASDAQ', symbol_1='AAPL')
    amzn_equity = db_mngr.query_equity_by_symbol_1_and_exchange(exchange='NASDAQ', symbol_1='AMZN')

    if input == 1:
        aapl_equity.overview.valuable_company = 1
        aapl_equity.overview.intrinsic_value = 150
        amzn_equity.overview.valuable_company = 1
        amzn_equity.overview.intrinsic_value = 114
    else:
        aapl_equity.overview.valuable_company = 0
        aapl_equity.overview.intrinsic_value = None
        amzn_equity.overview.valuable_company = 0
        amzn_equity.overview.intrinsic_value = None

    db_mngr.commit_to_database()


class MonitorIntrinsicValue:

    def __init__(self):

        try:
            self.request = None
            self.equities = None
            #data_test_generation(1)
            # for equity in self.equities:
            #     manual_check_yahoo_symbol_exists(equity)
            # return
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def check_for_discount(self):
        try:
            while True:
                self.scan_all_equities_and_monitor_them()
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def scan_all_equities_and_monitor_them(self):
        try:
            self.equities = db_mngr.query_equity_by_valuable_company()
            start = methods.get_date_days_ago(3)
            end = methods.get_today_date()
            self.request = YahooFinanceData()
            for equity in self.equities:

                symbol_message = f"{equity.exchange}:{equity.symbol_1}"

                data = self.request.get_data(equity.symbol_2, start, end)
                prices_close = data['Adj Close']
                last_price = prices_close[-1]

                if last_price <= float(equity.overview.intrinsic_value):
                    # send me email
                    message = self.get_email_message(symbol_message)
                    EmailSender.send(message)

                print(f"{self.get_date_now()}: last close of {symbol_message} is: {prices_close[-1]}")

            #self.wait_hours(5)
            self.wait_minutes(5)
            return
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            return

    @staticmethod
    def get_email_message(symbol_message):
        try:
            message = f"""\
            Subject: Attention!!!

            The equity with symbol {symbol_message} needs to be bought!!!!"""

            return message
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def wait_hours(number_of_hours):
        time.sleep(3600 * number_of_hours)

    @staticmethod
    def wait_minutes(number_of_minutes):
        time.sleep(60 * number_of_minutes)

    @staticmethod
    def wait_seconds(number_of_seconds):
        time.sleep(number_of_seconds)

    @staticmethod
    def get_date_now():
        now = datetime.datetime.now()
        return now.strftime("%Y-%m-%d %H:%M")
