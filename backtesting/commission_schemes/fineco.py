import backtrader as bt


class Fineco(bt.CommInfoBase):
    """
    This is a simple fixed commission scheme when using Fineco as a broker.
    """
    params = (
        ('commission', 19),
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_FIXED),
        )

    def _getcommission(self, size, price, pseudoexec):
        #print(f"current price: {price}, and size: {size}, and commission {self.p.commission}")
        return self.p.commission

