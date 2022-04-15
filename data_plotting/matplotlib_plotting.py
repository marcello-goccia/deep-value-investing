import matplotlib.pyplot as plt

from utilities import log


class PlotLine:

    def __init__(self, data, title, labelx, labely):

        self.title = title
        self.labelx = labelx
        self.labely = labely

        if type(data) is list:
            self.plot_list_data(data)
        else:
            self.plot_data(data)

        self.add_informative_text()
        plt.show()

    @staticmethod
    def plot_list_data(data):
        for d, l in zip(data):
            plt.plot(d)
        plt.legend()

        pass

    @staticmethod
    def plot_data(data):
        data.plot()

    def add_informative_text(self):
        plt.xlabel(self.labelx)
        plt.ylabel(self.labely)
        plt.title(self.title)
