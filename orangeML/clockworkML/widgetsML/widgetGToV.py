from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table, Domain, ContinuousVariable, DiscreteVariable
from Orange.widgets.widget import Msg
import numpy
import peakutils
from peakutils.plot import plot
from matplotlib import pyplot
from scipy import integrate

class dataProcessing:
    def GToV(self,xInput,yInput):
        """
        Heavily inspired from J. VACHAUDEZ
        """
        T = numpy.diff(xInput).mean()
        Fs = 1/T
        xOutput = xInput
        factor = 1000.0 * 9.81
        yOutput = integrate.cumtrapz(yInput, dx=1.0/Fs) * factor
        yOutput = numpy.insert(yOutput, 0, 0)
        yOutput = yOutput-numpy.mean(yOutput)
        return xOutput,yOutput
    def dataTableBuilder(self, xInput, yInput):
        yInput = numpy.array(yInput)
        xInput = numpy.array(xInput)
        preBuildArray = numpy.stack([xInput, yInput])
        preBuildArray = preBuildArray.swapaxes(0, 1)
        print(preBuildArray)
        domain = Domain([ContinuousVariable("Time"),ContinuousVariable("Acceleration")])
        dataTable = Table(domain, preBuildArray) 
        return dataTable

class widgetGToV(OWWidget):
    name = "Acceleration to velocity"
    icon = "icons/widget1.svg"
    description = "This Widget transform a FFTG into a FFTV"    
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
            formattedDataX = formattedData[:,0]
            formattedDataY = formattedData[:,1]
            dP = dataProcessing()
            [xIntegrated,yIntegrated] = dP.GToV(formattedDataX, formattedDataY)
            dataTableOutput = dP.dataTableBuilder(xIntegrated, yIntegrated)
            self.Outputs.outputWidget.send(dataTableOutput)

        else:
            print("No data supplied !")


if __name__ == "__main__":
    print("Unit test")
