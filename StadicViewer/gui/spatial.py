"""This module enables the GUI, buttons and control logic for Room-based plots."""

# coding=utf-8
from __future__ import  print_function

import bisect
import numbers
import sys

import numpy as np
from PyQt4 import QtCore,QtGui
from dataStructures.timeSeries import TimeArray
from readStadicData.processVisData import VisData
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from dataStructures.dayIll import Dayill
from readStadicData.parseJson import StadicProject
from pyqtGui.gui import Ui_Form

from plotFunctions.gridPlots import gridPlot

#~~~~~DevNotes: 25Mar2016:~~~~~~~
# Fixed display limits to conform to illuminance units.
# Moved all the connect signals to the end so that they don't get triggered..
# in the beginning the readStadicData is being loaded into all the comboBoxes and textBoxes

# TODO: Add a Qmessagebox to show an error message in case the grid..
# TODO:..spacings aren't uniform.
# TODO: Fix the calendar year. (Almost done) !
# TODO: Mask missing points.


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

                        if isinstance(data,numbers.Number):
                            if self.dataDescr:
                                s += " {} ".format(self.dataDescr)


                            if self.dataType:
                                if self.dataType == 'lux':
                                    dataVal = int(data)
                                elif self.dataType == 'fc':
                                    dataVal = round(data,3)
                                else:
                                    dataVal = round(data*100,3)
                            s += '{}'.format(dataVal)

                            if self.dataType != "%":
                                s += ' {}'.format(self.dataType)
                            else:
                                s += '{}'.format(self.dataType)
                        else:
                            s = ''

                if data is np.NaN or data < 0 :
                    s = ''

                if len(self.mode):

                        self.set_message('%s, %s' % (self.mode, s))
                else:
                    self.set_message(s)
        else:
            self.set_message(self.mode)

    def pick_event(self,event):
        print(event.ind)

