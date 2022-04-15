from utilities.common_methods import getDebugInfo
from utilities import log


class Fineco:
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

            elif self.country in ["Canada"]:
                return self.commissions_canada()

            # 'Germany', 'France', 'United Kingdom', 'Finland', 'Netherlands', 'Portugal', 'Spain', 'Switzerland'
            elif self.country in ['Germany', 'France', 'United Kingdom', 'Finland', 'Netherlands',
                                  'Portugal', 'Spain', 'Switzerland']:
                return self.commissions_europe()

            else:
                return self.commissions_others()

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_usa(self):
        try:
            # This is the commission which is fixed, always the same
            fixed_commission = 12.95  # dollar
            # The following is for the USA
            commission = fixed_commission
            return commission
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_canada(self):
        try:
            # This is the commission which is fixed, always the same
            fixed_commission = 25 * 0.65  # canadian dollars * exchange rate CAD/EUR  = currency in EURO
            # size is supposed to be the number of shares we are buying for the company.
            commission_per_share = 0.01  # canadian dollars
            # The following is for the USA
            commission = fixed_commission + self.size * commission_per_share
            return commission
        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_ita(self):
        try:
            # size is supposed to be the number of shares we are buying for the company.
            commission_percentage = 0.0019  # 1.9 per mille
            amount_spent = self.size * self.buying_price
            minimum = 2.95
            maximum = 19
            commission = commission_percentage * amount_spent
            if commission < minimum:
                commission = minimum
            elif commission > maximum:
                commission = maximum
            return commission

        except Exception as e:
            log.error(f"There is a problem in the code!: {e}\n{getDebugInfo()}")

    def commissions_europe(self):  # it was originally just Germany
        # # Germany, France, UK, Finland, Netherlands, Portugal, Spain, Switzerland
        try:
            # size is supposed to be the number of shares we are buying for the company.
            commission_percentage = 0.0019  # 1.9 per mille
            amount_spent = self.size * self.buying_price
            minimum = 2.95
            maximum = 19
            commission = commission_percentage * amount_spent
            if commission < minimum:
                commission = minimum
            elif commission > maximum:
                commission = maximum
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
