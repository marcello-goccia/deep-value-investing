import traceback
import time
import datetime
import sys
from decimal import Decimal
from utilities import log
from urllib.request import URLError

default_float = None

NA = ['-', '--', 'N/A', 'NA', ' ']


def parse(string, dictionary):
    if string in dictionary:
        return dictionary[string]
    else:
        return ''


d = {
    'K': 3,
    'k': 3,
    'M': 6,
    'm': 6,
    'B': 9,
    'b': 9,
    'T': 12,
    't': 12
}


class Methods:

    @staticmethod
    def perform_until_succeed(max_timeout, function, *args):
        """
        @function perform_until_succeed
        The method loops several times trying to running the function passed as input with its own arguments.
        It the function is performed without raising an exception, the performance is considered succeeded, otherwise
        it keeps on looping until the timout is reached.
        @param max_timeout the time spent before exiting without success.
        @param function the function to execute
        @args the parameters of the function.
        """
        try:
            timeout = time.time() + max_timeout  # 1 minutes from now
            while True:
                time.sleep(1)

                if time.time() > timeout:
                    raise Exception(f"Cannot execute the requested function {function}!!!: {e}\n{getDebugInfo()}")
                try:
                    fun_output = function(*args)
                    return fun_output
                except Exception as e:
                    print(f"Debug:\t\tTrying running the function {function} ")
                    continue

        except URLError as e:
            msg = "Cannot open url."
            log.error(msg)
            raise Exception(msg)
        except Exception as e:
            msg = f"Cannot execute the requested function {function}!!!: {e}\n{getDebugInfo()}"
            log.error(msg)
            raise Exception(msg)

    @staticmethod
    def text_to_num(text):
        """
        @function text_to_num
        Used to convert text number with B or M or K into numbers
        :param text:
        :return:
        """
        try:
            if text[-1] in d:
                num, magnitude = text[:-1], text[-1]
                return Decimal(num) * 10 ** d[magnitude]
            else:
                return Decimal(text)
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            raise

    @staticmethod
    def convert_to_float(value):
        """
        @function convert_to_float
        Used to convert text number with some particular keywords (like M,B or %) into a floating point number
        """
        try:
            if value is None:
                return None

            assert(isinstance(value, str))

            # remove the comma from large numbers.
            value = value.replace(',', '')

            if "%" in value:
                value = value.replace("%", u'')
                value = float(value) / 100  # get a percentage

            elif "T" in value or "t" in value or "B" in value or "b" in value or \
                    "M" in value or "m" in value or "K" in value or "k" in value:
                value = Methods.text_to_num(value)

            try:
                value = float(value)
            except ValueError:
                raise Exception(f"{value} cannot be converted to float")

            return value

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            raise

    @staticmethod
    def get_valid_value(value):
        """
        @function get_valid_value
        Removes not needed characters
        Still returns a string.
        """
        try:
            if value is None:
                return None

            if value == "NULL":
                return None

            assert(isinstance(value, str))

            value = value.replace(u'\xa0', u' ')
            value = value.replace(u'\n', u'')
            value = value.replace(u'\t', u'')

            if value in NA:
                return None
            value = value.replace('- ', '-')

            return value

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            raise

    @staticmethod
    def remove_character(string, to_remove):
        try:
            if string is None:
                return None
            return string.replace(to_remove, '')
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            raise

    @staticmethod
    def from_percent_to_decimal(value):
        try:
            if value is None:
                return None

            try:
                value = float(value)
            except ValueError:
                raise Exception(f"{value} cannot be converted to float")

            if isinstance(value, float):
                value = value / 100
            return value
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            raise

    @staticmethod
    def truncate(f, n):
        """
        Truncates/pads a float f to n decimal places without rounding
        """
        try:
            s = '{}'.format(f)
            if 'e' in s or 'E' in s:
                return '{0:.{1}f}'.format(f, n)
            i, p, d = s.partition('.')
            return '.'.join([i, (d+'0'*n)[:n]])
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            raise

    @staticmethod
    def validate(value):
        """
        @function get_valid_value
        This method check if the variable in input is None, if it is, it return zero, otherwise
        it returns the variable itself.
        """
        try:
             if value is None:
                 return 0
             else:
                 return value
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            raise

    @staticmethod
    def get_today_date():
        try:
            return datetime.datetime.today().strftime('%Y-%m-%d')
        except:
            print("Cannot define the current date.")
            return None

    @staticmethod
    def get_date_days_ago(number_of_days):
        try:
            date_days_ago = datetime.datetime.now() - datetime.timedelta(days=number_of_days)
            return date_days_ago.strftime('%Y-%m-%d')
        except:
            print("Cannot define the current date.")
            return None

    @staticmethod
    def get_date_weeks_ago(number_of_weeks):
        try:
            date_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=number_of_weeks)
            return date_weeks_ago.strftime('%Y-%m-%d')
        except:
            print("Cannot define the current date.")
            return None

    @staticmethod
    def get_last_year():
        try:
            now = datetime.datetime.now()
            return now.year - 1
        except:
            print("Cannot define last year number")
            return None

    @staticmethod
    def get_last_month():
        try:
            now = datetime.datetime.now()
            return now.month - 1 if now.month > 1 else 12
        except:
            print("Cannot define last month number")
            return None

    @staticmethod
    def forward_days(inut_time, days=0):
        try:
            return inut_time + datetime.timedelta(days=days)
        except:
            print("Cannot generate a data with one year foward")
            return None

    @staticmethod
    def backward_days(inut_time, days=0):
        try:
            return inut_time - datetime.timedelta(days=days)
        except:
            print("Cannot generate a data with one year foward")
            return None

    @staticmethod
    def trunc_date(a_date):
        return a_date.replace(day=1)

    @staticmethod
    def get_prices_in_range_of_dates(equity, dates):
        """
        Given the equity in input it returns the prices for the date in the range of the input variable dates..
        @param equity the equity we are interested in the dates
        @param dates, the dates among which the prices will be scraped (dates is a dictionary(
        @return the vector with the prices, empty if it was not successful
        """
        # sort the dates of the prices.
        try:
            equity.prices.sort(key=lambda x: x.day)

            prices_in_range = []
            for price in equity.prices:

                if dates['start_date'] <= price.day <= dates['end_date']:
                    prices_in_range.append(price)

            return prices_in_range

        except Exception as e:
            log.error(f"There is a problem with the equity {equity.exchange}:{equity.symbol_1} : {e}\n{getDebugInfo()}")
            return []

    @staticmethod
    def get_prices_in_range_of_dates_from_file(input_path, dates=None):
        """
        Given the equity in input it returns the prices for the date in the range of the input variable dates..
        @param equity the equity we are interested in the dates
        @param dates, the dates among which the prices will be scraped (dates is a dictionary(
        @return the vector with the prices, empty if it was not successful
        """
        try:
            import csv
            data_prices = dict()
            with open(input_path, newline='') as csvfile:
                data_reader = csv.reader(csvfile, delimiter=',', quotechar='"')

                header = next(iter(data_reader))

                for row in data_reader:
                    # Casting the two values
                    day = datetime.datetime.strptime(row[0], '%b %d, %Y').date()
                    price_str = row[1].replace(',', '')
                    price = float(price_str)
                    data_prices[day] = price

                sorted_dictionary = dict()
                for key in sorted(data_prices):
                    sorted_dictionary[key] = data_prices[key]

                selected_dates = dict()
                for key, value in sorted_dictionary.items():
                    if not dates:
                        selected_dates[key] = value
                    elif dates['start_date'] <= key <= dates['end_date']:
                        selected_dates[key] = value

                # return a list of prices (from the class Price)
                prices = []
                for key, value in selected_dates.items():
                    prices.append(Price(day=key, close=value))

                return prices

                # header = next(iter(data_reader))
                # # The following will read all the prices csv file and place in a complete dictionary
                # for value in header:
                #     data_prices[value] = []
                #
                # for row in data_reader:
                #     for key, value in zip(header, row):
                #         if "Date" in key:
                #             value = datetime.datetime.strptime(value, '%b %d, %Y').date()
                #         data_prices[key].append(value)

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            return None

    @staticmethod
    def sort_getter(item):
        value = item[0]
        return value


    @staticmethod
    def are_variations_in_purchasing_prices_unlikely(equity, dates):
        """
        The methods check if the prices of the equity in the wanted range are possible or not.
        We mean that if between two near samples there is a very high variations, for example
        higher that 50% or 100% it is possible that it is only a mistake of the website where the data was collected.
        @return True if variations are unlikely, False if they are not.
        """
        try:
            prices = Methods.get_prices_in_range_of_dates(equity, dates)

            higher_threshold = 5
            lower_threshold = 0.1

            for price_t0, price_t1 in zip(prices, prices[1:]):

                try:
                    price_ratio = price_t1.close / price_t0.close
                except ZeroDivisionError:
                    price_ratio = 10000

                if lower_threshold < price_ratio < higher_threshold:
                    continue  # False in this case is good
                else:
                    log.error(f"Something wrong about the price of equity {equity.exchange}:{equity.symbol_1}. "
                              f"The price ratio is {price_ratio}")
                    return True   # True in this case is not good

            return False  # False in this case is good

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            return False

    @staticmethod
    def nth_root(num, root):
       #** means square
       answer = num ** (1/root)
       return answer

class EthernetProblems:
    counter_connection_problems = 0
    connection_problems = False
    max_counter = 20


def getDebugInfo():
    """
    @function getDebugInfo
    This method returns the string with the information of what
    caused the exception to be raised.

    @return string the value with the debug info to write on the log file
    """
    string = ""
    for frame in traceback.extract_tb(sys.exc_info()[2]):

        file_name, line_no, function, text = frame

        if file_name is None:
            file_name = ''
        if line_no is None:
            line_no = ''
        if function is None:
            function = ''
        if text is None:
            text = ''

        string += f" in file: {file_name}" \
                  f" line no: {line_no}" \
                  f" function: {function}" \
                  f" text: {text} \n"

    return string


class Price:
    def __init__(self, day, close):
        self.day = day
        self.close = close

