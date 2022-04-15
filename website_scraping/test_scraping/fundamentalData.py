import pandas as pd
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen, URLError
from utilities.common_methods import getDebugInfo
from utilities import log

current_path = './fundamentals/yahoo_finance/'

#sp500 = pd.read_csv(current_path + "S&P500.csv", header = 0)
#symbols = sp500.Symbol

symbols = ["AAPL", "GOOG", "WMT"]

keyStatistics = [
    # Valuation Measures
    "Market Cap",
    "Enterprise Value",
    "Trailing P/E",
    "Forward P/E",
    "PEG Ratio",
    "Price/Sales",
    "Price/Book", # "Price/Book (mrq)",
    "Enterprise Value/Revenue",
    "Enterprise Value/EBITDA",

    # Fiscal Year
    "Fiscal Year Ends",
    "Most Recent Quarter",

    # Profitability
    "Profit Margin",  # "Profit Margin (ttm)",
    "Operating Margin",  # "Operating Margin (ttm)",

    # Management Effectiveness
    "Return on Assets",
    "Return on Equity",

    # Income Statement
    "Revenue",  # "Revenue (ttm)"
    "Revenue Per Share",
    "Quarterly Revenue Growth",
    "Gross Profit",  # "Gross Profit (ttm)",
    "EBITDA",
    "Net Income Avi to Common",
    "Diluted EPS",
    "Quarterly Earnings Growth",

    # Balance Sheet
    "Total Cash",
    "Total Cash Per Share",
    "Total Debt",
    "Total Debt/Equity",
    "Current Ratio",
    "Book Value Per Share",

    # Cash Flow Statement
    "Operating Cash Flow",
    "Levered Free Cash Flow",

    # Stock Price History
    "Beta",
    #"52-Week Change",
    #"S&P500 52-Week Change",
    #"52-Week High ",
    #"52-Week Low ",
    #"50-Day Moving Average",
    #"200-Day Moving Average",
    # Share Statistics
    "Avg Vol (3 month)",
    "Avg Vol (10 day)",
    "Shares Outstanding",
    "Float",
    "% Held by Insiders",
    "% Held by Institutions",
    "Shares Short",
    "Short Ratio",
    "Short % of Float",
    "Short % of Shares Outstanding",
    "Shares Short (prior month",

    # Dividend  & Splits
    "Forward Annual Dividend Rate",
    "Forward Annual Dividend Yield",
    "Trailing Annual Dividend Yield",
    "Trailing Annual Dividend Yield",
    "5 Year Average Dividend Yield",
    "Payout Ratio",
    "Dividend Date",
    "Ex-Dividend Date",
    "Last Split Factor (new per old)",
    "Last Split Date"
]

result = pd.DataFrame(index = symbols, columns = keyStatistics)

def getValue(allTd, keyStatistic):
    try:
        for t in allTd:
            p = t.parent
            escaped = re.escape("%s" % keyStatistic)
            compiled = re.compile(escaped)
            tdValue = p.find(text=compiled)
            if tdValue:
                return tdValue.findNext('td').text

        return "N/A"
    except Exception as e:
        log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")


for symbol in symbols:
    url = 'https://finance.yahoo.com/quote/'+symbol+'/key-statistics?ltr=1'
    #url = 'http://finance.yahoo.com/q/ks?s='+symbol+'+Key+Statistics'
    try:
        resp = urlopen(url)
    except URLError as e:
        raise Exception("Cannot open url.")    
    soup = BeautifulSoup(resp.read(), 'html.parser')

    # for debugging purposes write dowen the website.
    text_file = open(current_path + 'Output.txt', "w")
    text_file.write(soup.prettify())
    text_file.close()
    #print(soup.prettify())

    #allTd = soup.find_all('td', attrs={'class':'yfnc_tablehead1'})
    allTd = soup.find_all('td', attrs={'class':'Fz(s) Fw(500) Ta(end)'})
    #
    for keyStatistic in keyStatistics:
        output = getValue(allTd, keyStatistic)
        result.ix[symbol, keyStatistic] = output

    pass
	
#print result 
result.to_csv(current_path + "fundamentalData.csv", header=True, index=True, index_label="symbol")
pass
