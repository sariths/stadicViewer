# coding=utf-8
from __future__ import  print_function

from data.procData import VisData
from PyQt4 import QtCore,QtGui
from vis.gui import Ui_Form
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from base import NavigationToolbarStadic
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.dates import MonthLocator,DateFormatter,HourLocator
import warnings
import os,sys,operator
import datetime

from visuals.gridPlots import gridPlot
from visuals.heatMaps import heatMaps

hours = HourLocator()
months = MonthLocator()
# months = DayLocator(range(1,366),interval=30)
# TODO: This class should also inherit from a Json object class.
#TODO: I have a feeling that not all the data is getting plotted due to a glitch.
#check !
class TimeSeries(QtGui.QDialog, Ui_Form,VisData):

    def setupGui(self):

        #TODO: Turn this off later ;-)
        self.grpTimeSeriesMain.setVisible(True)


        self.tsFigure = Figure()
        self.tsCanvas = FigureCanvas(self.tsFigure)
        self.tsPlotsActivated = True

        self.tsToolbar = NavigationToolbar(self.tsCanvas,self)
        self.layoutTimeSeries.addWidget(self.tsToolbar)
        self.layoutTimeSeries.addWidget(self.tsCanvas)

        startDate = datetime.date(2015,1,1)
        self.tsDateList = [startDate+datetime.timedelta(x) for x in range(0,365)]


        self.sliderTimeSeriesOpacity.valueChanged.connect(self.tsOpacitySliderChanged)


        timeSeriesDataKeys,timeSeriesDataFiles = zip(*self.dataTimeSeriesLists)
        self.tsDataKeys = list(timeSeriesDataKeys)
        self.tsDataDict = dict(self.dataTimeSeriesLists)
        timeSeriesDataKeys = ['Select a chart']+sorted(list(timeSeriesDataKeys))


        self.cmbTimeSeriesPlotType.clear()
        self.cmbTimeSeriesPlotType.addItems(timeSeriesDataKeys)
        self.cmbTimeSeriesPlotType.currentIndexChanged.connect(self.tsPlotData)

        self.cmbTimeSeriesPlotType2.clear()
        self.cmbTimeSeriesPlotType2.addItems(timeSeriesDataKeys)
        self.cmbTimeSeriesPlotType2.currentIndexChanged.connect(self.tsPlotData)

        self.cmbTimeSeriesPlotType3.clear()
        self.cmbTimeSeriesPlotType3.addItems(timeSeriesDataKeys)
        self.cmbTimeSeriesPlotType3.currentIndexChanged.connect(self.tsPlotData)

        self.cmbTimeSeriesPlotType4.clear()
        self.cmbTimeSeriesPlotType4.addItems(timeSeriesDataKeys)
        self.cmbTimeSeriesPlotType4.currentIndexChanged.connect(self.tsPlotData)

        self.tsCmbTimeSeriesPlotList = [self.cmbTimeSeriesPlotType,
                                        self.cmbTimeSeriesPlotType2,
                                        self.cmbTimeSeriesPlotType3,
                                        self.cmbTimeSeriesPlotType4]



    def tsPlotData(self):
        dataSets = []

        for comboBox in self.tsCmbTimeSeriesPlotList:
            currentText = str(comboBox.currentText())
            if currentText in self.tsDataKeys:
                currentDataSet = self.tsDataDict[currentText]
                dataSets.append((currentText,currentDataSet))

        if dataSets:

            xCor = range(1,366)
            yCor = range(1,25)
            colorScheme = self.spCurrentColorScheme
            alphaVal = self.spCurrentSpaceChartOpacityValue

            heatMaps(dataSets, xCor, yCor,
                     figVal=self.tsFigure, colormap=colorScheme,
                     alpha=alphaVal,
                     colorMin=self.spIlluminanceMinVal,
                     interpolationVal='nearest',aspectValue='auto',xLabels=months,
                     xLabelFormatter=DateFormatter("%b"),yLabels=hours,orientationValue='vertical')

            self.tsCanvas.draw()


    def tsOpacitySliderChanged(self):
       self.txtTimeSeriesOpacityValue.setText(str(self.sliderTimeSeriesOpacity.value()))