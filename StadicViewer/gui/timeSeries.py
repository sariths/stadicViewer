# coding=utf-8
from __future__ import  print_function

from StadicViewer.data.procData import VisData
from PyQt4 import QtCore,QtGui
from StadicViewer.vis.gui import Ui_Form
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import warnings
import os,sys,operator


from visuals.heatMaps import thermalPlots

# TODO: This class should also inherit from a Json object class.
class TimeSeries(QtGui.QDialog, Ui_Form,VisData):

    def setupGui(self):

        #Turn this off later ;-)
        self.grpTimeSeriesMain.setVisible(True)


        self.tsFigure = Figure()
        self.tsCanvas = FigureCanvas(self.tsFigure)
        self.tsPlotsActivated = False

        self.tsToolbar = NavigationToolbar(self.tsCanvas,self)
        self.layoutTimeSeries.addWidget(self.tsToolbar)
        self.layoutTimeSeries.addWidget(self.tsCanvas)

        self.sliderTimeSeriesOpacity.valueChanged.connect(self.tsOpacitySliderChanged)

        self.txtTimeSeriesMsgBox.setText(self.dataLog)

        timeSeriesDataKeys,timeSeriesDataFiles = zip(*self.dataTimeSeriesLists)
        self.tsDataDict = dict(self.dataTimeSeriesLists)

        self.cmbTimeSeriesPlotType.clear()
        self.cmbTimeSeriesPlotType.addItems(sorted(timeSeriesDataKeys))
        self.cmbTimeSeriesPlotType.currentIndexChanged.connect(self.tsPlotData)


    def tsPlotData(self):
        currentDataSet = str(self.cmbTimeSeriesPlotType.currentText())
        print(self.tsDataDict[currentDataSet])

    def tsOpacitySliderChanged(self):
       self.txtTimeSeriesOpacityValue.setText(str(self.sliderTimeSeriesOpacity.value()))