import pandas as pd
from utilities import log

class GettingTickers:

    def __init__(self):
        """
        @function constructor
        It defines the class variables.
        """
        self.tickers = []

    def read_the_set_of_tickers_(self):
        """
        @function read_the_set_of_tickers
        The method returns the set of tickers to be analysed.
        @return the set of tickers extracted.
        """
        try:
            with open('./set_of_tickers/quandl_metadata.csv', 'r') as csv_file:

                data = pd.read_csv(csv_file, header=0)
                self.tickers = data.code.tolist()

                #csv_reader = csv.reader(csv_file, delimiter=',')
                #data = pd.read_csv('./set_of_tickers/quandl_metadata.csv', header=0)
                #for row in csv_reader:
                #     current_ticker = row[0]
                #     self.tickers.append(current_ticker)
                # del self.tickers[0]

            return self.tickers

        except Exception as e:
            print("There is a problem with getting the tickers: ", e)

    @classmethod
    def read_the_set_of_tickers(cls):
        """
        @function read_the_set_of_tickers
        The method returns the set of tickers to be analysed.
        @return the set of tickers extracted
        """
        obj = cls()
        return obj.read_the_set_of_tickers_()
