from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table
from Orange.widgets.widget import Msg

import matplotlib.pyplot

class widget1(OWWidget):
    name = "First Widget"
    icon = "icons/widget1.svg"
    description = "First widget, input something and return something else"    
    class Inputs:
        inputWidget = Input("first input", Table)
    class Outputs:
        outputWidget = Output("first output", Table)
    class error(widget.OWWidget.Error):
        defaultError = Msg("Error while treating data")
    def __init__(self):
        super().__init__()

    @Inputs.inputWidget
    def set_data(self,dataset):
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
                    formatedDataY.append(float(iFD))
                if curlyBraceFlag == 0:
                    if iFD.__contains__('}') == True:
                        iFD = iFD.replace('}', '')
                        curlyBraceFlag = 1
                    formatedDataX.append(float(iFD))

            matplotlib.pyplot.plot(formatedDataY, formatedDataX)
            matplotlib.pyplot.show()
            self.Outputs.outputWidget.send(dataset)

        else:
            print("No data supplied !")


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0
    WidgetPreview(widget1).run()
