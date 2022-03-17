import psycopg2 as pg
import numpy as np
import datetime
from psycopg2 import Error
from config import config

def connect():
    conn = None
    try:
        params = config()
        print ('Connecting to the PostGreSQL database')
        conn = pg.connect(**params)

        cur = conn.cursor()

        print ('PostgreSQL database version :')
        cur.execute ('SELECT version()')

        db_version = cur.fetchone()
        print (db_version)

        cur.close()
    except (Exception, error) as error:
        print('Error while connecting to the database : ',error)

    finally:
        if conn is not None:
            cur.close()
            conn.close()    
            print ('Database connection closed')


def brg2db(filepath):

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

## Retrieving data about the bearings ##

            vID = int(newLine1[0:11].strip())
            vType = newLine1[11:].strip()
            vBR = int(newLine2[0])
            vFTF = float(newLine2[1])
            vBSF = float(newLine2[2])
            vBPFO = float(newLine2[3])
            vBPFI = float(newLine2[4])
            values = (vID, vType, vBR, vFTF, vBSF, vBPFO, vBPFI)
            insert_brg(query, values)
            print(values)
    

def insert_brg (newQuery, newValues):
    
    params = config()
    conn = pg.connect(**params)
    cur = conn.cursor()

    try:
        cur.execute(newQuery, newValues)
        conn.commit()

    except (Exception, Error) as error:
      print('Error while inserting data : ', error)
    if conn is not None:
            cur.close()
            conn.close()  
            print ('Database connection closed')  
            
def blt2db(filepath):

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
            insert_blt(query, values)
            print (values)

def insert_blt (newQuery, newValues):

    params = config()
    conn = pg.connect(**params)
    cur = conn.cursor()

    try:
        cur.execute(newQuery, newValues)
        conn.commit()

    except (Exception, Error) as error:
        print('Error while inserting data :', error)
    if conn is not None:
        cur.close()
        conn.close()
        print ('Database connection closed')

def meas2db(filepath):
    
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
                    
                    #start = time_temp[0]
                    #step = np.mean(np.diff(time_temp))
                    #stop = step*nb_samples
                    #data_time = (start,stop,step) 

                    values = (date, area, equipment, POM, speed, load, data_vibration, time_temp)
                    insert_meas(query, values)


def insert_meas (newQuery, newValues):

    params = config()
    conn = pg.connect(**params)
    cur = conn.cursor()

    try:
        cur.execute(newQuery, newValues)
        conn.commit()

    except (Exception, Error) as error:
        print('Error while inserting data :', error)
    if conn is not None:
        cur.close()
        conn.close()
        print ('Database connection closed')


if __name__ == '__main__':
    path_brg = r'C:\Users\Lenovo\Documents\Projet MA1\Fichiers BDD\FaultFreqs\Bearings.txt'
    path_blt = r'C:\Users\Lenovo\Documents\Projet MA1\Fichiers BDD\FaultFreqs\Belts.txt'
    path_meas = r'C:\Users\Lenovo\Documents\Projet MA1\Fichiers BDD\Selected\Belt\EC27.13_ZONE1\AVA-20151221.txt'
    #brg2db(path_brg)
    #blt2db(path_blt)
    meas2db(path_meas)
