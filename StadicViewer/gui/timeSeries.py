# coding=utf-8
from __future__ import  print_function
from __future__ import division

from data.procData import VisData
from PyQt4 import QtCore,QtGui
from vis.gui import Ui_Form
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# from base import NavigationToolbarStadic
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.dates import MonthLocator,DateFormatter,HourLocator,DayLocator
import warnings
import os,sys,operator
import datetime
import bisect


from visuals.gridPlots import gridPlot
from visuals.heatMaps import heatMaps

# hours = HourLocator()

# months = DayLocator(range(1,366),interval=30)
# TODO: This class should also inherit from a Json object class.
#TODO: I have a feeling that not all the data is getting plotted due to a glitch.
#check !


dates = None

class NavigationToolbarStadic(NavigationToolbar):
    dataDescr = None
    dataType = None

    def mouse_move(self, event):
        self._set_cursor(event)

        if event.inaxes and event.inaxes.get_navigate():

            try:
                s = event.inaxes.format_coord(event.xdata, event.ydata)
            except (ValueError, OverflowError):
                pass
            else:
                artists = [a for a in event.inaxes.mouseover_set
                           if a.contains(event)]

                if artists:

                    a = max(enumerate(artists), key=lambda x: x[1].zorder)[1]
                    if a is not event.inaxes.patch:
                        data = a.get_cursor_data(event)
                        if data is not None:

                            dateVal = bisect.bisect_left(self.tsDateIntervals,
                                                         event.xdata) - 1

                            hourVal = bisect.bisect_left(self.tsHourIntervals,
                                                         event.ydata) - 1

                            dataIndex = dateVal * 24 + hourVal

                            s = self.tsDateList[dateVal].strftime("%B-%d ")
                            s += self.tsHourList[hourVal] + "  Current Chart: %s --  All Charts:("%data

                            dataList = []

                            for dataset in self.dataSets:
                                dataList.append(dataset[dataIndex])
                            s += ",\t\t".join(map(str, dataList))

                            s += ")"

                if data < 0:
                    s = ''

                if len(self.mode):

                    self.set_message('%s, %s' % (self.mode, s))
                else:
                    self.set_message(s)
        else:
            self.set_message(self.mode)



