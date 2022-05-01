import numpy
from scipy.fftpack import fft
from scipy.signal import find_peaks
from scipy import signal
import matplotlib.pyplot as plt

def FFTG(xInput, yInput):
    """
    This function calculate the Frequential Fourier Transform in Acceleration

    Parameters
    ----------
    xInput : array
        Array of a certain size that represent the temporal window
    yInput : array
        Array filled with the temporal response associated with every values of the xInput

    Returns
    -------
    xSpectral : array
        Array filled with the frequential window
    ySpectral : array
        Array filled with the amplitude associated with each frequency 
    """

    xLength = int(len(xInput)) #determine length of the array
    period = numpy.diff(xInput).mean() #determine period by the average of each element minus the one before
    
    start = 0.0
    stop = 1.0/(2.0*period)
    num = int(xLength/2)
    
    xSpectral = numpy.linspace(start, stop, num, dtype = float)
    print("xSpectral is : " , xSpectral)

    #filtering = signal.boxcar(xLength)
    #ywf = fft(yInput*filtering)
    ywf = fft(yInput)
    ySpectral = 2.0/xLength * numpy.abs(ywf[0:int(xLength/2)])
    print("ySpectral is : " , ySpectral)


    #matplotlib.pyplot.plot(xSpectral,ySpectral)
    #matplotlib.pyplot.show()

    return [xSpectral , ySpectral]

def FFTV(xInput,yInput):
    """
    This function calculate the Frequential Fourier Transform in Velocity 

    Parameters
    ----------
    xInput : array
        Array of a certain size that represent the temporal window
    yInput : array
        Array filled with the temporal response associated with every values of the xInput

    Returns
    -------
    xSpectral : array
        Array filled with the frequential window
    ySpectral : array
        Array filled with the amplitude associated with each frequency 
    """
    xLength = int(len(xInput))
    period = numpy.diff(xInput).mean()
    
    start = 0.0
    stop = 1.0/(2.0*period)
    num = int(xLength/2)

    xSpectral = numpy.linspace(0.0, 1.0/(2.0*period), num, dtype=float)
    ywm = fft(yInput)
    ySpectral = (9810 * (numpy.sqrt(2)/2))/(2*num*numpy.pi) * numpy.abs(ywm[0:num])
    
    xSpectral[0] = 0
    ySpectral = numpy.divide(ySpectral[1:],xSpectral[1:])
    ySpectral = numpy.concatenate(([0],ySpectral))

    #matplotlib.pyplot.plot(xSpectral,ySpectral)
    #matplotlib.pyplot.show()
    return [xSpectral , ySpectral]

if __name__ == "__main__":
    time = numpy.arange(0,100,0.1)
    amplitude = 2*numpy.sin(time)
    amplitude1 = numpy.cos(2*time)

    [xSpectralFFTG,ySpectralFFTG] = FFTG(time, amplitude + amplitude1)
    [xSpectralFFTV,ySpectralFFTV] = FFTV(time, amplitude + amplitude1)

    # Initialise the subplot function using number of rows and columns
    figure, axis = plt.subplots(1,2)
    axis[0].plot(xSpectralFFTG,ySpectralFFTG)
    axis[0].set_title("FFTG")
    axis[0].set_xlabel ('Fréquences (Hz)')
    axis[0].set_ylabel ('Amplitude')
    axis[1].plot(xSpectralFFTV,ySpectralFFTV)
    axis[1].set_title("FFTV")
    axis[1].set_xlabel ('Fréquences (Hz)')
    axis[1].set_ylabel ('Amplitude')

    ## find peaks

    peaksFFTG = find_peaks(ySpectralFFTG, height = 0, threshold = 0.75)
    peaksFFTV = find_peaks(ySpectralFFTV, height = 1000, threshold = 1, distance = 1)
    heightFFTG = peaksFFTG[1]['peak_heights']
    heightFFTV = peaksFFTV[1]['peak_heights']
    peaksPosFFTG = xSpectralFFTG[peaksFFTG[0]]
    peaksPosFFTV = xSpectralFFTV[peaksFFTV[0]]
    axis[0].scatter(peaksPosFFTG, heightFFTG, color = 'r', s = 15, marker = 'D', label = 'Peaks'    )
    axis[0].legend()
    axis[1].scatter(peaksPosFFTV, heightFFTV, color = 'r', s = 15, marker = 'D', label = 'Peaks'    )
    axis[1].legend()

    plt.show()
