
class Labels:

    countries = [           # broker-wise countries

        # America
        u'United States',
        u'Canada',
        u'Mexico',

        # Europe
        u'Austria',
        u'Belgium',
        u'Denmark',  # degiro
        u'France',
        u'Germany',
        u'Greece',  # degiro
        u'Hungary',
        u'Israel',
        u'Italy',
        u'Netherlands',
        u'Norway',
        u'Poland',
        u'Portugal',
        u'Spain',
        u'Sweden',
        u'Switzerland',
        u'United Kingdom',

        # Asia
        u'Australia',
        u'Hong Kong',
        u'India',   #
        u'Japan',
        u'Singapore'
        # u'Bahrain'
    ]

    to_exclude_countries = [
        u'Hungary',
        u'Poland',
        u'India',  #
        ]


    us_exchanges = [u'1', u'2']  # [u'NYSE', u'NASDAQ']
    de_exchanges = [u'104', u'112']  # just frankfurt and berlin the other are:
    #  #, u'123', u'125', u'106', u'107', u'105', u'4']
    # in the same order the following:
    # [u'Frankfurt', u'Berlin', u'Dusseldorf', u'Hamburg', u'Munich', u'Stuttgart', u'TradeGate', u'Xetra']

    suffix_yahoo = []
    exchanges_list = []

    @staticmethod
    def get_yahoo_list_exchanges(country_name):

        # THE FOLLOWING ARE THE EXCHANGES AS FROM YAHOO FINANCE:

        if country_name == u'United States':
            Labels.exchanges_list = [u'NYSE', u'NASDAQ', u'NASDAQ GIDS', u'NYSE MKT', u'NYSEArca',
                     u'New York Board of Trade', u'Dow Jones']
            Labels.suffix_yahoo = ['']
        elif country_name == u'Canada':
            Labels.exchanges_list = [u'CDNX', u'CNQ', u'CSE', u'NEO', u'Toronto', u'TSXV',  u'VAN', ]
            Labels.suffix_yahoo = ['CN', 'TO', 'NE', 'V']
        elif country_name == u'Mexico':
            Labels.exchanges_list = [u'Mexico', u'BIVA']
            Labels.suffix_yahoo = ['MX']

        elif country_name == u'Austria':
            Labels.exchanges_list = [u'Vienna']
            Labels.suffix_yahoo = ['VI']
        elif country_name == u'Belgium':
            Labels.exchanges_list = [u'Brussels Stock Exchange', u'Euronext', u'Brussels']
            Labels.suffix_yahoo = ['BR', 'NX']
        elif country_name == u'Denmark':
            Labels.exchanges_list = [u'Copenhagen']
            Labels.suffix_yahoo = ['CO']
        elif country_name == u'France':
            Labels.exchanges_list = [u'Paris', u'Euronext']
            Labels.suffix_yahoo = ['PA', 'NX']
        elif country_name == u'Germany':
            Labels.exchanges_list = [u'Frankfurt', u'Berlin', u'Munich', u'XETRA', u'Dusseldorf Stock Exchange', u'Hamburg', u'Hanover', u'Struffgart']
            Labels.suffix_yahoo = ['F', 'BE', 'MU', 'DE', 'DU', 'HM', 'HA', 'HE', 'SG']
        elif country_name == u'Greece':
            Labels.exchanges_list = [u'Athens']
            Labels.suffix_yahoo = ['AT']
        elif country_name == u'Hungary':
            Labels.exchanges_list = [u'BUD', u'Budapest']
            Labels.suffix_yahoo = ['BD']
        elif country_name == u'Israel':
            Labels.exchanges_list = [u'Tel Aviv']
            Labels.suffix_yahoo = ['TA']
        elif country_name == u'Italy':
            Labels.exchanges_list = [u'Milan', u'TLX Exchange']
            Labels.suffix_yahoo = ['MI', 'TI']
        elif country_name == u'Netherlands':
            Labels.exchanges_list = [u'Amsterdam', u'Euronext']
            Labels.suffix_yahoo = ['AS', 'NX']
        elif country_name == u'Norway':
            Labels.exchanges_list = [u'Oslo']
            Labels.suffix_yahoo = ['OL']
        elif country_name == u'Poland':
            Labels.exchanges_list = [u'Warsaw']
            Labels.suffix_yahoo = ['']
        elif country_name == u'Portugal':
            Labels.exchanges_list = [u'Lisbon Stock Exchange', u'Lisbon', u'Euronext']
            Labels.suffix_yahoo = ['LS', 'NX']
        elif country_name == u'Spain':
            Labels.exchanges_list = [u'Madrid Stock Exchange CATS', u'LATIBEX', u'Madrid']
            Labels.suffix_yahoo = ['MC']
        elif country_name == u'Sweden':
            Labels.exchanges_list = [u'Stockholm', u'Aktietorget', u'NGM', ]
            Labels.suffix_yahoo = ['ST']
        elif country_name == u'Switzerland':
            Labels.exchanges_list = [u'Swiss', u'VTX', u'Switzerland']
            Labels.suffix_yahoo = ['SW', 'VX']
        elif country_name == u'United Kingdom':
            Labels.exchanges_list = [u'Industry', u'International Orderbook - London', u'London', u'Euronext']
            Labels.suffix_yahoo = ['L', 'IL', 'NX']

        elif country_name == u'Australia':
            Labels.exchanges_list = [u'Sydney', u'Australian']
            Labels.suffix_yahoo = ['AX']
        elif country_name == u'Hong Kong':
            Labels.exchanges_list = [u'Hong Kong']
            Labels.suffix_yahoo = ['HK']
        elif country_name == u'India':
            Labels.exchanges_list = [u'Bombay', u'NSE', u'BSE']
            Labels.suffix_yahoo = ['BO', 'NS']
        elif country_name == u'Japan':
            Labels.exchanges_list = [u'Fukuoka Stock Exchange', u'Tokyo Stock Exchange', u'Sapporo Stock Exchange', u'Tokyo']
            Labels.suffix_yahoo = ['F', 'T', 'S']
        elif country_name == u'Singapore':
            Labels.exchanges_list = [u'Singapore']
            Labels.suffix_yahoo = ['SI']

        return Labels.exchanges_list, Labels.suffix_yahoo