class TimeSeries(QtGui.QDialog, Ui_Form,VisData):

    def setupGui(self):

        self.grpTimeSeriesMain.setVisible(True)

        self.tsFigure = Figure()
        self.tsCanvas = FigureCanvas(self.tsFigure)
        self.tsPlotsActivated = True

        self.tsToolbar = NavigationToolbarStadic(self.tsCanvas,self)

        self.tsToolbar.dataType = " "
        self.layoutTimeSeries.addWidget(self.tsToolbar)
        self.layoutTimeSeries.addWidget(self.tsCanvas)

        startDate = datetime.date(2015,1,1)
        self.tsToolbar.tsDateList = [startDate+datetime.timedelta(x) for x in range(0,365)]
        self.tsToolbar.tsDateIntervals = [1+364/365*idx for idx in range(366)]

        self.tsToolbar.tsHourList = ('00:30', '01:30', '02:30', '03:30', '04:30',
                    '05:30','06:30','07:30','08:30','09:30',
                    '10:30', '11:30', '12:30', '13:30', '14:30',
                    '15:30', '16:30', '17:30', '18:30', '19:30',
                    '20:30','21:30','22:30','23:30')
        self.tsToolbar.tsHourIntervals = [1+23/24*idx for idx in range(25)]


        self.sliderTimeSeriesOpacity.valueChanged.connect(self.tsOpacitySliderChanged)

        # Contstuctor Stuff
        self.tsColorMapTuple = (
        ('Uniform01', 'viridis'), ('Uniform02', 'inferno'),
        ('Uniform03', 'plasma'), ('Uniform04', 'magma'), ('Blues', 'Blues'),
        ('BlueGreen', 'BuGn'), ('BluePurple', 'BuPu'), ('GreenBlue', 'GnBu'),
        ('Greens', 'Greens'), ('Greys', 'Greys'), ('Oranges', 'Oranges'),
        ('OrangeRed', 'OrRd'), ('PurpleBlue', 'PuBu'),
        ('PurpleBlueGreen', 'PuBuGn'), ('PurpleRed', 'PuRd'),
        ('Purples', 'Purples'),
        ('RedPurple', 'RdPu'), ('Reds', 'Reds'), ('YellowGreen', 'YlGn'),
        ('YellowGreenBlue', 'YlGnBu'), ('YellowOrangeBrown', 'YlOrBr'),
        ('YellowOrangeRed', 'YlOrRd'), ('Hot01', 'afmhot'), ('Hot02', 'hot'),
        ('Hot03', 'gist_heat'), ('Autumn', 'autumn'), ('Bone', 'bone'),
        ('Cool', 'cool'),
        ('Copper', 'copper'), ('Spring', 'spring'), ('Summer', 'summer'),
        ('Winter', 'winter'))

        colorNames = [name for name, plotName in self.tsColorMapTuple]
        self.tsColorDict = dict(self.tsColorMapTuple)
        self.cmbTimeSeriesColorScheme.addItems(colorNames)
        self.cmbTimeSeriesColorScheme.setCurrentIndex(21)
        self.btnTimeSeriesSetColorScheme.clicked.connect(self.tsAssignSpaceColorScheme)

        self.tsCurrentColorScheme = 'YlOrRd'
        self.tsCurrentSpaceChartOpacityValue = 1


        timeSeriesDataKeys,timeSeriesDataFiles = zip(*self.dataTimeSeriesLists)
        self.tsDataKeys = list(timeSeriesDataKeys)
        self.tsDataDict = dict(self.dataTimeSeriesLists)
        timeSeriesDataKeys = ['Select a chart']+sorted(list(timeSeriesDataKeys))

        minMaxBoxes = [self.txtTimeSeriesChart1Max,self.txtTimeSeriesChart2Max,
                       self.txtTimeSeriesChart3Max,self.txtTimeSeriesChart4Max,
                       self.txtTimeSeriesChart1Min,self.txtTimeSeriesChart2Min,
                       self.txtTimeSeriesChart3Min,self.txtTimeSeriesChart4Min]

        # Validator for setting values
        floatValidator = QtGui.QDoubleValidator(0.0, 20000.0, 3)

        for txtBox in minMaxBoxes:
            txtBox.setValidator(floatValidator)

        self.cmbTimeSeriesPlotType.clear()
        self.cmbTimeSeriesPlotType.addItems(timeSeriesDataKeys)
        self.cmbTimeSeriesPlotType.currentIndexChanged.connect(lambda:self.tsChartTypeChanged(0))
        self.btnTimeSeriesChart1.clicked.connect(lambda:self.tsChartTypeConfirmed(0))
        self.txtTimeSeriesChart1Max.textChanged.connect(lambda:self.tsMinMaxValChanged(0))
        self.txtTimeSeriesChart1Min.textChanged.connect(
            lambda: self.tsMinMaxValChanged(0))

        self.cmbTimeSeriesPlotType2.clear()
        self.cmbTimeSeriesPlotType2.addItems(timeSeriesDataKeys)
        self.cmbTimeSeriesPlotType2.currentIndexChanged.connect(lambda:self.tsChartTypeChanged(1))
        self.btnTimeSeriesChart2.clicked.connect(lambda:self.tsChartTypeConfirmed(1))
        self.txtTimeSeriesChart2Max.textChanged.connect(
            lambda: self.tsMinMaxValChanged(1))
        self.txtTimeSeriesChart2Min.textChanged.connect(
            lambda: self.tsMinMaxValChanged(1))

        self.cmbTimeSeriesPlotType3.clear()
        self.cmbTimeSeriesPlotType3.addItems(timeSeriesDataKeys)
        self.cmbTimeSeriesPlotType3.currentIndexChanged.connect(lambda:self.tsChartTypeChanged(2))
        self.btnTimeSeriesChart3.clicked.connect(lambda:self.tsChartTypeConfirmed(2))
        self.txtTimeSeriesChart3Max.textChanged.connect(
            lambda: self.tsMinMaxValChanged(2))
        self.txtTimeSeriesChart3Min.textChanged.connect(
            lambda: self.tsMinMaxValChanged(2))

        self.cmbTimeSeriesPlotType4.clear()
        self.cmbTimeSeriesPlotType4.addItems(timeSeriesDataKeys)
        self.cmbTimeSeriesPlotType4.currentIndexChanged.connect(lambda:self.tsChartTypeChanged(3))
        self.btnTimeSeriesChart4.clicked.connect(lambda:self.tsChartTypeConfirmed(3))
        self.txtTimeSeriesChart4Max.textChanged.connect(
            lambda: self.tsMinMaxValChanged(3))
        self.txtTimeSeriesChart4Min.textChanged.connect(
            lambda: self.tsMinMaxValChanged(3))
        self.tsCmbTimeSeriesPlotList = [self.cmbTimeSeriesPlotType,
                                        self.cmbTimeSeriesPlotType2,
                                        self.cmbTimeSeriesPlotType3,
                                        self.cmbTimeSeriesPlotType4]

        self.tsTxtMaxList = [self.txtTimeSeriesChart1Max,
                             self.txtTimeSeriesChart2Max,
                             self.txtTimeSeriesChart3Max,
                             self.txtTimeSeriesChart4Max]

        self.tsTxtMinList = [self.txtTimeSeriesChart1Min,
                             self.txtTimeSeriesChart2Min,
                             self.txtTimeSeriesChart3Min,
                             self.txtTimeSeriesChart4Min]

        self.tsBtnChartList = [self.btnTimeSeriesChart1,
                               self.btnTimeSeriesChart2,
                               self.btnTimeSeriesChart3,
                               self.btnTimeSeriesChart4]

        self.tsLabelList = [self.lblTimeSeriesChart1Max,
                               self.lblTimeSeriesChart2Max,
                               self.lblTimeSeriesChart3Max,
                               self.lblTimeSeriesChart4Max,
                            self.lblTimeSeriesChart1Min,
                            self.lblTimeSeriesChart2Min,
                            self.lblTimeSeriesChart3Min,
                            self.lblTimeSeriesChart4Min]

        for obj in self.tsTxtMaxList+self.tsTxtMinList+self.tsBtnChartList:
            obj.setEnabled(False)

        # TODO: Disable the setvisible and enable the setEnabled.
        # for obj in self.tsTxtMaxList+self.tsTxtMinList+self.tsLabelList:
        #     obj.setVisible(False)



        self.tsChart1MaxVal,self.tsChart2MaxVal,self.tsChart3MaxVal,self.tsChart4MaxVal=None,None,None,None
        self.tsChart1MinVal, self.tsChart2MinVal, self.tsChart3MinVal, self.tsChart4MinVal = None, None, None, None

        self.tsMaxValList = [self.tsChart1MaxVal,self.tsChart2MaxVal,self.tsChart3MaxVal,self.tsChart4MaxVal]
        self.tsMinValList = [self.tsChart1MinVal, self.tsChart2MinVal, self.tsChart3MinVal, self.tsChart4MinVal]
        self.tsChartEnabledList = [False,False,False,False]


        self.tsXaxisFormat = MonthLocator()
    def tsMinMaxValChanged(self,chartIndex):
        self.tsBtnChartList[chartIndex].setText("Click to confirm")


    def tsAssignSpaceColorScheme(self):
        currentColor = self.tsColorDict[str(self.cmbTimeSeriesColorScheme.currentText())]

        if self.chkTimeSeriesColorSchemeInvert.checkState():
            currentColor += "_r"

        self.tsCurrentColorScheme = currentColor
        self.tsCurrentSpaceChartOpacityValue = self.sliderTimeSeriesOpacity.value()/100.0

        self.tsPlotData()

    def tsChartTypeChanged(self,chartIndex):
        currentDataSetName = str(self.tsCmbTimeSeriesPlotList[chartIndex].currentText())
        currentMaxText = self.tsTxtMaxList[chartIndex]
        currentMinText = self.tsTxtMinList[chartIndex]
        currentBtn = self.tsBtnChartList[chartIndex]
        self.tsChartEnabledList[chartIndex] = False
        self.tsBtnChartList[chartIndex].setText("Click to confirm")

        if currentDataSetName in self.tsDataKeys:
            currentMaxText.setEnabled(True)
            currentMinText.setEnabled(True)
            currentBtn.setEnabled(True)

            currentDataSet = self.tsDataDict[currentDataSetName]
            currentDataSetMax = max(currentDataSet)
            currentDataSetMin = min(currentDataSet)

            currentMaxText.setText(str(currentDataSetMax))
            currentMinText.setText(str(currentDataSetMin))


        else:
            currentMaxText.clear()
            currentMinText.clear()
            currentMaxText.setEnabled(False)
            currentMinText.setEnabled(False)
            # currentBtn.setEnabled(False)
            self.tsBtnChartList[chartIndex].setText("Confirm")


    def tsChartTypeConfirmed(self,chartIndex):
        currentDataSetName = str(self.tsCmbTimeSeriesPlotList[chartIndex].currentText())

        if currentDataSetName in self.tsDataKeys:
            currentMaxText = self.tsTxtMaxList[chartIndex]
            currentMinText = self.tsTxtMinList[chartIndex]
            self.tsMaxValList[chartIndex] = float(currentMaxText.text())
            self.tsMinValList[chartIndex] = float(currentMinText.text())
            self.tsChartEnabledList[chartIndex] = True
        else:
            self.tsChartEnabledList[chartIndex] = False
            self.tsMaxValList[chartIndex] = None
            self.tsMinValList[chartIndex] = None

        self.tsBtnChartList[chartIndex].setText("Confirmed")
        self.tsPlotData()

    def tsPlotData(self):
        dataSets = []
        maxValList = []
        minValList = []
        self.tsToolbar.dataSets = []
        for idx,comboBox in enumerate(self.tsCmbTimeSeriesPlotList):
            currentText = str(comboBox.currentText())
            currentMax = self.tsMaxValList[idx]
            currentMin = self.tsMinValList[idx]
            isChartEnabled = self.tsChartEnabledList[idx]

            if currentText in self.tsDataKeys and isChartEnabled:
                currentDataSet = self.tsDataDict[currentText]
                dataSets.append((currentText,currentDataSet))
                self.tsToolbar.dataSets.append(currentDataSet)
                maxValList.append(currentMax)
                minValList.append(currentMin)

        if dataSets:

            xCor = range(1,366)
            yCor = range(1,25)
            colorScheme = self.tsCurrentColorScheme
            alphaVal = self.tsCurrentSpaceChartOpacityValue

            heatMaps(dataSets, xCor, yCor,
                     figVal=self.tsFigure, colormap=colorScheme,
                     alpha=alphaVal,
                     colorMin=minValList,colorMax=maxValList,
                     interpolationVal='nearest',aspectValue='auto',xLabels=self.tsXaxisFormat,
                     xLabelFormatter=DateFormatter("%b"),yLabels=None,orientationValue='vertical')

            self.tsCanvas.draw()


    def tsOpacitySliderChanged(self):
       self.txtTimeSeriesOpacityValue.setText(str(self.sliderTimeSeriesOpacity.value()))