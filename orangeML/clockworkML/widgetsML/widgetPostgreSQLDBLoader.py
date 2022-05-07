from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table
from Orange.widgets.widget import Msg

class widgetPostgreSQLDBLoader(OWWidget):
    name = "PostgreSQL Data Base Loader Widget"
    icon = "icons/widget1.svg"
    description = "Loads and format data from .txt files into a PostgreSQL data base already created"    
    class error(widget.OWWidget.Error):
        defaultError = Msg("Error while treating data")
    def __init__(self):
        super().__init__()
        """
        # Write the code here
        """


if __name__ == "__main__":
    print("Unit test")
