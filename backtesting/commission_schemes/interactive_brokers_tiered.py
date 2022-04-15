import backtrader as bt


class InteractiveBrokersTiered(bt.CommInfoBase):
    """
    This is a simple fixed commission scheme when using Fineco as a broker.
    """
    params = (
        ('commission', 0.0035),
        ('stocklike', True),
        ('commtype', bt.CommInfoBase.COMM_FIXED),
        )

    def _getcommission(self, size, price, pseudoexec):
        pass

        # TODO: ...
        raise Exception("NOT DEFINED YET!!!")

        # perc_commission = 0.01
        # minumum_per_order = 1
        # trade_value = size * price
        #
        # maximum_perc_trade_order = trade_value * perc_commission
        #
        # commission = self.p.commission * size
        #
        # if commission > maximum_perc_trade_order:
        #     commission = maximum_perc_trade_order
        #
        # elif commission < minumum_per_order:
        #     commission = minumum_per_order
        #
        # return commission
