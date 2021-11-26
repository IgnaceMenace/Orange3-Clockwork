import numpy
from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table
from Orange.widgets.widget import Msg

class widget2(OWWidget):
    name = "Second Widget"
    icon = "icons/widget1.svg"
    description = "Testing the orange documentation"    

    class Inputs:
        inputWidget2 = Input("Second input", Table)
    class Outputs:
        ouputWidget2 = Output("Second output", Table)
    class error(widget.OWWidget.Error):
        defaultError = Msg("Error while treating data")
    want_main_area = False

    def __init__(self):
        super().__init__()
        infobox = gui.widgetBox(self.controlArea, "Info")
        infoa = gui.widgetLabel(infobox, 'No data on input yet, waiting to get something.')
#        self.error.defaultError()

    @Inputs.inputWidget2
    def set_data(self, dataset):
        if dataset is not None:
            print("It works !")
            self.Outputs.ouputWidget2.send(dataset)
        else:
            self.infoa.setText('No data on input yet, waiting to get something.')
            self.Outputs.sample.send("Sampled Data")
if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(widget2).run()

