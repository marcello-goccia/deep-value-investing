from bs4 import BeautifulSoup
from urllib.request import urlopen, URLError
from utilities.common_methods import getDebugInfo
from utilities.common_methods import NA
from utilities import log

main_website = u'https://finance.yahoo.com/quote/'

current_path = './fundamentals/yahoo_finance/'

class GetYahooFundamentals:

    def __init__(self, symbols):
        try:
            self.symbols = symbols

            self.soup = None

            self.stem_statistics = u'/key-statistics?p='  # '/key-statistics?ltr=1'
            self.stem_income_statement = u'/financials?p='
            self.stem_balance_sheet = u'/balance-sheet?p='
            self.stem_cash_flow = u'/cash-flow?p='
            self.stem_analysis = u'/analysis?p='
            self.stem_holders = u'/holders?p='

            self.table_key_statistics = []
            self.table_income_statement = []
            self.table_balance_sheet = []
            self.table_cash_flow = []
            self.table_analysis = []
            self.table_holders = []

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_all_the_fundamentals(self):
        try:
            for symbol in self.symbols:

                self.get_statistics(symbol)
                self.get_income_statement(symbol)
                self.get_balance_sheet(symbol)
                self.get_cash_flow(symbol)
                self.get_analysis(symbol)
                self.get_holders(symbol)

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def read_website(self, url):
        try:
            try:
                resp = urlopen(url)
            except URLError as e:
                raise Exception("Cannot open url.")

            self.soup = BeautifulSoup(resp.read(), 'html.parser')

            # for debugging purposes write down the website.
            text_file = open(current_path + 'Output.txt', "w")
            text_file.write(self.soup.prettify())
            text_file.close()
            # print(soup.prettify())
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_statistics(self, current_symbol):
        """
        From the section statistics.
        """
        try:
            self.table_key_statistics = []
            self.get_info_from_table(current_symbol, self.stem_statistics, self.table_key_statistics)
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_income_statement(self, current_symbol):
        """
        From the section financials/income statement.
        """
        try:
            self.table_income_statement = []
            self.get_info_from_table(current_symbol, self.stem_income_statement, self.table_income_statement)
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_balance_sheet(self, current_symbol):
        """
        From the section financials/balance sheet
        """
        try:
            self.table_balance_sheet = []
            self.get_info_from_table(current_symbol, self.stem_balance_sheet, self.table_balance_sheet)
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_cash_flow(self, current_symbol):
        """
        From the section financials/cash flow
        """
        try:
            self.table_cash_flow = []
            self.get_info_from_table(current_symbol, self.stem_cash_flow, self.table_cash_flow)
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_analysis(self, current_symbol):
        """
        From the section analysis
        """
        try:
            self.table_analysis = []
            self.get_info_from_table(current_symbol, self.stem_analysis, self.table_analysis)
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_holders(self, current_symbol):
        """
        From the section holders
        """
        try:
            self.table_holders = []
            self.get_info_from_table(current_symbol, self.stem_holders, self.table_holders)
            pass
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_info_from_table(self, current_symbol, stem, table_info):
        """
        General method to scrap info from yahoo-finance
        """
        try:
            url = main_website + current_symbol + stem + current_symbol
            self.read_website(url)

            all_tables = self.soup.find_all('table')

            for table in all_tables:
                table_filled = []
                GetYahooFundamentals.fill_up_table(table, table_filled)
                table_info.append(table_filled)
            pass
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    @staticmethod
    def fill_up_table(input_table, output_table):
        try:
            for row in input_table.find_all('tr'):  # rows
                table_row = []
                number_of_columns = 0
                columns = row.find_all('td')

                for column in columns:
                    text = column.get_text()  # columns
                    if text == u'-':
                        text = NA[1]
                    table_row.append(text)
                    number_of_columns += 1

                output_table.append(table_row)
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

def main():
    try:
        symbols = ["AAPL", "GOOG", "WMT"]
        yahoo_fundamental = GetYahooFundamentals(symbols)
        yahoo_fundamental.get_all_the_fundamentals()
        pass
    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")


if __name__ == "__main__":
    main()
    pass
