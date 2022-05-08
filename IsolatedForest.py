import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from scipy.fftpack import fft
import matplotlib.pyplot as plt
import peakutils 


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
    Model_PeakDetect(xSpect,ySpect)


def Model_PeakDetect(X,Y):
    base = peakutils.baseline(Y, 2)
    Y_nobase = Y-base
    indexes = peakutils.peak.indexes(Y_nobase, thres = 0.03, min_dist = 0, thres_abs=True)
    peaks_x = []
    peaks_y =[]
    for value in indexes:
        peaks_x.append(Y_nobase[value])
        peaks_y.append(Y_nobase[value])
    peaks_x = np.array(peaks_x)
    peaks_y = np.array(peaks_y)  
    #peaks_x = peakutils.interpolate(X,Y_nobase,ind=indexes)
    iForest = IsolationForest(n_estimators=20, verbose=2)
    peaks = np.column_stack((peaks_x,peaks_y))
    iForest.fit(peaks)
    pred = iForest.predict(peaks)
    plt.plot(X, Y_nobase)
    plt.scatter(peaks[:,0], peaks[:,1], c=pred, cmap='RdBu')


    pred_scores = -1*iForest.score_samples(peaks)
    plt.scatter(peaks[:, 0], peaks[:, 1], c=pred_scores, cmap='coolwarm')
    plt.colorbar(label='Anomaly Score')
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


path_meas = r'C:\Users\Lenovo\Documents\Projet MA1\Fichiers BDD\Selected\BPFI\GE27.24A_LOGISTIQUE\CVA-20160919.txt'
(time, vibration, rotationFrequency) = txtReader(path_meas)
FFTG(time, vibration, rotationFrequency)




