from data_collection.container import Container
from data_collection import request_quantic_data as qdata
from data_plotting.draw_movingavg_rsi_macd import Draw_movingavg_rsi_macd
from data_storing.assets.database_manager import DatabaseManager as db
from technical_analysis.moving_average_strategy import MovingAverageStrategy
from data_collection.set_of_tickers.getting_tickers import GettingTickers
from utilities import log
from utilities.common_methods import getDebugInfo


def main():
    try:

        fill_up_database_equities = False
        if fill_up_database_equities:
            # The following if you need to fill the database with the equities.
            tickers = GettingTickers.read_the_set_of_tickers()
            print(u'storing the tickers to the database')
            for ticker in tickers:
                db.insert_equity_into_asset(ticker=ticker)
            print(u'terminated storing the tickers to the database')


        #equities = ['AAPL', 'TSLA', '^GSPC']
        equities = db.query_all_equities()

        # define the quantitative object
        # access the retrieved data through: quantitative.requested.data
        quantitative = qdata.RequestQuanticData()

        for equity in equities:
            start_date = '2019-07-01'
            # end_date = 'define the end date'

            ticker = 'AAPL'

            # if you want to extract from the oldest available data, pass None as start_date.
            quantitative.get_requested_data(ticker, start=start_date)

            container = Container()

            if quantitative.requested.data is not None:

                quantitative.requested.data.name = ticker
                container.data = quantitative.requested.data

                ma = 'sma'
                strategy = MovingAverageStrategy(ticker)
                container.statistics = {ma: {}}
                buy, container.statistics[ma] = strategy.buying_signal_moving_averages(container.data['Adj Close'], container.statistics[ma])

                if buy:
                    Draw_movingavg_rsi_macd(quantitative.requested.data)

    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")


if __name__ == "__main__":
    main()
    pass


