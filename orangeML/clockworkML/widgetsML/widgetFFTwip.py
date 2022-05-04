from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table, Domain, ContinuousVariable, DiscreteVariable
from Orange.widgets.widget import Msg
import numpy
from scipy.fftpack import fft

import matplotlib.pyplot

class dataProcessing:
    def fft(self, xInput, yInput):
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
    name = "FFT Widget WIP Rewrite"
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
            rowDataSelected = dataset[[0]]
            formattingData = str(rowDataSelected)
            formattingData = formattingData.split(']')
            formattingData = formattingData[1]
            formattingData = formattingData.replace('[', '')
            formattingData = formattingData.replace(']', '')
            formattingData = formattingData.replace(' ', '')
            formattingData = formattingData.replace('{', '')
            formattingData = formattingData.split(',')
            formatedDataX = []
            formatedDataY = []
            curlyBraceFlag = 0
            for iFD in formattingData:
                if curlyBraceFlag == 1:
                    if iFD.__contains__('}') == True:
                        iFD = iFD.replace('}', '')
                    formatedDataX.append(float(iFD))
                if curlyBraceFlag == 0:
                    if iFD.__contains__('}') == True:
                        iFD = iFD.replace('}', '')
                        curlyBraceFlag = 1
                    formatedDataY.append(float(iFD))
            dP = dataProcessing()
            [xSpectralFFTG,ySpectralFFTG] = dP.fft(formatedDataX, formatedDataY)
            figure, axis = matplotlib.pyplot.subplots(1,2)
            axis[0].plot(xSpectralFFTG,ySpectralFFTG)
            axis[0].set_title("FFTG")
            axis[0].set_xlabel ('Fréquences (Hz)')
            axis[0].set_ylabel ('Amplitude')
            axis[1].plot(formatedDataX,formatedDataY)
            axis[1].set_title("Data")
            axis[1].set_xlabel ('Time [s]')
            axis[1].set_ylabel ('Amplitude')
            matplotlib.pyplot.show()
            dataTableOutput = dP.dataTableBuilder(xSpectralFFTG, ySpectralFFTG)
            print(f"Output data.Table {dataTableOutput}")
            self.Outputs.outputWidget.send(dataTableOutput)
        else:
            print("No data supplied !")

if __name__ == "__main__":
    print("Unit Test")
    dP = dataProcessing()
    xSpectralFFTG = [1,2,3]
    ySpectralFFTG = [4,5,6]
    print(f"Pre processed data \n {[xSpectralFFTG,ySpectralFFTG]} \n *******************")
    dataTableOutput = dP.dataTableBuilder(xSpectralFFTG, ySpectralFFTG)
    print(f"Output data.Table.domain {dataTableOutput.domain}")