from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table
from Orange.widgets.widget import Msg
import numpy
import matplotlib.pyplot
from scipy.fftpack import fft
from scipy import signal

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
        period = numpy.diff(xInput).mean() #determine period by the average of each element minus the one before
        
        start = 0.0
        stop = 1.0/(2.0*period)
        num = int(xLength/2)
        
        xSpectral = numpy.linspace(start, stop, num, dtype = float)
        print("xSpectral is : " , xSpectral)

        #filtering = signal.boxcar(xLength)
        #ywf = fft(yInput*filtering)
        ywf = fft(yInput)
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
        period = numpy.diff(xInput).mean() #determine period by the average of each element minus the one before
        
        start = 0.0
        stop = 1.0/(2.0*period)
        num = int(xLength/2)
        
        xSpectral = numpy.linspace(start, stop, num, dtype = float)
        print("xSpectral is : " , xSpectral)

        #filtering = signal.boxcar(xLength)
        #ywf = fft(yInput*filtering)
        ywf = fft(yInput)
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

        xSpectral = numpy.linspace(0.0, 1.0/(2.0*period), num, dtype=float)
        ywm = fft(yInput)
        ySpectral = (9810 * (numpy.sqrt(2)/2))/(2*num*numpy.pi) * numpy.abs(ywm[0:num])
        
        xSpectral[0] = 0
        ySpectral = numpy.divide(ySpectral[1:],xSpectral[1:])
        ySpectral = numpy.concatenate(([0],ySpectral))

        return [xSpectral , ySpectral]
        xSpectral = numpy.linspace(0.0, 1.0/(2.0*period), num, dtype=float)
        ywm = fft(yInput)
        ySpectral = (9810 * (numpy.sqrt(2)/2))/(2*num*numpy.pi) * numpy.abs(ywm[0:num])
        
        xSpectral[0] = 0
        ySpectral = numpy.divide(ySpectral[1:],xSpectral[1:])
        ySpectral = numpy.concatenate(([0],ySpectral))

        return [xSpectral , ySpectral]

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
        """
        time = numpy.arange(0,100,0.1)
        amplitude = 2*numpy.sin(time)
        amplitude1 = numpy.cos(2*time)
        FFTs1=FFTs()
        [xSpectralFFTG,ySpectralFFTG] = FFTs1.FFTG(time, amplitude + amplitude1)
        [xSpectralFFTV,ySpectralFFTV] = FFTs1.FFTV(time, amplitude + amplitude1)

        # Initialise the subplot function using number of rows and columns
        figure, axis = matplotlib.pyplot.subplots(1,2)
        axis[0].plot(xSpectralFFTG,ySpectralFFTG)
        axis[0].set_title("FFTG")
        axis[0].set_xlabel ('Fréquences (Hz)')
        axis[0].set_ylabel ('Amplitude')
        axis[1].plot(xSpectralFFTV,ySpectralFFTV)
        axis[1].set_title("FFTV")
        axis[1].set_xlabel ('Fréquences (Hz)')
        axis[1].set_ylabel ('Amplitude')
        matplotlib.pyplot.show()
        """
    @Inputs.inputWidget2
    def set_data(self, dataset):
        if dataset is not None:
            print("It works !")
            print(dataset.shuffle())
            print("Column ID is : " , dataset.columns)
            print("Domain is : " , dataset.domain)
            print(dataset)
            self.Outputs.outputWidget2.send(dataset)
            print(f"il s'agit d'un test {dataset[:,0]} voila")
            FFTs1=FFTs()
            [xSpectralFFTG,ySpectralFFTG] = FFTs1.FFTG(dataset[:,0], dataset[:,1])
        else:
            self.infoa.setText('No data on input yet, waiting to get something.')
            self.Outputs.sample.send("Sampled Data")

if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0
    WidgetPreview(widgetFFT).run()
