import backtrader as bt


class DegiroFixed(bt.CommInfoBase):
    """
    This is a simple fixed commission scheme when using degiro as a broker.
    """
    params = (
        ('commission', 0.50),  # dollars
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_FIXED),
        )

    def _getcommission(self, size, price, pseudoexec):

        # size is supposed to be the number of shares we are buying for the company.
        commission_per_share = 0.004  # dollars
        # The following is for the USA
        commission = self.p.commission + size * commission_per_share
        return commission
