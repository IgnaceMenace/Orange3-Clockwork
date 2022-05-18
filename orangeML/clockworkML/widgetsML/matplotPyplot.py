from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table, Domain, ContinuousVariable, DiscreteVariable
from Orange.widgets.widget import Msg
import numpy
from scipy.fftpack import fft

import matplotlib.pyplot


class widgetPlot(OWWidget):
    name = "Matplotlib pyplot"
    icon = "icons/widget1.svg"
    description = """Widget that plot data in the matplotlib.pyplot way
    for a better visibility"""   
    class Inputs:
        inputWidget = Input("Data to process (input)", Table)
    class Outputs:
        outputWidget = Output("FFT values (output)", Table)
    class error(widget.OWWidget.Error):
        defaultError = Msg("Error while treating data")
    want_main_area = True
    def __init__(self):
        print("init")
    @Inputs.inputWidget
    def set_data(self, dataset):
        if dataset is not None:
            formattedData = numpy.array(dataset)
            formattedDataX = formattedData[:,0]
            formattedDataY = formattedData[:,1]
            matplotlib.pyplot.plot(formattedDataX, formattedDataY)
            matplotlib.pyplot.show()

        else:
            print("No data supplied !")

if __name__ == "__main__":
    print("Unit Test")