import psycopg2 as pg
from psycopg2 import Error
"""from config import config"""

"""
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
"""

def brg2db(filepath):

    query = "INSERT INTO Bearings (ID, Type, BR, FTF, BSF, BPFO, BPFI) VALUES (%s, %s, %s, %s, %s, %s, %s)"
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
            print(values)
           # insert_brg(query, values)

    
"""
def insert_brg (newQuery, newValues):
    
    params = config()
    conn = pg.connect(**params)
    cur = conn.cursor()

    try:
        cur.execute(newQuery, newValues)

    except (Exception, error) as error:
      print('Error while inserting data : ', Error)
    finally:
        if conn is not None:
            cur.close()
            conn.close()    
            print ('Database connection closed')

"""

if __name__ == '__main__':
    path = r'C:\Users\Lenovo\Documents\Projet MA1\Fichiers BDD\FaultFreqs\Bearings.txt'
    brg2db(path)
