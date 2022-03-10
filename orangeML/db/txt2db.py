import psycopg2 as pg
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
    print ('Database connection closed')
    

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
                
            vID = int(newLine1[0:8].strip())
            vType = newLine1[8:].strip()
            vFreq = float(newLine2[0])
            vSpeed = float(newLine2[1])
            vSheave1 = float(newLine2[2])
            vSheave2 = float(newLine2[3])
            vLength = float(newLine2[4])
            values = (vID, vType, vFreq, vSpeed, vSheave1, vSheave2, vLength)
            insert_blt(query, values)
            print (values)
    print ('Database connection closed')

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



if __name__ == '__main__':
    path_brg = r'C:\Users\Lenovo\Documents\Projet MA1\Fichiers BDD\FaultFreqs\Bearings.txt'
    path_blt = r'C:\Users\Lenovo\Documents\Projet MA1\Fichiers BDD\FaultFreqs\Belts.txt'
    #brg2db(path_brg)
    #blt2db(path_blt)
