from Orange.widgets.widget import OWWidget
from Orange.widgets import settings, widget, gui
from Orange.widgets.widget import Msg
from PyQt5.QtWidgets import *
from PyQt5 import QtWidgets
import psycopg2 as pg
import numpy as np
import datetime
from psycopg2 import Error

class agentPostgreSQLDBLoader:
    def insertToDb (self,newQuery, newValues, paramDb):
        connection = None
        try:
            print ('Connecting to the PostGreSQL database')
            connection = pg.connect(user=paramDb[2],
                                    password=paramDb[4],
                                    host=paramDb[0],
                                    port=paramDb[3],
                                    database=paramDb[1])
            cursor = connection.cursor()
            cursor.execute(newQuery, newValues)
            connection.commit()
        except (Exception, Error) as error:
            print('Error while inserting data : ', error)
        if connection is not None:
                cursor.close()
                connection.close()  
                print ('Database connection closed') 

    def measToDb(self,paramDb):
        filepath = paramDb[6]
        query = "INSERT INTO \"VibrationData\" (\"Date\", \"Area\",\"Equipment\", \"MeasurmentPoint\",\"Speed\", \"Load\", \"Measure\", \"Time\") VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        time_temp = []
        data_vibration = []
        f = open (filepath, 'r')
        for line in f:
            if (line.strip() != ""):
                if (line.strip().split()[0]=="Date/Time:"):
                    DAY = int(line.strip().split(' ')[1].split("/")[0])
                    MONTH = int(line.strip().split(' ')[1].split("/")[1])
                    YEAR = int("20" + line.strip().split(' ')[1].split("/")[2])
                    HOUR = int(line.strip().split(' ')[3].split(":")[0])
                    MIN = int(line.strip().split(' ')[3].split(":")[1])
                    SEC = int(line.strip().split(' ')[3].split(":")[2])
                    date = datetime.datetime(YEAR, MONTH, DAY, HOUR, MIN, SEC)
                    #print (date.strftime("%c"))
                if (line.strip().split()[0]=="Area:"):
                    area = line.strip().split("[")[1].split("]")[0].strip()
                    #area = line.strip().split()[3][1:]   Donne la zone + le client
                if (line.strip().split()[0]=="Equipment:"):
                    equipment = line.strip().split('[')[2][:-1].strip()
                if (line.strip().split()[0]=="Measurement"):
                    POM = line.strip().split('[')[1][0:3]
                if (line.strip().split()[0]=="Speed:"):
                    speed = float(line.strip().split(' ')[1])
                    speed_unit = line.strip().split(' ')[2]                
                if (line.strip().split()[0]=="LOAD:"):
                    load = float(line.strip().split(' ')[1])                
                if (line.strip().split()[0]=="Number"):
                    nb_samples = int(line.strip().split()[3])                
                if (line.strip().split()[0]=="Time"):
                    meas_unit = line.strip().split()[2]
                    # Skip 2 line
                    line = next(f)
                    line = next(f)
                    for j in range(nb_samples):
                        time_temp.append(float(line.split()[0]))
                        data_vibration.append(float(line.split()[1]))
                        line = next(f)
                    values = (date, area, equipment, POM, speed, load, data_vibration, time_temp)
                    self.insertToDb(query, values, paramDb)

    def brg2db(self, paramDb):
        filepath = paramDb[6]
        query = "INSERT INTO \"Bearings\" (\"IDBearing\", \"BearingType\", \"BR\", \"FTF\", \"BSF\", \"BPFO\", \"BPFI\") VALUES (%s, %s, %s, %s, %s, %s, %s)"
        skipCount = 0
        f = open(filepath, 'r')
        for line in f:
            skipCount = skipCount + 1
            if (skipCount > 5):
                currentLine1 =line[0:33]
                currentLine2 = line[33:].split(' ')
                newLine1 = currentLine1
                newLine2 = [x.strip() for x in currentLine2 if x]

                vID = int(newLine1[0:11].strip())
                vType = newLine1[11:].strip()
                vBR = int(newLine2[0])
                vFTF = float(newLine2[1])
                vBSF = float(newLine2[2])
                vBPFO = float(newLine2[3])
                vBPFI = float(newLine2[4])
                values = (vID, vType, vBR, vFTF, vBSF, vBPFO, vBPFI)
                self.insertToDb(query, values, paramDb)
        
    def blt2db(self, paramDb):
        paramDb[6]
        query = "INSERT INTO \"Belts\" (\"IDBelt\", \"BeltType\", \"BeltFreq\", \"Speed2Out\", \"Sheave1\", \"Sheave2\", \"BeltLength\") VALUES (%s, %s, %s, %s, %s, %s, %s)"
        skipCount = 0
        f=open(filepath, 'r')
        for line in f:
            skipCount = skipCount + 1
            if (skipCount > 5):
                currentLine1 = line[0:32]
                currentLine2 = line[32:].split(' ')
                newLine1 = currentLine1
                newLine2 = [x.strip() for x in currentLine2 if x]

                ID=int(newLine1[0:8].strip())
                Type=newLine1[8:].strip()
                Freq=float(newLine2[0])
                Speed=float(newLine2[1])
                Sheave1=float(newLine2[2])
                Sheave2=float(newLine2[3])
                Length=float(newLine2[4])
                values = (ID, Type, Freq, Speed, Sheave1, Sheave2, Length)
                self.insertToDb(query, values, paramDb)

