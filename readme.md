# Finding deep valued companies

I wrote this code more than two year ago. I wanted to write an algorithm which would allow me to find the best equities 
around the world based on their fundamentals.
The code works and, at that time, I managed to successfully get all the data and the information needed. I back-tested 
the implemented algorithms and it was very useful and informative.
The first and major obstacle was of course to get the data: there are several python packages that would allow me
to get equity prices from yahoo finance, but first, I came to know that yahoo finance was stopping providing this
service, and second I wanted to focus on the fundamental data, and I did not find useful packages which allowed
me to get that for all the countries around the world (indeed I could find for the US market, but I wanted a broad one).

I released this code just as demonstration.

### Website Scraping

I found investing.com has a lof of useful data, with equity prices for all around the world,
together with fundamental data up to 4 years, from annual reports and quarterly reports. 
But how to get that? Of course by web-scraping! Also, this allowed me to get exactly the data I needed.
The scraping algorithm works by initially retrieving the links for all the equities of the countries that appear
in a list. The names and the links for all these equities are stored in a database.
Then the scraping algorithm is run again but this time it retrieved all the useful data for each equity in te database.

The information obtained for each equity is the following:

* data from the stock general page
* information form the company profile: industry, sector, country
* historical data
* info from the financial summary
* annual and quarterly data of the income statement for the past 4 years
* annual and quarterly data of the balance sheet for the past 4 years
* annual and quarterly data of the cash flow statement for the past 4 years
* all the company and industry ratios
* the historical distributed dividends
* the historical earnings

There is also a section where I directly scrape some data from yahoo finance.

### Data Storing

All the data was stored in a sqlite database.

### Fundamentals

This package is a collection of different strategies to help me to detect valuable companies.

Some used strategies are:
* From the Acquirers Multiple book
* Piotrosky F-score
* The strategy that gave best results in the book "What works in Wall Street"

The package also contains numerous measures used by the strategies listed above and many more (I do not list them here 
because are too many).

### Technical Analysis

There is also a package with some simple technical analysis strategies. I wrote them for testing the goodness of the 
technical analysis in the long run. 

### Back-testing

Finally, a package for the back-testing. Of course all the strategies need to be tested. Tests include taxes and 
commissions.
For back-testing I was using the data scraped out of the website, up to 4-5 years. 
At the moment I could not do more, of course with time tests became more accurate because I could collect more data.  

### Data Monitoring

The purpose of this package was to be used with the technical analysis, constantly monitor the stocks 
and if/when a condition was met, the application was supposed to email me and  alert me with the info.

### Data plotting

A package to plot data data and the results obtained.

### Running the code

To scrape the list of assets run the following file:
- /website_scraping/run_to_scrape_list_of_assets.py

To scrape all the company information run the following:
- /website_scraping/run_to_scrape_full_company.py

To back-testing the strategy run the following:
- /backtesting/run_me_to_backtest.py
