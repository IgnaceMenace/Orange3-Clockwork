from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table, Domain
from Orange.widgets.widget import Msg
import numpy
import matplotlib.pyplot
from scipy.fftpack import fft
from scipy import signal
def dataTableBuilder(self, xInput, yInput):
    xInputArray = numpy.array(xInput)
    yInputArray = numpy.array(yInput)
    xDomain = numpy.stack([xInputArray, yInputArray])
    print(xDomain)
    print(xDomain.shape)
    domain = Domain.from_numpy(xDomain)
    dataTableOutput = Table.from_numpy(domain, xDomain)
    return dataTableOutput

class FFTs:
    def FFTG(self,xInput, yInput):
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
        xLength = int(len(xInput)) #determine length of the array
        xSpectral = numpy.linspace(0, int(xLength/2), int(xLength/2))
        yInputArray = numpy.array(yInput)
        yInputArray = yInputArray.swapaxes(0, 1)
        yInputArray2 = yInputArray[0,:]
        ywf = fft(yInputArray2)
        ySpectral = 2.0/xLength * numpy.abs(ywf[0:int(xLength/2)])

        return [xSpectral , ySpectral]

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

class widgetFFT(OWWidget):
    name = "FFT Widget WIP"
    icon = "icons/widget1.svg"
    description = """Widget that calculate the FFTs out vibration data 
    and send the data via in an Orange.Table format"""   
    class Inputs:
        inputWidget2 = Input("Data to process (input)", Table)
    class Outputs:
        outputWidget2 = Output("FFT values (output)", Table)
    class error(widget.OWWidget.Error):
        defaultError = Msg("Error while treating data")
    want_main_area = False 
    def __init__(self):
        print("init")
    @Inputs.inputWidget2
    def set_data(self, dataset):
        if dataset is not None:
            FFTs1=FFTs()
            [xSpectralFFTG,ySpectralFFTG] = FFTs1.FFTG(dataset[:,0], dataset[:,1])
            #self.Outputs.outputWidget2.send(dataTableBuilder(self, dataset[:,0], dataset[:,1]))
            self.Outputs.outputWidget2.send(dataTableBuilder(self, xSpectralFFTG, ySpectralFFTG))
        else:
            self.infoa.setText('No data on input yet, waiting to get something.')
            self.Outputs.sample.send("Sampled Data")

if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(widgetFFT).run()


"""
Make this unit test better 
Clear traffic chen nothing is sent
""" 