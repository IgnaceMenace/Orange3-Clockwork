import numpy
from scipy.fftpack import fft
from scipy import signal
import matplotlib.pyplot as plt

xArray = numpy.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100])
yArray = numpy.array([15, 25, 35, 45, 55, 65, 75, 85, 95, 105])

def FFTG(xInput, yInput):
    xLength = int(len(xInput)) #determine length of the array
    period = numpy.diff(xInput).mean() #determine period by the average of each element minus the one before
    
    start = 0.0
    stop = 1.0/(2.0*period)
    num = int(xLength/2)
    
    xSpect = numpy.linspace(start, stop, num, dtype = float)
    print("xSpect is : " , xSpect)

    #filtering = signal.boxcar(xLength)
    #ywf = fft(yInput*filtering)
    ywf = fft(yInput)
    ySpect = 2.0/xLength * numpy.abs(ywf[0:int(xLength/2)])
    print("ySpect is : " , ySpect)

    plt.plot(xSpect,ySpect)
    plt.show()

def FFTV(xInput,yInput):
    period = numpy.diff(xInput).mean() #determine period by the average of each element minus the one before
    xLength = int(len(xInput)) #determine length of the array
    start = 0.0
    stop = 1.0/(2.0*period)
    num = int(xLength/2)
    xSpect = numpy.linspace(start, stop, num, dtype=float)
    #filtering = signal.boxcar(xLength)
    #ywf = fft(yInput*filtering)
    ywf = fft(yInput)
    ySpect = int((9810 * (numpy.sqrt(2)/2))/int(xLength) *numpy.pi * numpy.abs(ywf[0:int(xLength)/2]))
    
    xSpect[0] = 0
    ySpect = numpy.divide(ySpect[1:],xSpect[1:])
    ySpect = numpy.concatenate(([0],ySpect))
    
    matplotlib.pyplot.plot(xSpect,ySpect)
    matplotlib.pyplot.show()

if __name__ == "__main__":
    
    time = numpy.arange(0,100,0.1)
    amplitude = 2*numpy.sin(time)
    amplitude1 = numpy.cos(2*time)
    #FFTG(xArray, yArray)
    #FFTG(time, amplitude)
    #FFTG(time, amplitude1)
    #print("time", time)
    FFTG(time, amplitude + amplitude1)
    FFTV(time, amplitude + amplitude1)
