from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table, Domain, ContinuousVariable, DiscreteVariable
from Orange.widgets.widget import Msg
import numpy
from scipy.fftpack import fft

import matplotlib.pyplot

class dataProcessing:
    def dataTableBuilder(self, xInput, yInput):
        yInput = numpy.array(yInput)
        xInput = numpy.array(xInput)
        preBuildArray = numpy.stack([xInput, yInput])
        preBuildArray = preBuildArray.swapaxes(0, 1)
        print(preBuildArray)
        domain = Domain([ContinuousVariable("Time"),ContinuousVariable("Acceleration")])
        dataTable = Table(domain, preBuildArray) 
        return dataTable

class widgetFormat(OWWidget):
    name = "Data formatter"
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
            dataTableOutput = dP.dataTableBuilder(formatedDataX, formatedDataY)
            self.Outputs.outputWidget.send(dataTableOutput)
        else:
            print("No data supplied !")

if __name__ == "__main__":
    print("Unit Test")