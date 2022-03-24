import Orange
from PyQt5 import Qt
from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.widgets.widget import Msg

class File(OWWdiget):
    name = "File"
    icon = ""
    description = "Selects a .txt file and forwards its path to the next widget"

    class Outputs:
        outputFile = Output("File path", str)
        outputType = Output ("Data type", str)
    class error(widget.OWWidget.Error):
        defaultError = Msg("Error while retrieving the file")

    def __init__(self):
        super().__init__()

    def selectFile():
        QFileDialog.getOpenFileName()[0]

    def commit(self):
        self.Outputs.outputFile.send(path)
        self.Outputs.outputType.send(dataType)



