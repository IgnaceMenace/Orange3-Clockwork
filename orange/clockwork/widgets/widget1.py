from AnyQt.QtWidgets import QLabel
from Orange.widgets.widget import OWWidget


class MyWidget(OWWidget):
    name = "First Widget"
    icon = "icons/widget1.svg"
    
    
    def __init__(self):
        super().__init__()

        label = QLabel("Ca marche ?")
        self.controlArea.layout().addWidget(label)


if __name__ == "__main__":
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0
    WidgetPreview(MyWidget).run()
