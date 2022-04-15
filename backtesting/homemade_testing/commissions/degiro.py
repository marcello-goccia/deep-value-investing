from utilities.common_methods import getDebugInfo
from utilities import log


class DeGiro:
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

            elif self.country in ['Greece',  'Israel', 'Mexico']:
                return self.commissions_east_europe()

            elif self.country in ["Canada"]:
                return self.commissions_canada()

            elif self.country in ['Australia', 'Hong Kong', 'Japan', 'Singapore']:
                return self.commissions_asia()

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_usa(self):
        try:
            # This is the commission which is fixed, always the same
            fixed_commission = 0.50
            # size is supposed to be the number of shares we are buying for the company.
            commission_per_share = 0.004  # dollars
            # The following is for the USA
            commission = fixed_commission + self.size * commission_per_share
            return commission
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_europe(self):
        # # Austria, Belgio, Danimarca, Finlandia, Francia, Germany, Irlanda, Norvegia, Paesi Bassi, Portogallo,
        # # Regno Unito, Spagna, Svezia, Svizzera
        try:
            # This is the commission which is fixed, always the same
            fixed_commission = 4
            # size is supposed to be the number of shares we are buying for the company.
            commission_per_price = 0.0005  # dollars
            # The following is the commission price
            commission = fixed_commission + self.size * self.buying_price * commission_per_price
            return commission
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_ita(self):
        try:
            # This is the commission which is fixed, always the same
            fixed_commission = 0.50
            # size is supposed to be the number of shares we are buying for the company.
            commission_per_price = 0.0005  # dollars
            # The following iis the commission price
            commission = fixed_commission + self.size * self.buying_price * commission_per_price
            return commission
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_canada(self):
        try:
            # This is the commission which is fixed, always the same
            fixed_commission = 2
            # size is supposed to be the number of shares we are buying for the company.
            commission_per_share = 0.01  # canadian dollars
            # The following is for the USA
            commission = fixed_commission + self.size * commission_per_share
            return commission
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_asia(self):
        # ## Australia, Hong Kong, Giappone, Singapore
        try:
            # This is the commission which is fixed, always the same
            fixed_commission = 10
            # size is supposed to be the number of shares we are buying for the company.
            commission_per_price = 0.0006  # dollars
            # The following is the commission price
            commission = fixed_commission + self.size * self.buying_price * commission_per_price
            return commission
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_east_europe(self):
        # ## Repubblica Ceca, Grecia, Turchia, Ungheria
        try:
            # This is the commission which is fixed, always the same
            fixed_commission = 10
            # size is supposed to be the number of shares we are buying for the company.
            commission_per_price = 0.0016  # dollars
            # The following is the commission price
            commission = fixed_commission + self.size * self.buying_price * commission_per_price
            return commission
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")
