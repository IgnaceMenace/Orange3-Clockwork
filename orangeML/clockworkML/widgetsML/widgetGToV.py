from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table
from Orange.widgets.widget import Msg
import numpy
import peakutils
from peakutils.plot import plot
from matplotlib import pyplot

class dataProcessing:
    def GToV(self,X,Y):
        print("********************************************")


class widgetPeakFinder(OWWidget):
    name = "Peak Finder Widget"
    icon = "icons/widget1.svg"
    description = "This Widget finds the peak in a 2 dimension array"    
    class Inputs:
        inputWidget = Input("input", Table)
    class Outputs:
        outputWidget = Output("output", Table)
    class error(widget.OWWidget.Error):
        defaultError = Msg("Error while treating data")
    def __init__(self):
        super().__init__()

    @Inputs.inputWidget
    def set_data(self,dataset):
        if dataset is not None:
            formattedData = numpy.array(dataset)
            dp = dataProcessing()
            [PASFINI,HEIN] = dp.GToV(formattedData[:,0], formattedData[:,1])
            self.Outputs.outputWidget.send(dataset)

        else:
            print("No data supplied !")


if __name__ == "__main__":
    print("Unit test")
