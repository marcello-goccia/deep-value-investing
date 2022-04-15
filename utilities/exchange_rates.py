import pyUSDforex

exchange_id = 'a1e1562d0c74449eb6ec0156697f81c0'

# exchange rate to US dollar
# last day 6/8/2019
class Exchange:

    country = {'United States': 'USD',
                        'Canada': 'CAD',
                        'Mexico': 'MXN',
                        'Austria': 'EUR',
                        'Belgium': 'EUR',
                        'Denmark': 'EUR',  # degiro
                        'France': 'EUR',
                        'Germany': 'EUR',
                        'Greece': 'EUR',  # degiro
                        'Hungary': 'HUF',
                        'Israel': 'ILS',
                        'Italy': 'EUR',
                        'Netherlands': 'EUR',
                        'Norway': 'NOK',
                        'Poland': 'PLN',
                        'Portugal': 'EUR',
                        'Spain': 'EUR',
                        'Sweden': 'SEK',
                        'Switzerland': 'CHF',
                        'United Kingdom': 'GBP',
                        'Australia': 'AUD',
                        'Hong Kong': 'HKD',
                        'India': 'INR',  #
                        'Japan': 'JPY',
                        'Singapore': 'SGD'}

    rate = {'EUR': 1.12021,
            'GBP': 1.21634,
            'AUD': 0.675824,
            'CAD': 0.753331,
            'CNY': 0.141662,
            'RUB': 0.0153156,
            'MXN': 0.0510923,
            'TWD': 0.0317862,
            'JPY': 0.00941422,
            'BRL': 0.251570,
            'DKK': 0.150153,
            'INR': 0.0140782,
            'COP': 0.000291670,
            'IDR': 0.0000703104,
            'ZAR': 0.0663717,
            'KRW': 0.000824001,
            'CLP': 0.00139990,
            'ARS': 0.0219736,
            'PHP': 0.0191248,
            'TRY': 0.182054,
            'PEN': 0.295074,
            'ILS': 0.287393,
            'SEK': 0.103754,
            'CHF': 1.02559,
            'NZD': 0.645056,
            'HUF': 0.00343887,
            #'': 1,
            #'': 1,
            }

    rate_test = {'EUR': pyUSDforex.convert(1, 'EUR', exchange_id),
                 'GBP': pyUSDforex.convert(1, 'GBP', exchange_id),
                 'AUD': pyUSDforex.convert(1, 'AUD', exchange_id),
                 'CAD': pyUSDforex.convert(1, 'CAD', exchange_id),
                 'CNY': pyUSDforex.convert(1, 'CNY', exchange_id),
                 'RUB': pyUSDforex.convert(1, 'RUB', exchange_id),
                 'MXN': pyUSDforex.convert(1, 'MXN', exchange_id),
                 'TWD': pyUSDforex.convert(1, 'TWD', exchange_id),
                 'JPY': pyUSDforex.convert(1, 'JPY', exchange_id),
                 'BRL': pyUSDforex.convert(1, 'BRL', exchange_id),
                 'DKK': pyUSDforex.convert(1, 'DKK', exchange_id),
                 'INR': pyUSDforex.convert(1, 'INR', exchange_id),
                 'COP': pyUSDforex.convert(1, 'COP', exchange_id),
                 'IDR': pyUSDforex.convert(1, 'IDR', exchange_id),
                 'ZAR': pyUSDforex.convert(1, 'ZAR', exchange_id),
                 'KRW': pyUSDforex.convert(1, 'KRW', exchange_id),
                 'CLP': pyUSDforex.convert(1, 'CLP', exchange_id),
                 'ARS': pyUSDforex.convert(1, 'ARS', exchange_id),
                 'PHP': pyUSDforex.convert(1, 'PHP', exchange_id),
                 'TRY': pyUSDforex.convert(1, 'TRY', exchange_id),
                 'PEN': pyUSDforex.convert(1, 'PEN', exchange_id),
                 'ILS': pyUSDforex.convert(1, 'ILS', exchange_id),
                 'SEK': pyUSDforex.convert(1, 'SEK', exchange_id),
                 'CHF': pyUSDforex.convert(1, 'CHF', exchange_id),
                 'NZD': pyUSDforex.convert(1, 'NZD', exchange_id),
                 'HUF': pyUSDforex.convert(1, 'HUF', exchange_id),
                 #'': 1,
                 #'': 1,
            }

    @staticmethod
    def get_value_in_usd(value, currency):
        exchange_rate = Exchange.get_rate(currency)
        if exchange_rate is None:
            return None
        else:
            converted_value = value * exchange_rate
            return converted_value

    @staticmethod
    def get_exchange_rate_from_currency(currency):
        """
        It returns the correct exchange rate (with respect to the USD) given the currency as input variable
        @param currency the currency used by the stock
        @return the exchange rate to be used for the calculation
        """
        exchange = 1
        if not currency:
            currency = 'USD'
        if currency != 'USD':
            exchange = Exchange.get_rate(currency)
        return exchange

    # @staticmethod
    # def get_rate(currency):
    #     exchange_rate = Exchange.rate[currency]
    #     return exchange_rate

    @staticmethod
    def get_rate(currency):
        exchange_rate = pyUSDforex.convert(1, currency, exchange_id)
        exchange_rate = float(exchange_rate)
        return exchange_rate
