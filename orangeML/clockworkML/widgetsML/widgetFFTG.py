from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table, Domain, ContinuousVariable, DiscreteVariable
from Orange.widgets.widget import Msg
import numpy
from scipy.fftpack import fft

import matplotlib.pyplot

class dataProcessing:
    def FFTG(self, xInput, yInput):
        """
        This function calculate the Frequential Fourier Transform in Acceleration 

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
        period = numpy.diff(xInput,n=1,axis=0).mean()
        start = 0.0
        stop = 1.0/(2.0*period)
        num = int(xLength/2)
        ywm = fft(yInput)
        xSpectral = numpy.linspace(start, stop, num, dtype = float)
        ySpectral = 2.0/xLength * numpy.abs(ywm[0:int(xLength/2)])
        return xSpectral, ySpectral
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
    name = "FFTG"
    icon = "icons/widget1.svg"
    description = """Widget that calculate the FFTs out vibration data 
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
            [xSpectralFFTG,ySpectralFFTG] = dP.FFTG(formattedDataX, formattedDataY)
            dataTableOutput = dP.dataTableBuilder(xSpectralFFTG, ySpectralFFTG)
            self.Outputs.outputWidget.send(dataTableOutput)
        else:
            print("No data supplied !")

if __name__ == "__main__":
    print("Unit Test")