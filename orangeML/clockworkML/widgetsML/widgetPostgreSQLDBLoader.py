from Orange.widgets.widget import OWWidget
from Orange.widgets import settings, widget, gui
from Orange.widgets.widget import Msg
from PyQt5.QtWidgets import *

class widgetPostgreSQLDBLoader(OWWidget):
    name = "PostgreSQL Data Base Loader Widget"
    icon = "icons/widget1.svg"
    description = "Loads and format data from .txt files into a PostgreSQL data base already created"  
    class error(widget.OWWidget.Error):
        defaultError = Msg("Error while treating data")
    
    want_main_area = False
    resizing_enabled = True
    def guiBuilder(self):

        #Create label
        self.hostLbl = QLabel(self)
        self.hostLbl.setText("Host :")
        self.hostLbl.move(10,20)
        self.hostLbl.resize(90, 20)

        self.dataBaseLbl = QLabel(self)
        self.dataBaseLbl.setText("Database :")
        self.dataBaseLbl.move(10,50)
        self.dataBaseLbl.resize(90, 20)

        self.userLbl = QLabel(self)
        self.userLbl.setText("User :")
        self.userLbl.move(10,80)
        self.userLbl.resize(90, 20)

        self.passwdLbl = QLabel(self)
        self.passwdLbl.setText("Password :")
        self.passwdLbl.move(10,110)
        self.passwdLbl.resize(90, 20)

        self.tableLbl = QLabel(self)
        self.tableLbl.setText("Table to fill :")
        self.tableLbl.move(10,150)
        self.tableLbl.resize(200, 20)

        self.tableLbl = QLabel(self)
        self.tableLbl.setText("Source file :")
        self.tableLbl.move(10,210)
        self.tableLbl.resize(200, 20)

        self.hostTxt = QLineEdit(self)
        self.hostTxt.move(100, 20)
        self.hostTxt.resize(100,20)

        self.dataBaseTxt = QLineEdit(self)
        self.dataBaseTxt.move(100, 50)
        self.dataBaseTxt.resize(100,20)

        self.userTxt = QLineEdit(self)
        self.userTxt.move(100, 80)
        self.userTxt.resize(100,20)

        self.passwdTxt = QLineEdit(self)
        self.passwdTxt.setEchoMode(QLineEdit.Password)
        self.passwdTxt.move(100, 110)
        self.passwdTxt.resize(100,20)

        self.tableCmb = QComboBox(self)
        self.tableCmb.addItems(["Bearings","Belts","VibrationData"])
        self.tableCmb.move(10, 180)
        self.tableCmb.resize(190, 20)

        self.validateBtn = QPushButton('Start loading', self)
        self.validateBtn.move(10,300)
        self.validateBtn.resize(190,30)
        self.validateBtn.clicked.connect(self.onClickValB)

        self.fileDlgBtn = QPushButton('Explore', self)
        self.fileDlgBtn.move(100,210)
        self.fileDlgBtn.resize(100,20)
        self.fileDlgBtn.clicked.connect(self.onClickFDB)
        
        self.sourceFileDlg = QFileDialog(self)
        self.sourceFileDlg.setNameFilters(["Text files (*.txt)"])
    
    def onClickFDB(self):
        print("clicked")
        self.sourceFileDlg.exec()
        self.selectedSourceFile = self.sourceFileDlg.getOpenFileName()

    def onClickValB(self):
        print("clicked")
        

    def __init__(self):
        super().__init__()
        self.selectedSourceFile = ""
        self.guiBuilder()
        print(f"The selected source file is : {self.selectedSourceFile}")
        
        
if __name__ == "__main__":
    print("Unit test")
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(widgetPostgreSQLDBLoader).run()