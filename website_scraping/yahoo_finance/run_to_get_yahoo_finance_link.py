import os
import sys
import csv
import time
from difflib import SequenceMatcher
from pandas_datareader import data as data_reader
from pandas_datareader._utils import RemoteDataError
from utilities.log import root_folder_all_code

dir_path = os.path.dirname(os.path.realpath(__file__))
dir_root = dir_path.split(root_folder_all_code, 1)[0]
code_path = os.path.join(dir_root, root_folder_all_code)
sys.path.insert(0, code_path)

from utilities.common_methods import getDebugInfo
from utilities.common_methods import Methods as methods
from utilities import log
from utilities.globals import websites
from website_scraping.investing_dot_com.assets_labels import Labels as labels
from data_storing.assets.database_manager import DatabaseManager as db_mngr

sure_threshold = 0.85


def similar(a, b):
    return SequenceMatcher(None, a, b).ratio()


def main():
    try:
        start_time_process_equities = time.monotonic()

        # open the file yahoo_symbols.csv in the folder set_of_symbols
        path_yahoo_symbols_file = os.path.join(code_path, 'website_scraping', 'yahoo_finance', 'yahoo_symbols.csv')

        exchanges_list = ''

        equities = db_mngr.query_all_equities_by()  # Take all the equities

        # Open the csv file and keep it in the memory
        with open(path_yahoo_symbols_file, 'r', encoding="ISO-8859-1") as csvFile:

            reader = csv.reader(csvFile)

            counter_not_found = 0
            counter_processed = 0

            for equity in equities:
                if equity.symbol_2:
                    continue

                try:
                    counter_processed += 1

                    exchanges_list, suffixes_yahoo = labels.get_yahoo_list_exchanges(equity.country)

                    for suffix in suffixes_yahoo:
                        try:
                            if suffix:
                                symbol = '.'.join([equity.symbol_1, suffix])
                            else:
                                symbol = equity.symbol_1
                            data_reader.get_data_yahoo(symbol, start=methods.get_date_days_ago(3))
                            equity.symbol_2 = symbol
                            equity.weblink_2 = websites.yahoo + equity.symbol_2
                            break
                        except RemoteDataError as e:
                            if "No data fetched for symbol" in str(e):
                                continue

                    if equity.symbol_2:
                        db_mngr.commit_to_database()
                        continue

                except Exception as e:
                    log.error(f"There is a problem in the code when reading symbol for {equity.name}, "
                              f"{equity.exchange}:{equity.symbol_1}")

                # back to the beginning of the csv file.
                csvFile.seek(0)
                best_score = {'yahoo_symbol':     '',              'yahoo_name':     '',
                              'investing_symbol': equity.symbol_1, 'investing_name': equity.name,
                              'ratio': 0.0}
                try:
                    for row in reader:

                        exchange_yahoo = row[3]

                        if exchange_yahoo not in exchanges_list:
                            continue

                        equity_name = equity.name.replace('.', '')
                        equity_name = equity_name.lower()
                        yahoo_name = row[1].replace('.', '')
                        yahoo_name = yahoo_name.lower()
                        ratio = similar(equity_name, yahoo_name)

                        if ratio > best_score['ratio']:
                            best_score['yahoo_symbol'] = row[0]
                            best_score['yahoo_name'] = yahoo_name
                            best_score['ratio'] = ratio

                            if ratio == 1.0:
                                break

                    if best_score['ratio'] > sure_threshold:
                        print(f"found symbol for the equity with id: {equity.id} with a score {best_score['ratio']}. "
                              f"yahoo = investing:  {best_score['yahoo_name']} = {equity.name} : "
                              f"{best_score['yahoo_symbol']} = {equity.symbol_1}")
                        equity.symbol_2 = best_score['yahoo_symbol']
                        equity.weblink_2 = websites.yahoo + equity.symbol_2
                        db_mngr.commit_to_database()
                    else:
                        counter_not_found += 1
                        print(f"could not find link on yahoo  for the equity with id: {equity.id}:  "
                              f"yahoo = investing:  {best_score['yahoo_name']} = {equity.name} : "
                              f"{best_score['yahoo_symbol']} = {equity.symbol_1}\t\tthe ratio was : "
                              f"{best_score['ratio']}. "
                              f"So far we could not find {counter_not_found} symbols in yahoo finance "
                              f"on a total number of {counter_processed} equities!")

                except Exception as e:
                    log.error(f"There is a problem in the code when parsing equity {equity.name}!: {e}\n{getDebugInfo()}")

        csvFile.close()

        elapsed_time_process_equities = time.monotonic() - start_time_process_equities
        message = f"Terminated: the time spent to retrieve all the equities links is " \
            f"{elapsed_time_process_equities}. " \
            f"Could not find {counter_not_found} symbols in yahoo finance " \
            f"on a total number of {counter_processed} equities!"
        log.info(message)

    except Exception as e:
        log.error(f"There is a problem in the code when parsing the symbols for yahoo finance!: {e}\n{getDebugInfo()}")


if __name__ == "__main__":
    main()
    pass
