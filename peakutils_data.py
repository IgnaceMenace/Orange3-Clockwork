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

    indexes = peakutils.indexes(ySpect, thres = 0.1, min_dist = 0)
    print (xSpect[indexes], ySpect[indexes])
    plt.figure()
    pplot(xSpect,ySpect, indexes)
    plt.title('Détection des pics')
    plt.xlabel('Ordre')
    plt.ylabel('Amplitude')
    plt.legend()
    plt.show()

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

    indexes = peakutils.indexes(y_spect, thres = 0, min_dist = 0)
    print (x_spect[indexes], y_spect[indexes])
    plt.figure()
    pplot(x_spect,y_spect, indexes)
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
    print (time, vibration, RotationFreq)
    return (time, vibration, RotationFreq)



path_meas = r'C:\Users\Lenovo\Documents\Projet MA1\Fichiers BDD\Selected\Belt\EC27.13_ZONE1\AVA-20151221.txt'
(time, vibration, rotationFrequency) = txtReader(path_meas)
FFTG(time, vibration, rotationFrequency)
FFTV(time, vibration, rotationFrequency)
