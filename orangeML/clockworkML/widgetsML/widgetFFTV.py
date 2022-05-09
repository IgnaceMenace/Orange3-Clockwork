from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table, Domain, ContinuousVariable, DiscreteVariable
from Orange.widgets.widget import Msg
import numpy
from scipy.fftpack import fft

import matplotlib.pyplot

class dataProcessing:
    def FFTV(self,xInput,yInput):
        """
        This function calculate the Frequential Fourier Transform in Velocity 

        Parameters
        ----------
        xInput : array
            Array of a certain size that represent the temporal window
        yInput : array
            Array filled with the temporal response associated with every values of the xInput

        Returns
        -------
        xSpectral : array
            Array filled with the frequential window
        ySpectral : array
            Array filled with the amplitude associated with each frequency 
        """
        xLength = int(len(xInput))
        period = numpy.diff(xInput).mean()
        start = 0.0
        stop = 1.0/(2.0*period)
        num = int(xLength/2)
        xSpectral = numpy.linspace(0.0, 1.0/(2.0*period), num, dtype=float)
        ywm = fft(yInput)
        ySpectral = (9810 * (numpy.sqrt(2)/2))/(2*num*numpy.pi) * numpy.abs(ywm[0:num])
        xSpectral[0] = 0
        ySpectral = numpy.divide(ySpectral[1:],xSpectral[1:])
        ySpectral = numpy.concatenate(([0],ySpectral))
        return xSpectral , ySpectral
    def dataTableBuilder(self, xInput, yInput):
        yInput = numpy.array(yInput)
        xInput = numpy.array(xInput)
        preBuildArray = numpy.stack([xInput, yInput])
        preBuildArray = preBuildArray.swapaxes(0, 1)
        print(preBuildArray)
        domain = Domain([ContinuousVariable("Time"),ContinuousVariable("Acceleration")])
        dataTable = Table(domain, preBuildArray) 
        return dataTable

class widgetFFT(OWWidget):
    name = "FFTV"
    icon = "icons/widget1.svg"
    description = """Widget that calculate the FFTV out vibration data 
    and send the data via in an Orange.Table format"""   
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

            dP = dataProcessing()
            [xSpectralFFTV,ySpectralFFTV] = dP.FFTV(formattedDataX, formattedDataY)
            dataTableOutput = dP.dataTableBuilder(xSpectralFFTV, ySpectralFFTV)
            self.Outputs.outputWidget.send(dataTableOutput)
        else:
            print("No data supplied !")

if __name__ == "__main__":
    print("Unit Test")
