import datetime  # For datetime objects
from utilities import log
from utilities.common_methods import getDebugInfo
from utilities.globals import paths

import backtrader as bt
import backtesting.commission_schemes as commission_schemes
import backtesting.strategies as strategy
import backtesting.data_reading as data_reading


class BackTestStrategy:

    def __init__(self, equity_symbol, from_date, to_date, porfolio_value, cash_to_invest_in_asset):
        self.equity_symbol = equity_symbol
        self.from_date = from_date
        self.to_date = to_date
        self.porfolio_value = porfolio_value
        self.cash_to_invest_in_asset = cash_to_invest_in_asset

    def run(self):
        try:
            # TODO: Make this algorithm to iterate through the years
            # TODO: Make this algorithm a better money management, just instantiate for each equity a little money
            #  and add up all the money when the investing is concluded.

            # Create a cerebro entity
            cerebro = bt.Cerebro()

            # Add a strategy
            #cerebro.addstrategy(strategy.BuyAndHold, self.cash_to_invest_in_asset)
            cerebro.addstrategy(strategy.DollarCostAveraging, self.cash_to_invest_in_asset)

            # # Create a Data Feed
            # data = bt.feeds.YahooFinanceData(dataname=self.equity_symbol,fromdate=self.from_date,
            #     todate=self.to_date, reverse=False)

            data = data_reading.InvestingCSVData(  # bt.feeds.GenericCSVData(
                dataname=paths.historical_data_csv,
                fromdate=self.from_date,
                todate=self.to_date)

            # Add the Data Feed to Cerebro
            cerebro.adddata(data)

            # Set our desired cash start
            cerebro.broker.setcash(self.porfolio_value)

            # Add a FixedSize sizer according to the stake
            cerebro.addsizer(bt.sizers.FixedSize)  #, stake=10)

            # Set the commission - 0.1% ... divide by 100 to remove the %
            commissions = commission_schemes.DegiroFixed()
            cerebro.broker.addcommissioninfo(commissions)

            # Print out the starting conditions
            print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

            # Run over everything
            cerebro.run()

            finale_value = cerebro.broker.getvalue() - commissions.p.commission  # subtract to see if I sell at the last
            amount_earned = finale_value - self.porfolio_value

            rate_earned = 0
            for data in cerebro.broker.positions.items():
                position = data[1]
                initial_capital = position.size * position.price - commissions.p.commission
                final_capital = initial_capital + amount_earned
                rate_earned = round((final_capital / initial_capital - 1) * 100, 2)
                break

            # Print out the final result
            print('Final Portfolio Value: %.2f' % finale_value)

            # Plot the result
            cerebro.plot()

            return amount_earned, rate_earned

        except FileNotFoundError as e:
            return 0

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
            return 0


# run the program
if __name__ == "__main__":

    equity_symbol = 'MSFT'
    from_date = datetime.datetime(2019, 4, 1)
    to_date = datetime.date.today()
    porfolio_value = 10000  # dollars(?)
    percent_to_invest = 0.20
    amount_to_invest = round(porfolio_value * percent_to_invest)

    backtest = BackTestStrategy(equity_symbol, from_date, to_date, porfolio_value, amount_to_invest)
    backtest.run()
