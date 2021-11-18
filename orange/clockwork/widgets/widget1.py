from Orange.widgets.widget import OWWidget, Output
from Orange.widgets import gui
from Orange.widgets import settings

class widget1(OWWidget):
    name = "First Widget"
    icon = "icons/widget1.svg"
    description = "First widget, input something and return something else"    
    number = 2
    def __init__(self):
        super().__init__()
        a = float(input("entrer le nombre : "))
        gui.widgetLabel(self.controlArea, "Ca marche ? " + str(a*2))

if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0
    WidgetPreview(widget1).run()
