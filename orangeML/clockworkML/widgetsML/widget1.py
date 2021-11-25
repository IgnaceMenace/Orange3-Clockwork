from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table
from Orange.widgets.widget import Msg

class widget1(OWWidget):
    name = "First Widget"
    icon = "icons/widget1.svg"
    description = "First widget, input something and return something else"    
    number = 2
    class input:
        inputwidget1 = Input("first input", int)
    class output:
        ouputwidget1 = Output("first output", int)
    class error(widget.OWWidget.Error):
        defaultError = Msg("Error while treating data")
    
    def __init__(self):
        super().__init__()
        print("test")
        infobox = gui.widgetBox(self.controlArea, "Info")    
        gui.widgetLabel(infobox,"ca marche ??????")
        gui.widgetBox(self.controlArea, "Input status")
#        self.error.defaultError()


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0
    WidgetPreview(widget1).run()
