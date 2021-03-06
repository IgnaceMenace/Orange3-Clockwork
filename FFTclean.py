import numpy as np
import matplotlib.pyplot as plt
from scipy.fftpack import fft
from scipy import signal
from scipy.signal import find_peaks


def FFTG(xInput, yInput):
    xLength = int(len(xInput)) #determine length of the array
    period = np.diff(xInput).mean() #determine period by the average of each element minus the one before
    
    start = 0.0  # 1st x value
    stop = 1.0/(2.0*period)  #last x value
    num = int(xLength/2)
    ywm = fft(yInput)
    
    xSpect = np.linspace(start, stop, num, dtype = float)
    ySpect = 2.0/xLength * np.abs(ywm[0:int(xLength/2)])

    plt.figure() 
    plt.plot(xSpect,ySpect)
    plt.title('FFTG')
    plt.xlabel('Fréquences (Hz)')
    plt.ylabel('Amplitude')
    plt.show()
    peaksFFTG = find_peaks(ySpect, height = 0, threshold = 0.75)
    heightFFTG = peaksFFTG[1]['peak_heights']
    peaksPosFFTG = xSpect[peaksFFTG[0]]
    plt.scatter(peaksPosFFTG, heightFFTG, color = 'r', s = 15, marker = 'D', label = 'Peaks'    )
    plt.legend()


def FFTV(xInput,yInput):
    xLength = int(len(xInput))
    Period = np.diff(xInput).mean()
    
    start = 0.0
    stop = 1.0/(2.0*Period)
    num = int(xLength/2)

    x_spect = np.linspace(0.0, 1.0/(2.0*Period), num, dtype=float)
    ywm = fft(yInput)
    y_spect = (9810 * (np.sqrt(2)/2))/(2*num*np.pi) * np.abs(ywm[0:num])
    
    x_spect[0] = 0
    y_spect = np.divide(y_spect[1:],x_spect[1:])
    y_spect = np.concatenate(([0],y_spect))
    
    

    return [x_spect, y_spect]
   


# Données du sinus
time = np.arange(0,100,0.1)
amplitude = 2*np.sin(time)
amplitude1 = np.cos(2*time)

# Graphe sinus
plt.plot(time,amplitude)
plt.show()
plt.title('Vibration')
plt.xlabel('Temps')
plt.ylabel('Amplitude')

# FFTG
FFTG(time, amplitude)
FFTG(time, amplitude1)
FFTG(time, amplitude + amplitude1)

#FFTV

[x_FFTV, y_FFTV] = FFTV(time,amplitude)

plt.plot(x_FFTV,y_FFTV)
plt.show()
plt.title('FFTV')
plt.xlabel ('Fréquences (Hz)')
plt.ylabel ('Amplitude')

[x_FFTV, y_FFTV] = FFTV(time,amplitude1)

plt.plot(x_FFTV,y_FFTV)
plt.show()
peaksFFTV = find_peaks(y_FFTV, height = 0, threshold = 1, distance = 1)
heightFFTV = peaksFFTV[1]['peak_heights']
peaksPosFFTV = x_FFTV[peaksFFTV[0]]
plt.scatter(peaksPosFFTV, heightFFTV, color = 'r', s = 15, marker = 'D', label = 'Peaks'    )
plt.legend()

[x_FFTV, y_FFTV] = FFTV(time, amplitude + amplitude1)

plt.plot(x_FFTV,y_FFTV)
peaksFFTV = find_peaks(y_FFTV, height = 0, threshold = 1, distance = 1)
heightFFTV = peaksFFTV[1]['peak_heights']
peaksPosFFTV = x_FFTV[peaksFFTV[0]]
plt.scatter(peaksPosFFTV, heightFFTV, color = 'r', s = 15, marker = 'D', label = 'Peaks')
plt.show()
plt.legend()
