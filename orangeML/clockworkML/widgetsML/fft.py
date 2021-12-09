import Orange
from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table
from Orange.widgets.widget import Msg
import numpy
from scipy.fftpack import fft
from scipy import signal

class widgetFFT(OWWidget):
    name = "FFT Widget"
    icon = "icons/widget1.svg"
    description = "Calculate the FFTG and FFTV"      
    class Inputs:
        inputWidgetFFT = Input("input widget FFT", Table)
    class Outputs:
        ouputWidgetFFT = Output("input widget FFT", Table)
#    class error(widget.OWWidget.Error):
#        defaultError = Msg("Error while treating data")
#    want_main_area = False

    def __init__(self):
        super().__init__()
        infobox = gui.widgetBox(self.controlArea, "Info")
        infoa = gui.widgetLabel(infobox, 'No data on input yet, waiting to get something.')
#        self.error.defaultError()
        xArray = numpy.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
        yArray = numpy.array([15, 25, 35, 45, 55, 65, 75, 85, 95, 105])

        def FFTG(xInput, yInput):
            xLength = int(len(xInput))
            period = numpy.diff(xInput).mean()
        
            start = 0.0
            stop = 1.0/(2.0*period)
            num = int(xLength/2)
            xSpect = numpy.linspace(start, stop, num, dtype = float)
            print(xSpect)

            filtering = signal.boxcar(xLength)
            ywf = fft(yInput*filtering)
            ySpect = 2.0/xLength * numpy.abs(ywf[0:int(xLength/2)])
        FFTG(xArray, yArray)

    @Inputs.inputWidgetFFT
    def set_data(self, dataset):
        if dataset is not None:
            print("test")
#            self.Outputs.ouputWidget2.send(dataset)
        else:
            self.infoa.setText('No data on input yet, waiting to get something.')
            self.Outputs.sample.send("Sampled Data")
if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(widgetFFT).run()

