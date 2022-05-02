import numpy as np
import peakutils 
from scipy.fftpack import fft
from matplotlib import pyplot as plt
from peakutils.plot import plot as pplot


def FFTG(xInput, yInput, RotationFreq):
    xLength = int(len(xInput)) #determine length of the array
    period = np.diff(xInput).mean() #determine period by the average of each element minus the one before
    
    start = 0.0  # 1st x value
    stop = 1.0/(2.0*period)  #last x value
    num = int(xLength/2)
    ywm = fft(yInput)
    
    xSpect = np.linspace(start, stop, num, dtype = float)
    xSpect = xSpect/RotationFreq
    ySpect = 2.0/xLength * np.abs(ywm[0:int(xLength/2)])
    plt.figure()
    plt.plot(xSpect,ySpect)
    plt.title('FFTG')
    plt.xlabel('Ordre')
    plt.ylabel('Amplitude')
    plt.show()

    #indexes = peakutils.indexes(ySpect, thres = 0.1, min_dist = 0)
    #peaks = (xSpect[indexes], ySpect[indexes])
    #
    #for value in indexes:
    #    print ("(",xSpect[value],",",ySpect[value],",", value,")")
    #plt.figure()
    #pplot(xSpect,ySpect, indexes)
    #plt.title('Détection des pics')
    #plt.xlabel('Ordre')
    #plt.ylabel('Amplitude')
    #plt.legend()
    #plt.show()

    print ("FFTG :")
    FaultFinderBearings(xSpect,ySpect)

def FFTV(xInput,yInput, RotationFreq):
    xLength = int(len(xInput))
    Period = np.diff(xInput).mean()
    
    start = 0.0
    stop = 1.0/(2.0*Period)
    num = int(xLength/2)

    x_spect = np.linspace(0.0, 1.0/(2.0*Period), num, dtype=float)
    ywm = fft(yInput)
    y_spect = (9810 * (np.sqrt(2)/2))/(2*num*np.pi) * np.abs(ywm[0:num])
    
    x_spect[0] = 0
    x_spect = x_spect/RotationFreq  
    y_spect = np.divide(y_spect[1:],x_spect[1:])
    y_spect = np.concatenate(([0],y_spect))

    plt.figure()
    plt.plot(x_spect,y_spect)
    plt.title('FFTV')
    plt.xlabel('Ordre')
    plt.ylabel('Amplitude')
    plt.show()

    #indexes = peakutils.indexes(y_spect, thres = 0.1, min_dist = 0)
    #peaks_x = (x_spect[indexes])
    #peaks_y = (y_spect[indexes])
    #for value in indexes:
    #    print ("Peaks : (",x_spect[value],",",y_spect[value],",", value,")")
    #print ("Peaks v2 : (",peaks_x,",",peaks_y,")")
    #plt.figure()
    #pplot(x_spect,y_spect, indexes)
    #plt.title('Détection des pics')
    #plt.xlabel('Ordre')
    #plt.ylabel('Amplitude')
    #plt.legend()
    #plt.show()
    print ("FFTV : ")
    FaultFinderBearings(x_spect,y_spect)


def FaultFinderBearings(x, y):

    indexes = peakutils.indexes(y, thres = 0.06, min_dist = 0, thres_abs=True)
    peaks_x = (x[indexes])
    peaks_y = (y[indexes])
    for value in indexes:
        print ("Peaks : (",x[value],",",y[value],",", value,")")
    print ("Peaks v2 : (",peaks_x,",",peaks_y,")")

    