class Spatial(QtGui.QDialog, Ui_Form,VisData):

    def setupGui(self):
            if self.dataSpaceNameSelected:
                self.tabWidget.setEnabled(True)

                #Set the calendar as per the starting year.
                self.calSpaceDateTimeIllum.setMinimumDateTime(
                    QtCore.QDateTime(self.dataYear,1,1,0,0))
                self.calSpaceDateTimeIllum.setDateTime(
                    QtCore.QDateTime(self.dataYear, 1, 1, 0, 0))
                self.calSpaceDateTimeIllum.setMaximumDateTime(
                    QtCore.QDateTime(self.dataYear,12,31,23,59))




                self.grpContoursIlluminance.setEnabled(True)

                self.btnSpaceSettingsContour.setEnabled(True)
                #TODO: Change the visiblity settings to True later ;)
                self.btnSpaceSettingsContour.setVisible(True)

                #Setup matplotlib inside Qt.
                self.spFigure = Figure()
                self.spCanvas = FigureCanvas(self.spFigure)



                #Validator for setting values
                floatValidator = QtGui.QDoubleValidator(0.0,20000.0,3)

                #Settings for showing and hiding color and contours.
                self.grpColoursIlluminance.setVisible(False)
                self.grpContoursIlluminance.setVisible(False)


                #Initiate a dictioanry for ill files.
                self.spAllFilesDict = {}

                #Code for manipulating navigation settings for illuminance.
                #Code for manipulating navigation settings for illuminance.

                self.spTimeStepIlluminance = 1 #This attribute determines the time step for stepping between different illuminance plots.

                #Changing/clicking any of the below controls should trigger the illuminance plots.


                self.spIlluminanceActivated = False
                self.spCurrentIlluminanceHour = 9


                units = self.dataProject.unitsIlluminance
                unitsMultiplier = {'lux':1,'fc':0.1}[str(units)]


                self.spIlluminanceMaxVal = 5000*unitsMultiplier
                self.spIlluminanceMinVal = 0

                self.spIlluminanceMaxValDefault = 5000*unitsMultiplier
                self.spIlluminanceMinValDefault = 0
                self.spIlluminanceUpperMaskValue = None
                self.spIlluminanceLowerMaskValue = None
                self.spIlluminanceUpperMaskColor = None
                self.spIlluminanceLowerMaskColor = None

                self.spElectricMaxVal = 400 * unitsMultiplier
                self.spElectricMinVal = 0

                self.spElectricMaxValDefault = 400 * unitsMultiplier
                self.spElectricMinValDefault = 0
                self.spElectricUpperMaskValue = None
                self.spElectricLowerMaskValue = None
                self.spElectricUpperMaskColor = None
                self.spElectricLowerMaskColor = None

                self.spMetricsMaxVal = 1.0
                self.spMetricsMinVal = 0.0
                self.spMetricsMaxValDefault = 1.0
                self.spMetricsMinValDefault = 0
                self.spMetricsUpperMaskValue = None
                self.spMetricsLowerMaskValue = None
                self.spMetricsUpperMaskColor = None
                self.spMetricsLowerMaskColor = None


                self.spCurrentPlotIsIlluminance = True
                self.spCurrentPlotIsElectric = False


                self.txtSpaceColorsMax.setText(str(self.spIlluminanceMaxValDefault))
                self.txtSpaceColorsMin.setText(str(self.spIlluminanceMinValDefault))
                self.txtSpaceColorsMax.setValidator(floatValidator)
                self.txtSpaceColorsMin.setValidator(floatValidator)


                self.spPlotIlluminanceColors = True



                #Put all contourboxes inside a list for easy iteration.
                self.spContourBoxes = [self.txtSpaceCountourValue1, self.txtSpaceCountourValue2, self.txtSpaceCountourValue3, self.txtSpaceCountourValue4,
                                       self.txtSpaceCountourValue5, self.txtSpaceCountourValue6, self.txtSpaceCountourValue7, self.txtSpaceCountourValue8]

                for contourBox in self.spContourBoxes:
                    contourBox.setValidator(floatValidator)






                self.spContourValuesIlluminance = (50, 100, 500, 1000, 2000, 3000, 5000, 10000)
                self.spContourValuesIlluminance = map(lambda x:x*unitsMultiplier,self.spContourValuesIlluminance)

                self.spContourValuesElectric = (50, 100, 150, 200, 250, 300, 350, 400)
                self.spContourValuesElectric = map(lambda x:x*unitsMultiplier,self.spContourValuesElectric)


                self.spContourValuesIlluminanceDefault = (50, 100, 500, 1000, 2000, 3000, 5000, 10000)
                self.spContourValuesIlluminanceDefault = map(lambda x:x*unitsMultiplier,self.spContourValuesIlluminanceDefault)

                self.spContourValuesElectricDefault = (50, 100, 150, 200, 250, 300, 350, 400)
                self.spContourValuesElectricDefault = map(lambda x:x*unitsMultiplier,self.spContourValuesElectricDefault)

                for idx,contourBox in enumerate(self.spContourBoxes):
                    contourBox.setText(str(self.spContourValuesIlluminance[idx]))

                self.spContourValuesMetrics = (0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.0)
                self.spContourValuesMetricsDefault = (0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.0)



                #Contstuctor Stuff
                self.spColorMapTuple = (('Uniform01', 'viridis'), ('Uniform02', 'inferno'), ('Uniform03', 'plasma'), ('Uniform04', 'magma'), ('Blues', 'Blues'),
                                        ('BlueGreen','BuGn'), ('BluePurple','BuPu'), ('GreenBlue','GnBu'), ('Greens','Greens'), ('Greys','Greys'), ('Oranges','Oranges'),
                                        ('OrangeRed','OrRd'), ('PurpleBlue','PuBu'), ('PurpleBlueGreen','PuBuGn'), ('PurpleRed','PuRd'), ('Purples','Purples'),
                                        ('RedPurple','RdPu'), ('Reds','Reds'), ('YellowGreen','YlGn'), ('YellowGreenBlue','YlGnBu'), ('YellowOrangeBrown','YlOrBr'),
                                        ('YellowOrangeRed','YlOrRd'), ('Hot01','afmhot'), ('Hot02','hot'), ('Hot03','gist_heat'), ('Autumn','autumn'), ('Bone','bone'), ('Cool','cool'),
                                        ('Copper','copper'), ('Spring','spring'), ('Summer','summer'), ('Winter','winter'))

                colorNames = [name for name,plotName in self.spColorMapTuple]
                self.spColorDict =dict(self.spColorMapTuple)
                self.cmbSpaceColorScheme.addItems(colorNames)
                self.cmbSpaceColorScheme.setCurrentIndex(21)

                self.spCurrentColorScheme = 'YlOrRd'
                self.spCurrentSpaceChartOpacityValue = 1

                self.spCurrentColorSchemeMetrics = 'YlOrRd'
                self.spCurrentSpaceChartOpacityValueMetrics = 1

                self.spCurrentColorSchemeElectric = 'YlOrRd'
                self.spCurrentSpaceChartOpacityValueElectric = 1

                self.spInterpolateColorScheme= None

                self.txtSpaceStatusDisplay.setEnabled(False)

                illFileKeys,illFileNames = zip(*self.dataDayIllFilesList)

                self.ptsFile = self.dataPtsFile

                self.illData = Dayill(illFileNames[0],self.ptsFile)


                hourFormat = self.illData.timedata[0:24]
                hourFormat = [hourVal['tstamp'].strftime("%I:%M %p") for hourVal in hourFormat]

                #Set valid time stamps for all the drop boxes that show time.
                self.cmbSpaceTimeIllum.clear()
                self.cmbSpaceTimeIllum.addItems(map(str,hourFormat))
                self.cmbSpaceTimeIllum.setCurrentIndex(9)

                self.cmbSpaceTimeIntervalMax.clear()
                self.cmbSpaceTimeIntervalMax.addItems(map(str,hourFormat))
                self.cmbSpaceTimeIntervalMax.setCurrentIndex(23)

                self.cmbSpaceTimeIntervalMin.clear()
                self.cmbSpaceTimeIntervalMin.addItems(map(str,hourFormat))
                self.cmbSpaceTimeIntervalMin.setCurrentIndex(0)

                # Set valid time stamps for all the drop boxes that show time.
                self.cmbCombinedTimeIllum.clear()
                self.cmbCombinedTimeIllum.addItems(map(str, hourFormat))
                self.cmbCombinedTimeIllum.setCurrentIndex(9)

                self.cmbCombinedTimeIntervalMax.clear()
                self.cmbCombinedTimeIntervalMax.addItems(map(str, hourFormat))
                self.cmbCombinedTimeIntervalMax.setCurrentIndex(23)

                self.cmbCombinedTimeIntervalMin.clear()
                self.cmbCombinedTimeIntervalMin.addItems(map(str, hourFormat))
                self.cmbCombinedTimeIntervalMin.setCurrentIndex(0)

                self.spAllFilesDict = self.dataAllFiles

                # Addedd this test as sometimes metrics are not calculated. In those cases it's just the illuminance readStadicData.
                try:
                    resultsFiles,resultsFilesNames = zip(*self.dataMetricsFilesList)
                    if self.dataElectricIllFilesList:
                        electricFiles,electricFilesNames = zip(*self.dataElectricIllFilesList)
                    else:
                        electricFiles=[]
                        electricFilesNames=[]
                    mainComboBoxContents = [illFileKeys[0]]+ \
                                           sorted(list(resultsFiles))+ \
                                           sorted(list(electricFiles))

                except ValueError:
                    mainComboBoxContents = [illFileKeys[0]]

                self.cmbSpacePlotType.clear()
                self.cmbSpacePlotType.addItems(mainComboBoxContents)



                self.cmbSpaceSelectIlluminanceFile.clear()
                self.cmbSpaceSelectIlluminanceFile.addItems(illFileKeys)
                self.cmbCombinedSelectIlluminanceFile.clear()
                self.cmbCombinedSelectIlluminanceFile.addItems(illFileKeys)


                self.spacePlotTypeDict = self.dataAllFilesAvailable


                self.spShadeSchedule = self.dataProject.spaces[self.dataSpaceIndex].scheduleShades
                self.spWindowGroupNames = [windowGroup.name for windowGroup in self.dataProject.spaces[self.dataSpaceIndex].windowGroups]
                self.spShowWindowGroupInfo = True #Toggle this to False in case window Group info isn't to be shown.

                if self.spShadeSchedule and self.spShowWindowGroupInfo:
                    shadeData = TimeArray(self.spShadeSchedule)
                    shadeData = [map(int,timedata['readStadicData']) for timedata in shadeData.timedata]
                    self.spShadeSchedule = shadeData

                self.btnSpaceSettingsContour.clicked.connect(self.spToggleContourSettings)
                self.btnSpaceSettingsColours.clicked.connect(self.spToggleColorSettings)
                self.calSpaceDateTimeIllum.dateChanged.connect(self.spSetCurrentIlluminanceHourCalendar)
                self.cmbSpaceTimeIllum.currentIndexChanged.connect(self.spSetCurrentIlluminanceHourCalendar)

                self.btnSpacePrevHour.clicked.connect(lambda:self.spSetCurrentIlluminanceHourTimeStep(False))
                self.btnSpaceNextHour.clicked.connect(lambda:self.spSetCurrentIlluminanceHourTimeStep(True))

                #If the timestep settings are changed, change the time step but don't trigger the illuminance plot.
                self.cmbSpaceIlluminanceStepType.currentIndexChanged.connect(self.spUpdateIlluminanceTimeStep)
                self.cmbSpaceIluminanceStepValue.currentIndexChanged.connect(self.spUpdateIlluminanceTimeStep)

                #Settings for displaying the opacity value on a box.
                self.sliderSpaceOpacity.valueChanged.connect(self.spOpacitySliderChanged)


                #Settings for color values of the illuminance plot.
                self.btnSelectColorLowerMask.clicked.connect(lambda:self.spMaskSettingsActivated(False))
                self.btnSelectColorUpperMask.clicked.connect(lambda:self.spMaskSettingsActivated(True))

                self.btnSpaceResetColors.clicked.connect(self.spResetColorSettings)
                self.btnSpaceSetColors.clicked.connect(self.spSetColorSettings)

                #settings for contour values for the illuminance plot.
                self.cmbSpaceContourQuantity.currentIndexChanged.connect(self.spSetContourQuantity)


                self.chkSpaceColors.clicked.connect(self.spRefreshPlots)
                self.chkSpaceContours.clicked.connect(self.spRefreshPlots)

                self.btnSpaceResetContours.clicked.connect(self.spResetContourSettings)
                self.btnSpaceSetContours.clicked.connect(self.spSetContourSettings)

                self.btnSpaceSetColorScheme.clicked.connect(self.spAssignSpaceColorScheme)

                self.cmbSpacePlotType.currentIndexChanged.connect(self.spPlotTypeSelect)

                self.cmbSpaceSelectIlluminanceFile.currentIndexChanged.connect(self.spLoadDifferentIlluminanceFile)

                self.cmbSpaceTimeIllum.setCurrentIndex(10)

                # self.spCanvas.mpl_connect('motion_notify_event',self.spMouseClicked)

                # self.spCurrentDataSet = None



                self.txtSpaceMsgBox.setText(self.dataLog)

                # TODO: Delete the line below to enable the timeseries stuff.
                self.tabWidget.removeTab(2)

    def spMouseClicked(self,event):
        """
        I am leaving this on for future reference for event releated stuff
        :param event:
        :return:
        """
        xdata,ydata = event.xdata,event.ydata

        if xdata and ydata:
            xCor = list(self.illData.roomgrid.uniCorX)
            yCor = list(self.illData.roomgrid.uniCorY)
            xCorLen,yCorLen = len(xCor),len(yCor)
            currentData = self.spCurrentDataSet
            xloc = bisect.bisect(xCor,xdata)
            yloc = bisect.bisect(yCor,ydata)


    def spSetContourSettings(self):
        contourList = []
        for box in self.spContourBoxes:
            if box.isEnabled() and box.text():
                contourList.append(float(str(box.text())))
        if self.spCurrentPlotIsIlluminance:
            self.spContourValuesIlluminance = list(contourList)
            self.spPlotIlluminance()
        elif self.spCurrentPlotIsElectric:
            self.spContourValuesElectric = list(contourList)
            self.spPlotElectric()
        else:
            self.spContourValuesMetrics = list(contourList)
            self.spPlotMetrics()

    def spResetContourSettings(self):
        self.cmbSpaceContourQuantity.setCurrentIndex(6)

        for idx,box in enumerate(self.spContourBoxes):
            if self.spCurrentPlotIsIlluminance:
                box.setText(str(self.spContourValuesIlluminanceDefault[idx]))
            elif self.spCurrentPlotIsElectric:
                box.setText(str(self.spContourValuesElectricDefault[idx]))
            else:
                box.setText(str(self.spContourValuesMetricsDefault[idx]))

    def spRefreshPlots(self):
        """
        This is required because there are certain events that just need to trigger the current plot.
        :return:
        """
        if self.spCurrentPlotIsIlluminance:
            self.spPlotIlluminance()
        elif self.spCurrentPlotIsElectric:
           self.spPlotElectric()
        else:
            self.spPlotMetrics()

    def spLoadDifferentIlluminanceFile(self):
        selectedIllFileKey = str(self.cmbSpaceSelectIlluminanceFile.currentText())
        selectedIllFile = self.spAllFilesDict[selectedIllFileKey]
        self.illData = Dayill(selectedIllFile,self.ptsFile)
        self.txtSpaceStatusDisplay.setText("Current space: {} \tCurrent readStadicData set: {}.\t Source:{}".format(self.dataSpaceNameSelected, selectedIllFileKey, selectedIllFile))
        self.spPlotIlluminance()

    def spOpenJsonFileDirectly(self):
        jsonFileName = QtGui.QFileDialog.getOpenFileName(self,"Select a json file to open","C:/","Json File (*.json)")
        if jsonFileName:
             self.jsonFile = str(jsonFileName)
             self.txtJsonPath.setText(jsonFileName)
             project = StadicProject(jsonFileName)

             spaceTuple = [space.spaceName for space in project.spaces]
             self.cmbSpaceName.clear()
             self.cmbSpaceName.addItems(spaceTuple)

             self.cmbSpaceName.setEnabled(True)
             self.btnSelectSpaceName.setEnabled(True)

             newWindowTitle = jsonFileName+"  --  "+self.defaultWindowTitle
             self.setWindowTitle(newWindowTitle)


             del project

    def spLoadVisualsFromOpenedJsonFile(self):
        self.txtSpaceStatusDisplay.clear()
        self.spLoadJson(self.jsonFile, self.cmbSpaceName.currentIndex())
        self.tabWidget.setEnabled(True)

    def spAssignSpaceColorScheme(self):
        currentColor = self.spColorDict[str(self.cmbSpaceColorScheme.currentText())]

        if self.chkSpaceColorSchemeInvert.checkState():
            currentColor += "_r"

        if self.chkSpaceColorSchemeInterpolate.checkState():
            self.spInterpolateColorScheme = 'nearest'
        else:
            self.spInterpolateColorScheme = 'hanning'

        if self.spCurrentPlotIsIlluminance:
            self.spCurrentColorScheme = currentColor
            self.spCurrentSpaceChartOpacityValue = self.sliderSpaceOpacity.value() / 100.0
            self.spPlotIlluminance()
        elif self.spCurrentPlotIsElectric:
            self.spCurrentColorSchemeElectric = currentColor
            self.spCurrentSpaceChartOpacityValueElectric = self.sliderSpaceOpacity.value() / 100.0
            self.spPlotElectric()

        else:

            self.spCurrentColorSchemeMetrics = currentColor
            self.spCurrentSpaceChartOpacityValueMetrics = self.sliderSpaceOpacity.value() / 100.0
            self.spPlotMetrics()

        # TODO:Change this to mean all plots later.

    def spSetContourQuantity(self):
        contourQuantity = int(self.cmbSpaceContourQuantity.currentText())
        for idx,contourBoxes in enumerate(self.spContourBoxes):
            if (idx+2-1)>contourQuantity:
                contourBoxes.clear()
                contourBoxes.setEnabled(False)
            else:
                contourBoxes.setEnabled(True)

    def spMaskSettingsActivated(self, isUpperMask):
        colorDialog = QtGui.QColorDialog
        selectedColor = colorDialog.getColor()

        if selectedColor.isValid():
            selectedColor = selectedColor.getRgb()
            if isUpperMask:
                self.txtSpaceColorsUpperMask.setStyleSheet("background-color: rgb{}".format(selectedColor))
                if self.spCurrentPlotIsIlluminance:
                    self.spIlluminanceUpperMaskColor = selectedColor
                elif self.spCurrentPlotIsElectric:
                    self.spElectricUpperMaskColor = selectedColor
                else:
                    self.spMetricsUpperMaskColor = selectedColor
            else:
                self.txtSpaceColorsLowerMask.setStyleSheet("background-color: rgb{}".format(selectedColor))
                if self.spCurrentPlotIsIlluminance:
                    self.spIlluminanceLowerMaskColor = selectedColor
                elif self.spCurrentPlotIsElectric:
                    self.spElectricLowerMaskColor = selectedColor
                else:
                    self.spMetricsLowerMaskColor = selectedColor

    def spSetCurrentIlluminanceHourCalendar(self):
        """
        Plot illuminance based on a selection from the calendar
        """
        dateVal = self.calSpaceDateTimeIllum.dateTime().date().dayOfYear()
        self.spCurrentIlluminanceHour = (dateVal - 1) * 24 + self.cmbSpaceTimeIllum.currentIndex()
        self.spPlotIlluminance()

    def spSetCurrentIlluminanceHourTimeStep(self, stepForward):
        currentHour = self.spCurrentIlluminanceHour
        currentHourOriginal = currentHour
        skipDarkHours = self.chkSpaceSkipDarkHours.checkState()
        timeStep = self.spTimeStepIlluminance

        lowerInterval = self.cmbSpaceTimeIntervalMin.currentIndex()
        higherInterval = self.cmbSpaceTimeIntervalMax.currentIndex()
        intervals = sorted(range(*sorted([lowerInterval,higherInterval])))

        if intervals:
            intervals.extend([max(intervals)+1])
        else:
            intervals.extend([lowerInterval])


        if stepForward:
            currentHour += timeStep
            currentDay = (currentHour+1)//24
            currentDayHour = currentHour%24
            if currentDayHour not in intervals:
                currentDay += 1
                currentHour = currentDay*24+intervals[0]
            if skipDarkHours:
                while currentHour<8759 and max(self.illData.timedata[currentHour]['readStadicData'].illarr)==0:
                    currentHour += 1

        else:
            currentHour -= timeStep
            currentDay = (currentHour+1)//24
            currentDayHour = currentHour%24
            if currentDayHour not in intervals:
                currentDay -= 1
                currentHour = currentDay*24+intervals[-1]
            if skipDarkHours:
                while currentHour>-1 and max(self.illData.timedata[currentHour]['readStadicData'].illarr)==0:
                    currentHour -= 1

        #If the current skipped hour turns out to be dark, then just rever to the original value.
        if skipDarkHours and -1<currentHour<8760 and  max(self.illData.timedata[currentHour]['readStadicData'].illarr)==0:
            currentHour = currentHourOriginal

        if -1<currentHour<8760:
            self.spCurrentIlluminanceHour = currentHour
            self.spPlotIlluminance()

    def spUpdateIlluminanceTimeStep(self):
        """
        Update illuminance time step in case corresponding controls are updated.
        :return:
        """
        #0 corresponds to hour while 1 corresponds to day.
        timeStepType = {0:1,1:24}[self.cmbSpaceIlluminanceStepType.currentIndex()]
        timeStepMultiplier = int(self.cmbSpaceIluminanceStepValue.currentText())
        self.spTimeStepIlluminance = timeStepMultiplier * timeStepType


    def spOpacitySliderChanged(self):
        opacityValue = self.sliderSpaceOpacity.value()
        self.txtSpaceOpacityValue.setText(str(opacityValue))

    def spToggleContourSettings(self):
        visibility = self.grpContoursIlluminance.isVisible()

        if not visibility:
            self.btnSpaceSettingsContour.setText("Hide Settings")
            self.grpContoursIlluminance.setVisible(True)
        else:
            self.btnSpaceSettingsContour.setText("Show Settings")
            self.grpContoursIlluminance.setVisible(False)

    def spSetColorSettings(self):
        if self.spCurrentPlotIsIlluminance:
            try:
                self.spIlluminanceUpperMaskValue = float(str(self.txtSpaceColorsUpperMask.text()))
            except ValueError:
                pass
            try:
                self.spIlluminanceLowerMaskValue = float(self.txtSpaceColorsLowerMask.text())
            except ValueError:
                pass
            self.spIlluminanceMaxVal = float(self.txtSpaceColorsMax.text())
            self.spIlluminanceMinVal = float(self.txtSpaceColorsMin.text())
            self.spPlotIlluminance()

        elif self.spCurrentPlotIsElectric:
            try:
                self.spElectricUpperMaskValue = float(str(self.txtSpaceColorsUpperMask.text()))
            except ValueError:
                pass
            try:
                self.spElectricLowerMaskValue = float(self.txtSpaceColorsLowerMask.text())
            except ValueError:
                pass
            self.spElectricMaxVal = float(self.txtSpaceColorsMax.text())
            self.spElectricMinVal = float(self.txtSpaceColorsMin.text())
            self.spPlotElectric()

        else:
            try:
                self.spMetricsUpperMaskValue = float(str(self.txtSpaceColorsUpperMask.text()))
            except ValueError:
                pass
            try:
                self.spMetricsLowerMaskValue = float(self.txtSpaceColorsLowerMask.text())
            except ValueError:
                pass
            self.spMetricsMaxVal = float(self.txtSpaceColorsMax.text())
            self.spMetricsMinVal = float(self.txtSpaceColorsMin.text())
            self.spPlotMetrics()

    def spResetColorSettings(self):
        self.txtSpaceColorsLowerMask.setStyleSheet("")
        self.txtSpaceColorsUpperMask.setStyleSheet("")
        self.txtSpaceColorsUpperMask.clear()
        self.txtSpaceColorsUpperMask.setEnabled(False)
        self.txtSpaceColorsUpperMask.setPlaceholderText('')
        self.txtSpaceColorsLowerMask.clear()
        self.txtSpaceColorsLowerMask.setEnabled(False)
        self.txtSpaceColorsLowerMask.setPlaceholderText('')

        if self.spCurrentPlotIsIlluminance:
            self.txtSpaceColorsMax.setText(str(self.spIlluminanceMaxValDefault))
            self.txtSpaceColorsMin.setText(str (self.spIlluminanceMinValDefault))
            self.spIlluminanceLowerMaskColor = None
            self.spIlluminanceUpperMaskColor = None
            self.spIlluminanceMaxVal = float(self.txtSpaceColorsMax.text())
            self.spIlluminanceMinVal = float(self.txtSpaceColorsMin.text())
            self.spPlotIlluminance()
        elif self.spCurrentPlotIsElectric:
            self.txtSpaceColorsMax.setText(str(self.spElectricMaxValDefault))
            self.txtSpaceColorsMin.setText(str (self.spElectricMinValDefault))
            self.spElectricLowerMaskColor = None
            self.spElectricUpperMaskColor = None
            self.spElectricMaxVal = float(self.txtSpaceColorsMax.text())
            self.spElectricMinVal = float(self.txtSpaceColorsMin.text())
            self.spPlotElectric()

        else:
            self.txtSpaceColorsMax.setText(str(self.spMetricsMaxValDefault))
            self.txtSpaceColorsMin.setText(str (self.spMetricsMinValDefault))
            self.spMetricsLowerMaskColor = None
            self.spMetricsUpperMaskColor = None

            self.spMetricsMaxVal = float(self.txtSpaceColorsMax.text())
            self.spMetricsMinVal = float(self.txtSpaceColorsMin.text())

            self.spPlotMetrics()

    def spToggleColorSettings(self):
        visibility = self.grpColoursIlluminance.isVisible()

        if not visibility:
            self.btnSpaceSettingsColours.setText("Hide Settings")
            self.grpColoursIlluminance.setVisible(True)
        else:
            self.btnSpaceSettingsColours.setText("Show Settings")
            self.grpColoursIlluminance.setVisible(False)

    def spPlotTypeSelect(self):
        """
            Plot metrics or illuminance readStadicData based on the selection from the main combo box for space.

        """
        currentSelection = str(self.cmbSpacePlotType.currentText())
        filesDict = self.spacePlotTypeDict
        if filesDict:
            currentFile = filesDict[currentSelection]

            if currentFile.endswith(".ill") and 'electric zone' not in currentSelection.lower():
                selectedIllFileKey = [key for key,items in self.spAllFilesDict.items() if items == currentFile][0]
                self.illData = Dayill(currentFile,self.ptsFile)
                self.txtSpaceStatusDisplay.setText("Current space: {} \tCurrent readStadicData set: {}.\t Source:{}".format(self.dataSpaceNameSelected, selectedIllFileKey, currentFile))
                self.spPlotIlluminance()
                self.grpSpaceIlluminance.setVisible(True)
                self.spCurrentPlotIsIlluminance=True

                self.sliderSpaceOpacity.setValue(self.spCurrentSpaceChartOpacityValue * 100)
                currentColorScheme = self.spCurrentColorScheme

            elif 'electric zone' in currentSelection.lower():
                with open(currentFile)as metricsFile:
                    electricData = map(float,metricsFile.read().split())
                    self.spElectricData = list(electricData)
                    self.spCurrentElectricZoneName = currentSelection
                    self.spPlotElectric()
                self.txtSpaceStatusDisplay.setText("Current space: {} \tCurrent readStadicData set: {}.\t Source:{}".format(self.dataSpaceNameSelected,currentSelection,currentFile))
                self.grpSpaceIlluminance.setVisible(False)
                self.spCurrentPlotIsIlluminance = False
                self.spCurrentPlotIsElectric = True
                self.sliderSpaceOpacity.setValue(self.spCurrentSpaceChartOpacityValueMetrics * 100)
                currentColorScheme = self.spCurrentColorSchemeElectric



            elif currentFile.endswith(".res"):
                with open(currentFile)as metricsFile:
                    metricsData = map(float,metricsFile.read().split())
                    self.spMetricsData = list(metricsData)
                    self.spCurrentMetricsName = currentSelection
                    self.spPlotMetrics()
                self.txtSpaceStatusDisplay.setText("Current space: {} \tCurrent readStadicData set: {}.\t Source:{}".format(self.dataSpaceNameSelected,currentSelection,currentFile))
                self.grpSpaceIlluminance.setVisible(False)

                self.spCurrentPlotIsIlluminance = False

                # TODO: Uncomment this one. !
                self.spCurrentPlotIsElectric = False
                self.sliderSpaceOpacity.setValue(self.spCurrentSpaceChartOpacityValueMetrics * 100)
                currentColorScheme = self.spCurrentColorSchemeMetrics


                # currentIndex = [idx for idx,value in enumerate(self.cmbSpaceColorScheme.)]
                # print(currentIndex)

            #I am resetting the values for colors and contours everytime. Ideally I should be saving state for each occassion but that will result in too much readStadicData getting store in
            #each instance.
            self.spResetColorSettings()
            self.spResetContourSettings()

            if currentColorScheme.endswith("_r"):
                self.chkSpaceColorSchemeInvert.setChecked(True)
                currentColorScheme = currentColorScheme[:-2]
            else:
                self.chkSpaceColorSchemeInvert.setChecked(False)

            if self.spInterpolateColorScheme == 'nearest':
                self.chkSpaceColorSchemeInterpolate.setChecked(True)
            else:
                self.chkSpaceColorSchemeInterpolate.setChecked(False)

            colorSchemes= zip(*self.spColorMapTuple)[1]

            currentColorIndex = colorSchemes.index(currentColorScheme)
            self.cmbSpaceColorScheme.setCurrentIndex(currentColorIndex)

    def spPlotIlluminance(self):
        if not self.spIlluminanceActivated:

            self.spToolbar = NavigationToolbarStadic(self.spCanvas, self)

            self.layoutSpace.addWidget(self.spToolbar)
            self.layoutSpace.addWidget(self.spCanvas)
            self.spIlluminanceActivated = True

        xCor = self.illData.roomgrid.uniCor['x']
        yCor = self.illData.roomgrid.uniCor['y']
        data = self.illData.timedata[self.spCurrentIlluminanceHour]['readStadicData'].illarr


        # if len(readStadicData)<len(xCor)*len(yCor):
        #     readStadicData = readStadicData + [0]*(len(xCor)*len(yCor)-len(readStadicData))

        timeStamp = self.illData.timedata[self.spCurrentIlluminanceHour]['tstamp']
        timeStamp = timeStamp.strftime("%I:%M%p on %b %d")

        colorScheme = self.spCurrentColorScheme
        alphaVal = self.spCurrentSpaceChartOpacityValue

        upperMask = self.spIlluminanceUpperMaskColor
        lowerMask = self.spIlluminanceLowerMaskColor

        plotTitle = str("Illuminance at {}".format(timeStamp).strip())

        if self.spShowWindowGroupInfo and self.spShadeSchedule:
            shadeScheduleCurrentHour = self.spShadeSchedule[self.spCurrentIlluminanceHour]
            groupNames = map(str,self.spWindowGroupNames)
            groupNames = map(str.strip,groupNames)
            shadeSettings = zip(groupNames,shadeScheduleCurrentHour)
            shadeSettings = str("\nShade Settings: {}".format(shadeSettings))
            plotTitle += shadeSettings

        contourValues = self.spContourValuesIlluminance

        self.spToolbar.dataType = self.dataProject.unitsIlluminance

        self.spCurrentDataSet = data


        gridPlot(data, xCor, yCor,plotTitle,"X Coordinates","Y Coordinates",
                 fullDataGrid=self.illData.roomgrid.gridMatrixLocations, figVal=self.spFigure, colormap=colorScheme,
                 alpha=alphaVal, colorMax=self.spIlluminanceMaxVal, colorMin=self.spIlluminanceMinVal, lowerMask=lowerMask,
                 upperMask=upperMask, plotColors=self.chkSpaceColors.checkState(), plotContours=self.chkSpaceContours.checkState(),
                 contourValues=contourValues,interpolationVal=self.spInterpolateColorScheme)

        self.spCanvas.draw()

    def spPlotMetrics(self):
        if not self.spIlluminanceActivated:
            self.spToolbar = NavigationToolbarStadic(self.spCanvas, self)
            self.layoutSpace.addWidget(self.spToolbar)
            self.layoutSpace.addWidget(self.spCanvas)
            self.spIlluminanceActivated = True


        xCor = self.illData.roomgrid.uniCor['x']
        yCor = self.illData.roomgrid.uniCor['y']
        data = self.spMetricsData


        colorScheme = self.spCurrentColorSchemeMetrics
        alphaVal = self.spCurrentSpaceChartOpacityValueMetrics

        upperMask = self.spMetricsUpperMaskColor
        lowerMask = self.spMetricsLowerMaskColor

        #This replace is a quick hack for cases where Illuminance is abbreivated as Illuminance
        currentMetricsName = self.spCurrentMetricsName.replace("Illum", "Illuminance")
        currentMetricsName = self.dataSpaceNamesDict[self.spCurrentMetricsName]
        self.spCurrentDataSet = data

        self.spToolbar.dataType = "%"

        gridPlot(data, xCor, yCor, currentMetricsName,"X Coordinates","Y Coordinates",
                 fullDataGrid=self.illData.roomgrid.gridMatrixLocations, figVal=self.spFigure, colormap=colorScheme,
                 alpha=alphaVal, colorMax=self.spMetricsMaxVal, colorMin=self.spMetricsMinVal, lowerMask=lowerMask,
                 upperMask=upperMask, plotColors=self.chkSpaceColors.checkState(), plotContours=self.chkSpaceContours.checkState(), contourValues=self.spContourValuesMetrics,
                 interpolationVal=self.spInterpolateColorScheme)

        self.spCanvas.draw()

    def spPlotElectric(self):
        if not self.spIlluminanceActivated:
            self.spToolbar = NavigationToolbarStadic(self.spCanvas, self)
            self.layoutSpace.addWidget(self.spToolbar)
            self.layoutSpace.addWidget(self.spCanvas)
            self.spIlluminanceActivated = True

        xCor = self.illData.roomgrid.uniCor['x']
        yCor = self.illData.roomgrid.uniCor['y']
        data = self.spElectricData

        colorScheme = self.spCurrentColorSchemeElectric
        alphaVal = self.spCurrentSpaceChartOpacityValueElectric

        upperMask = self.spElectricUpperMaskColor
        lowerMask = self.spElectricLowerMaskColor

        # This replace is a quick hack for cases where Illuminance is abbreivated as Illuminance
        currentZoneName = self.spCurrentElectricZoneName

        self.spCurrentDataSet = data

        self.spToolbar.dataType = self.dataProject.unitsIlluminance

        gridPlot(data, xCor, yCor, currentZoneName, "X Coordinates",
                 "Y Coordinates",
                 fullDataGrid=self.illData.roomgrid.gridMatrixLocations,
                 figVal=self.spFigure, colormap=colorScheme,
                 alpha=alphaVal, colorMax=self.spElectricMaxVal,
                 colorMin=self.spElectricMinVal, lowerMask=lowerMask,
                 upperMask=upperMask, plotColors=self.chkSpaceColors.checkState(),
                 plotContours=self.chkSpaceContours.checkState(),
                 contourValues=self.spContourValuesElectric,
                 interpolationVal=self.spInterpolateColorScheme)

        self.spCanvas.draw()


    @property
    def illData(self):
        return self._illData

    @illData.setter
    def illData(self,value):
        self._illData = value
        self.checkPointsFileSpacing(value)

    @property
    def spMetricsData(self):
        return self._spMetricsData

    @spMetricsData.setter
    def spMetricsData(self,value):
        self._spMetricsData = value
        self.checkPointsFileSpacing(self.illData)


    def checkPointsFileSpacing(self,illData):
        roomGrid = illData.roomgrid
        coordDict = {'z_spacings': 'coordinates in the Z axis',
                     'y_spacings': 'coordinates in the Y axis',
                     'x_spacings': 'coordinates in the X axis'}
        msg = ''
        setPtsErrorMsg = ''
        for key, value in roomGrid.testUniformSpc.items():
            if len(value) > 1:
                if not setPtsErrorMsg:
                    setPtsErrorMsg = "The readStadicData set cannot be plotted properly due to " \
                                     "the structure of the points file {} " \
                                     "not being in a compatible format.\n\n".format(self.dataPtsFile)
                    msg += setPtsErrorMsg
                msg += "The {} are not uniformly spaced. The spacing intervals" \
                       " are {}.\n".\
                    format(coordDict[key],",".join(map(str, value)))

        if len(roomGrid.testUniformSpc['z_spacings'])>0:
            msg += "There are multiple values for the z coordinate in the points" \
                   " file. The values are {}".format(",".join(map(str,roomGrid.uniCorZ)))

        if msg:
            self.displayInErrorBox(msg)

    def displayInErrorBox(self,msg):
        """Copy existing readStadicData, then add new readStadicData to the error box and display."""
        if not self.spErrorDataDisplayVisible:
            for values in self.spErrorDataDisplay:
                values.setVisible(True)
        currentText = str(self.txtSpaceErrorBox.toPlainText())
        msg = "{0}\n{1}\n{0}".format("-"*84,msg)
        if currentText:
            newText = currentText + "\n\n" + msg
        else:
            newText = msg
        self.txtSpaceErrorBox.setText(newText)
def main(jsonFile=None,spaceID=None,*args):

    app = QtGui.QApplication(sys.argv)

    if len(sys.argv)>=3:
        jsonFile = sys.argv[-2]
        spaceID = int(sys.argv[-1])
    else:
        jsonFile=spaceID=None

    form = Spatial()
    form.show()
    app.exec_()

if __name__ =="__main__":
    pass