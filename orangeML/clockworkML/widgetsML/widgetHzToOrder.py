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
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets

class dataProcessing:
    def hzToOrder(self,xInput,yInput, rpm):
        yOutput = yInput
        xOutput = xInput / (rpm / 60)
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
    name = "Hz to order"
    icon = "icons/widget1.svg"
    description = "Transform your frequential data into order data with original RPM"    
    class Inputs:
        inputWidget = Input("input", Table)
    class Outputs:
        outputWidget = Output("output", Table)
    class error(widget.OWWidget.Error):
        defaultError = Msg("Error while treating data")
    def __init__(self):
        super().__init__()
    want_main_area = False
    resizing_enabled = True
    
    def onClickValB(self):
        self.rpm = self.rSpeedTxt.text()
        dP = dataProcessing()
        [xOrdered,yOrdered] = dP.hzToOrder(self.formattedDataX, self.formattedDataY, int(self.rpm))
        dataTableOutput = dP.dataTableBuilder(xOrdered, yOrdered)
        self.Outputs.outputWidget.send(dataTableOutput)

    def guiBuilder(self):
        self.rSpeedLbl = QLabel(self)
        self.rSpeedLbl.setText("Rotating speed :")
        self.rSpeedLbl.move(10,20)
        self.rSpeedLbl.resize(90, 20)

        self.rSpeedTxt = QLineEdit(self)
        self.rSpeedTxt.move(110, 20)
        self.rSpeedTxt.resize(100,20)
        self.rSpeedTxt.setText("1")

        self.rpmLbl = QLabel(self)
        self.rpmLbl.setText("RPM")
        self.rpmLbl.move(220,20)
        self.rpmLbl.resize(90, 20)

        self.validateBtn = QPushButton('OK', self)
        self.validateBtn.move(220,50)
        self.validateBtn.resize(30,30)
        self.validateBtn.clicked.connect(self.onClickValB)

    @Inputs.inputWidget
    def set_data(self,dataset):
        if dataset is not None:
            formattedData = numpy.array(dataset)
            self.formattedDataX = formattedData[:,0]
            self.formattedDataY = formattedData[:,1]
            self.guiBuilder()

        else:
            print("No data supplied !")

if __name__ == "__main__":
    print("Unit test")