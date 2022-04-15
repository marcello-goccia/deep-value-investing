from data_storing.assets.database_manager import DatabaseManager as db_mngr
from data_storing.assets.common import Timespan, MeasureUnit
from datetime import date


def delete_equity():
    symbol = 'HCAT'
    id = 43752
    db_mngr.delete_equity_from_database(symbol=symbol)
    db_mngr.delete_equity_by(id=id)
    print(f"deleted equity with symbol {symbol}")
    print(f"deleted equity with id {id}")


def reset_all_done():
    equities = db_mngr.query_all_equities_by()  # country="United States" 'Bahrain')
    for equity in equities:
        if equity.id > 43841:
            equity.all_done = False
    print("all done from equities were all reset!")
    db_mngr.commit_to_database()


def set_all_done():
    equities = db_mngr.query_all_equities_by()  # country="United States" 'Bahrain')
    for equity in equities:
        equity.all_done = True
    print("all done from equities were all set to done!")
    db_mngr.commit_to_database()


def delete_all_prices_from_equity(equity_symbol=None, exchange=None):

    if equity_symbol is None and exchange is None:
        equity_symbol = "place here a testing symbol"
        exchange = "place here a testing exchange"

    equity = db_mngr.query_equity_by_symbol_1_and_exchange(equity_symbol, exchange)
    db_mngr.delete_list_of_items(equity.prices)


def count_number_of_equities_with_historical_data_newer_than_2014():
    import datetime

    total_counter_equities = 0
    counter = 0
    equities = db_mngr.query_all_equities_by()
    for equity in equities:
        total_counter_equities += 1
        if equity.prices:
            equity.prices.sort(key=lambda x: x.day)
            oldest_price = equity.prices[0]
            oldest_day = oldest_price.day
            if oldest_day > datetime.date(2014, 1, 1):
                counter += 1
                if total_counter_equities % 300 == 0:
                    print(f"so far done {total_counter_equities} equities, and found {counter} with a too new date.")
    print(f"FINAL !!! Found {counter} equities with a too new date.")


def reset_equities_with_historical_data_newer_than_2014():
    import datetime

    total_counter_equities = 0
    counter = 0
    equities = db_mngr.query_all_equities_by()
    for equity in equities:
        total_counter_equities += 1
        if equity.prices:
            equity.prices.sort(key=lambda x: x.day)
            oldest_price = equity.prices[0]
            oldest_day = oldest_price.day
            if oldest_day > datetime.date(2014, 1, 1):
                equity.all_done = False
                counter += 1
                if total_counter_equities % 300 == 0:
                    print(f"so far done {total_counter_equities} equities, and found {counter} with a too new date.")

    print(f"FINAL !!! Found {counter} equities with a too new date.")
    db_mngr.commit_to_database()

def main():

    # equity = db_mngr.insert_equity_into_asset(symbol_1="AAPL", name="Apple Inc.", exchange=u'nasdaq')
    # db_mngr.insert_equity_into_asset(symbol_1="AMZN", name="Amazon.com", exchange=u'nasdaq')
    # db_mngr.insert_equity_into_asset(symbol_1="TSLA", name="Tesla Electric Cars", exchange=u'nasdaq')
    #
    # db_mngr.insert_balance_sheet_into_asset(equity_id=equity.id,
    #                                         period_length=Timespan.annual,
    #                                         period_ending=date(2009, 12, 28),
    #                                         measure_unit=MeasureUnit.million,
    #                                         total_current_assets=123456789)
    #
    # db_mngr.insert_income_statement_into_asset(equity_id=equity.id,
    #                                         period_length=Timespan.annual,
    #                                         period_ending=date(2009, 12, 28),
    #                                         measure_unit=MeasureUnit.million,
    #                                         total_revenue=789)
    #
    # db_mngr.insert_cash_flow_into_asset(equity_id=equity.id,
    #                                     period_length=Timespan.annual,
    #                                     period_ending=date(2009, 12, 28),
    #                                     measure_unit=MeasureUnit.million,
    #                                     cash_from_operating_activities=456)
    #
    # # db_mngr.insert_ratios_into_asset(equity_id=equity.id,
    # #                                     something=456)
    #
    # # TESTING QUERIES
    # equities = db_mngr.query_all_equities()
    # apple = db_mngr.query_equity_by_symbol_1_and_exchange(symbol_1="AAPL", exchange=u'nasdaq')

    # TESTING DELETING
    # delete_equity()

    # TESTING REMOVE ALL DONE
    # reset_all_done()

    set_all_done()

    # TESTING REMOVE ALL PRICES
    # delete_all_prices_from_equity('BRKb', 'NYSE')

    # CHECKING HISTORICAL DATA OF EQUITIES ARE ALL OK
    # count_number_of_equities_with_historical_data_newer_than_2014()
    # reset_equities_with_historical_data_newer_than_2014()

    pass


# run the program
if __name__ == "__main__":
    main()
