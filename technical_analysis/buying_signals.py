
from utilities import log


class BuyingSignals:

    def __init__(self):
        pass

    @classmethod
    def ma_buying_signal(self, mas, shorter, longer):
        """
        @function sma_buying_signal
        It returns true if there is a buying signal, based on the study
        of the simple moving averages (50 and 200)
        @param dataframe
        @return trus is a buyng signal
        """
        print(f"last element MA {shorter}: {mas[shorter][-1]}")
        print(f"last element MA {longer}:  {mas[longer][-1]}")

        # takes the last values of the moving averages and does the check.
        if (mas[shorter][-1] > mas[longer][-1]):
            return True
        else:
            return False



