import numpy
from scipy.fftpack import fft
from scipy import signal
import matplotlib.pyplot

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

    matplotlib.pyplot.plot(xSpect,ySpect)
    matplotlib.pyplot.show()

#FFTG(xArray, yArray)

time = numpy.arange(0,100,0.1)
amplitude = 2*numpy.sin(time)

amplitude1 = numpy.cos(2*time)
FFTG(time, amplitude)
FFTG(time, amplitude1)
print("time", time)
FFTG(time, amplitude + amplitude1)

def FFTV(xInput,yInput):
    print("FFTV")

#rajouter le if name = main
