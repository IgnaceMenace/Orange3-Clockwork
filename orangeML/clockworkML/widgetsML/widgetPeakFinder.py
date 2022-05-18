from Orange.widgets.widget import OWWidget
from Orange.widgets.utils.signals import Input, Output
from Orange.widgets import settings, widget, gui
from Orange.data import Table
from Orange.widgets.widget import Msg
import numpy as np
import peakutils
from sklearn.ensemble import IsolationForest
from peakutils.plot import plot
from matplotlib import pyplot
import matplotlib.pyplot as plt

class dataProcessing:
    def peakFinder(self,X,Y):
        base = peakutils.baseline(Y, 2)
        Y_nobase = Y-base
        Y=Y_nobase
        indexes = peakutils.indexes(Y, thres = 0.1, min_dist = 0, thres_abs=True)
        peaks_x = []
        peaks_y =[]
        for value in indexes:
            peaks_x.append(X[value])
            peaks_y.append(Y[value])
        peaks_x = np.array(peaks_x)
        peaks_y = np.array(peaks_y)  
        
        iForest = IsolationForest(n_estimators=40, verbose=3)
        peaks = np.column_stack((peaks_x,peaks_y))
        iForest.fit(peaks)
        pred = iForest.predict(peaks)
        plt.plot(X, Y)
        plt.scatter(peaks[:,0], peaks[:,1], c=pred, cmap='RdBu')


        pred_scores = -1*iForest.score_samples(peaks)
        plt.scatter(peaks[:, 0], peaks[:, 1], c=pred_scores, cmap='coolwarm')
        plt.colorbar(label='Anomaly Score')
        plt.show()

class widgetPeakFinder(OWWidget):
    name = "Peak Finder Widget"
    icon = "icons/widget1.svg"
    description = "This Widget finds the peak in a 2 dimension array"    
    class Inputs:
        inputWidget = Input("input", Table)
    class Outputs:
        outputWidget = Output("output", Table)
    class error(widget.OWWidget.Error):
        defaultError = Msg("Error while treating data")
    def __init__(self):
        super().__init__()

    @Inputs.inputWidget
    def set_data(self,dataset):
        if dataset is not None:
            formattedData = np.array(dataset)
            dp = dataProcessing()
            dp.peakFinder(formattedData[:,0], formattedData[:,1])
            self.Outputs.outputWidget.send(dataset)

        else:
            print("No data supplied !")

if __name__ == "__main__":
    print("Unit test")
