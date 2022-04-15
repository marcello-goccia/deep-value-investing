# Extract and analyze companies' fundamental data from Yahoo finance

## Introduction

Public companies' technical data can be obtained from a lot of providers, such as Yahoo Finance, Quandl, Google Finance, etc, whereas few free database and APIs are available for fundamental data. 

Yahoo Finance Key Statistics is a good source for fundamental data, the file `fundamentalData.py` can be used to scrape the data from this webpage, using the python's "BeautifulSoup" package. 

Users can get data for a list of any companies, while in this example, I extracted the data for companies in the S&P 500. The data is got at 11/09/2015. Users can also choose theri own statistics in interest from the total ~60 categories.

## Exploratory Analysis

We first look at the market cap, gross profit and net income information. 

### Market Cap

This is a boxplot of all S&P 500 companies. We observe a lot of outliers with market cap well above the majorities.

<img class=center src=./figs/marketCapBoxplot.png height=450>

This is the market cap of the top 15 companies.

<img class=center src=./figs/marketCap.png height=450>

This is the frequency distribution of companies with market cap below 40 billions. 

<img class=center src=./figs/marketCapMajor.png height=450>

### Gross Profit

This is a boxplot of all S&P 500 companies. Similar to the market cap, a lot of outliers have gross profits well above the majorities.

<img class=center src=./figs/grossProfitBoxplot.png height=450>

This is the gross profit of the top 15 companies.

<img class=center src=./figs/grossProfit.png height=450>

This is the frequency distribution of companies with gross profit below 6 billions. 

<img class=center src=./figs/grossProfitMajor.png height=450>

### Net Income

This is a boxplot of all S&P 500 companies. The outliers are at both sides: some companies gain or lose  far more than the majorities do.

<img class=center src=./figs/netIncomeBoxplot.png height=450>

This is the net income of the top 15 companies.

<img class=center src=./figs/netIncome.png height=450>

This is the frequency distribution of companies with net income between -500 million and 1.5 billions. 

<img class=center src=./figs/netIncomeMajor.png height=450>

A lot of more analysis can be done from this data set, and the code can be extended easily to obtain the historical data.


