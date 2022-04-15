from data_storing.assets.database_manager import DatabaseManager as db_mngr
from utilities.globals import websites


def manual_check_yahoo_symbol_exists(equity):
    if not equity.symbol_2:
        yahoo_symbol = input(f"Input the yahoo symbol for the equity: {equity.exchange}:{equity.symbol_1}:\n")
        if yahoo_symbol == '':
            print("ok you do not want! let's go on!!")
        confirm = input(f"Are you sure {yahoo_symbol} is correct? (yes, y) ")
        if confirm.lower() == 'yes' or confirm.lower() == 'y':
            equity.symbol_2 = yahoo_symbol
            equity.weblink_2 = websites.yahoo + equity.symbol_2
            db_mngr.commit_to_database()
        else:
            print("ok try again later if you want")
    return