# On divise les fréquences (en ordres) en plusieurs zones pour analyse approfondie et détection des défauts
                    #splitSub = peaks_x.searchsorted([0,1])
                    #splitLow = peaks_x.searchsorted([1, 2.5])
                    #splitMid = peaks_x.searchsorted([2.5, 4.5])
                    #splitHigh = peaks_x.searchsorted([4.5, 20.5])
                    #splitVeryHigh = peaks_x.searchsorted([20.5, 1000])
                    #xLow = np.split(peaks_x,splitLow)
                    #xMid = np.split(peaks_x,splitMid)
                    #xHigh = np.split(peaks_x,splitHigh)
                    #xVeryHigh = np.split(peaks_x,splitVeryHigh)
                     # peut être utile plus tard ou probablement pas mdr, ça permet de split un array dans 2 (qui du coup fait 2 array dans 1 array)

    #contiennent les valeurs en fréquence des pics
    xSub = peaks_x[peaks_x <= 1] 
    xLow = peaks_x[(peaks_x > 1) & (peaks_x <= 2.5)] 
    xMid = peaks_x[(peaks_x > 2.5) &(peaks_x <= 4.5)] 
    xHigh = peaks_x[(peaks_x > 4.5) & (peaks_x <= 20.5)] 
    xVeryHigh = peaks_x[(peaks_x > 20.5) & (peaks_x < 1000)]

    #Récupérer les index pour ensuite récupérer les coordonnées en y par zone

    xSubIndexes = np.nonzero(peaks_x <= 1) 
    xLowIndexes = np.nonzero((peaks_x > 1) & (peaks_x <= 2.5)) 
    xMidIndexes  = np.nonzero((peaks_x > 2.5) & (peaks_x <= 4.5)) 
    xHighIndexes = np.nonzero((peaks_x > 4.5) & (peaks_x <= 20.5)) 
    xVeryHighIndexes =  np.nonzero((peaks_x > 20.5) & (peaks_x < 1000)) 

    # Récupérer les coordonnées en y
    
    ySub = peaks_y[xSubIndexes]
    yLow = peaks_y[xLowIndexes]
    yMid = peaks_y[xMidIndexes]    
    yHigh = peaks_y[xHighIndexes]   
    yVeryHigh = peaks_y[xVeryHighIndexes]

    print ("Tentative : (",xSub,", oui ,",ySub,")")

    # Analyse des fréquences sous la fréquence de rotation de la machine (sous l'ordre 1) [pas finito]

        #On récup le pic max
    ySubMax = max(ySub)
    ySubMaxIndex = ySub.argmax()
    xSubMax = xSub[ySubMaxIndex]
    print("Sous 1 ordre, pic maximum : (",xSubMax,",",ySubMax,")")

        #FTF - Cage - On cherche un pic aux multiples de la fréquence du pic max
    
    FtfCheck1 = xSubMax*2
    FtfCheck2 = xSubMax*3
    FtfCheck3 = xSubMax*4
    FtfCheckIndex1 = np.nonzero(peaks_x == (xSubMax*2))
    FtfCheckIndex2 = np.nonzero((peaks_x > (xSubMax*3-0.01)) & (peaks_x < (xSubMax*3+0.01)))
    FtfCheckIndex3 = np.nonzero((peaks_x > (xSubMax*4-0.01)) & (peaks_x < (xSubMax*4+0.01)))
    print ("Index 1: ",FtfCheckIndex1)
    print ("Index 2: ",FtfCheckIndex2)
    print ("Index 3: ",FtfCheckIndex3)

    FTFCheck_x = np.array([peaks_x[FtfCheckIndex1], peaks_x[FtfCheckIndex2],peaks_x[FtfCheckIndex3]])
    FTFCheck_y = np.array([peaks_y[FtfCheckIndex1], peaks_y[FtfCheckIndex2],peaks_y[FtfCheckIndex3]])

    print(FTFCheck_x)
    print (FTFCheck_y)

    if ((FTFCheck_x.size == 3)):
        if ((FTFCheck_y[0] < ySubMax) & (FTFCheck_y[1] < FTFCheck_y[0]) & (FTFCheck_y[2] < FTFCheck_y[1])):
           print ("sOUCI DE CAGE")

    #Suite [pas finito]

    if not ((yLow == 0).all()):
        yLowMax = max(yLow)
        yLowMaxIndex = yLow.argmax()
        xLowMax = xLow[yLowMaxIndex]
        print("Entre 1 et 2,5 ordres, pic maximum : (",xLowMax,",",yLowMax,")")

    if not ((yMid == 0).all()):
        yMidMax = max(yMid)
        yMidMaxIndex = yMid.argmax()
        xMidMax = xMid[yMidMaxIndex]
        print("Entre 2,5 et 4,5 ordres, pic maximum : (",xMidMax,",",yMidMax,")")

    if not ((yHigh == 0).all()):
        yHighMax = max(yHigh)
        yHighMaxIndex = yHigh.argmax()
        xHighMax = xHigh[yHighMaxIndex]
        print("Entre 4,5 et 20,5 ordres, pic maximum : (",xHighMax,",",yHighMax,")")

    if not ((yVeryHigh == 0).all()):
        yVeryHighMax = max(yVeryHigh)
        yVeryHighMaxIndex = yVeryHigh.argmax()
        xVeryHighMax = xVeryHigh[yVeryHighMaxIndex]
        print("Entre 20,5 et 1000 ordres, pic maximum : (",xVeryHighMax,",",yVeryHighMax,")")




    plt.figure()
    pplot(x,y, indexes)
    plt.title('Détection des pics')
    plt.xlabel('Ordre')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()


def txtReader (path):
    time_temp = []
    data_vibration = []
    f = open(path, 'r')
    for line in f:
         if (line.strip() != ""):
            if (line.strip().split()[0]=="Speed:"):
                speed = float(line.strip().split(' ')[1])
                speed_unit = line.strip().split(' ')[2]
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
    time = np.array(time_temp)
    if (speed_unit=="RPM"):
        RotationFreq = speed/60
    vibration = np.array(data_vibration)
    #print (time, vibration, RotationFreq)
    return (time, vibration, RotationFreq)



path_meas = r'C:\Users\Lenovo\Documents\Projet MA1\Fichiers BDD\Selected\FTF\EC27.62_ZONE6\CVP-20160919.txt'
(time, vibration, rotationFrequency) = txtReader(path_meas)
FFTG(time, vibration, rotationFrequency)
FFTV(time, vibration, rotationFrequency)