class widgetPostgreSQLDBLoader(OWWidget):
    name = "PostgreSQL Data Base Loader Widget"
    icon = "icons/widget1.svg"
    description = "Loads and format data from .txt files into a PostgreSQL data base already created"  
    class error(widget.OWWidget.Error):
        defaultError = Msg("Error while treating data")
    
    want_main_area = False
    resizing_enabled = True
    def guiBuilder(self):

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

        self.portLbl = QLabel(self)
        self.portLbl.setText("Port :")
        self.portLbl.move(10,110)
        self.portLbl.resize(90, 20)

        self.passwdLbl = QLabel(self)
        self.passwdLbl.setText("Password :")
        self.passwdLbl.move(10,140)
        self.passwdLbl.resize(90, 20)

        self.tableLbl = QLabel(self)
        self.tableLbl.setText("Table to fill :")
        self.tableLbl.move(10,180)
        self.tableLbl.resize(200, 20)

        self.tableLbl = QLabel(self)
        self.tableLbl.setText("Source file :")
        self.tableLbl.move(10,240)
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

        self.portTxt = QLineEdit(self)
        self.portTxt.move(100, 110)
        self.portTxt.resize(100,20)
        self.portTxt.setText("5432")

        self.passwdTxt = QLineEdit(self)
        self.passwdTxt.setEchoMode(QLineEdit.Password)
        self.passwdTxt.move(100, 140)
        self.passwdTxt.resize(100,20)

        self.tableCmb = QComboBox(self)
        self.tableCmb.addItems(["Bearings","Belts","VibrationData"])
        self.tableCmb.move(10, 210)
        self.tableCmb.resize(190, 20)

        self.fileDlgBtn = QPushButton('Explore', self)
        self.fileDlgBtn.move(100,240)
        self.fileDlgBtn.resize(100,20)
        self.fileDlgBtn.clicked.connect(self.onClickFDB)
        
        self.filePathTxt = QLineEdit(self)
        self.filePathTxt.move(10, 270)
        self.filePathTxt.resize(190,20)

        self.sourceFileDlg = QFileDialog(self)

        self.validateBtn = QPushButton('Start loading', self)
        self.validateBtn.move(10,300)
        self.validateBtn.resize(190,30)
        self.validateBtn.clicked.connect(self.onClickValB)
    
    def onClickFDB(self):
        paramDb6Temp = self.sourceFileDlg.getOpenFileName(self,'Open File',"","Text files (*.txt)")
        self.filePathTxt.setText(paramDb6Temp[0])

    def onClickValB(self):
        comp = True
        self.paramDb[0] = self.hostTxt.text()
        self.paramDb[1] = self.dataBaseTxt.text()
        self.paramDb[2] = self.userTxt.text()
        self.paramDb[3] = self.portTxt.text()
        self.paramDb[4] = self.passwdTxt.text()
        self.paramDb[5] = self.tableCmb.currentText()
        self.paramDb[6] = self.filePathTxt.text()
        for i in range(len(self.paramDb)):
            if self.paramDb[i] == "":
                comp = False
        if comp == False:
            error_dialog = QtWidgets.QErrorMessage(self)
            error_dialog.showMessage('One or more missing parameter!')
        if comp == True:
            agent = agentPostgreSQLDBLoader()
            agent.measToDb(self.paramDb)

    def __init__(self):
        super().__init__()
        self.paramDb = [""]*7
        self.guiBuilder()
        
if __name__ == "__main__":
    print("Unit test")
    from Orange.widgets.utils.widgetpreview import WidgetPreview
    WidgetPreview(widgetPostgreSQLDBLoader).run()