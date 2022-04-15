from utilities.common_methods import getDebugInfo
from utilities import log


class Directa:
    def __init__(self):
        try:
            self.commissions = 0
            self.country = None
            self.size = 0
            self.buying_price = 0
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def set_country(self, country):
        try:
            self.country = country
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def get_commission(self, size=None, buying_price=None):
        try:
            self.size = size
            self.buying_price = buying_price

            if not self.size:
                raise Exception("Please define the size of the bulk of stock you are going to buy.")

            if not self.buying_price:
                raise Exception("Please define the buying price of the bulk of stock you are going to buy.")

            if not self.country:
                raise Exception("Please define the country you are investing in.")

            if self.country in ["United States"]:
                return self.commissions_usa()

            elif self.country in ["Italy"]:
                return self.commissions_ita()

            elif self.country in ['Austria', 'Belgium', 'Denmark', 'France', 'Germany', 'Netherlands', 'Norway',
                                  'Portugal', 'Spain', 'Sweden', 'Switzerland', 'United Kingdom']:
                return self.commissions_europe()

            else:
                return self.commissions_others()

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_usa(self):
        try:
            # This is the commission which is fixed, always the same
            fixed_commission = 9  # dollar
            # size is supposed to be the number of shares we are buying for the company.
            commission_per_share = 0  # dollars
            # The following is for the USA
            commission = fixed_commission + self.size * commission_per_share
            return commission
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_ita(self):
        try:
            # This is the commission which is fixed, always the same
            fixed_commission = 5  # not used
            # size is supposed to be the number of shares we are buying for the company.
            commission_percentage = 0.0019  # 1.9 per mille
            amount_spent = self.size * self.buying_price
            minimum = 1.5
            maximum = 18
            commission = commission_percentage * amount_spent
            if commission < minimum:
                commission = minimum
            elif commission > maximum:
                commission = maximum
            return commission

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_europe(self):  # it was originally just Germany
        # # Austria, Belgio, Danimarca, Finlandia, Francia, Germany, Irlanda, Norvegia, Paesi Bassi, Portogallo,
        # # Regno Unito, Spagna, Svezia, Svizzera
        try:
            # This is the commission which is fixed, always the same
            fixed_commission = 5
            # size is supposed to be the number of shares we are buying for the company.
            commission_percentage = 0.00025  # 0.25 per mille
            amount_spent = self.size * self.buying_price
            minimum = 9.5  # euro
            commission = commission_percentage * amount_spent
            if commission < minimum:
                commission = minimum
            return commission

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_switzerland(self):
        try:
            # This is the commission which is fixed, always the same
            fixed_commission = 5
            # size is supposed to be the number of shares we are buying for the company.
            commission_percentage = 0.0003  # 0.3 per thousand
            amount_spent = self.size * self.buying_price
            minimum = 20 * 0.94  # 20 CHF * exchange rate euro = currency in euro
            commission = commission_percentage * amount_spent
            if commission < minimum:
                commission = minimum
            return commission
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_others(self):
        try:
            # To define:::
            # This is the commission which is fixed, always the same
            fixed_commission = 20
            # size is supposed to be the number of shares we are buying for the company.
            commission_per_price = 0.0016  # dollars
            # The following is the commission price
            commission = fixed_commission + self.size * self.buying_price * commission_per_price
            return commission
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
