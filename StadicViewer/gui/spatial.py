# coding=utf-8
from __future__ import  print_function

from PyQt4 import QtCore,QtGui
from StadicViewer.vis.gui import Ui_Form
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import warnings
import os,sys,operator

from StadicViewer.data.procData import VisData


from visuals.gridPlots import gridPlot
from visuals.heatMaps import thermalPlots

from results.dayIll import Dayill
from software.stadic.readStadic import StadicProject



class Spatial(QtGui.QDialog, Ui_Form,VisData):

    def setupGui(self):

            if self.dataSpaceNameSelected:
                self.tabWidget.setEnabled(True)
                self.grpContoursIlluminance.setEnabled(True)
                self.btnSpaceSettingsContour.setEnabled(True)

                #Setup matplotlib inside Qt.
                self.spFigure = Figure()
                self.spCanvas = FigureCanvas(self.spFigure)


                #Validator for setting values
                floatValidator = QtGui.QDoubleValidator(0.0,20000.0,3)

                #Settings for showing and hiding color and contours.
                self.grpColoursIlluminance.setVisible(False)
                self.grpContoursIlluminance.setVisible(False)
                self.btnSpaceSettingsContour.clicked.connect(self.spToggleContourSettings)
                self.btnSpaceSettingsColours.clicked.connect(self.spToggleColorSettings)

                #Initiate a dictioanry for ill files.
                self.spAllFilesDict = {}

                #Code for manipulating navigation settings for illuminance.
                #Code for manipulating navigation settings for illuminance.

                self.spTimeStepIlluminance = 1 #This attribute determines the time step for stepping between different illuminance plots.

                #Changing/clicking any of the below controls should trigger the illuminance plots.
                self.calSpaceDateTimeIllum.dateChanged.connect(self.spSetCurrentIlluminanceHourCalendar)
                self.cmbSpaceTimeIllum.currentIndexChanged.connect(self.spSetCurrentIlluminanceHourCalendar)


                self.btnSpacePrevHour.clicked.connect(lambda:self.spSetCurrentIlluminanceHourTimeStep(False))
                self.btnSpaceNextHour.clicked.connect(lambda:self.spSetCurrentIlluminanceHourTimeStep(True))

                #If the timestep settings are changed, change the time step but don't trigger the illuminance plot.
                self.cmbSpaceIlluminanceStepType.currentIndexChanged.connect(self.spUpdateIlluminanceTimeStep)
                self.cmbSpaceIluminanceStepValue.currentIndexChanged.connect(self.spUpdateIlluminanceTimeStep)


                self.spIlluminanceActivated = False
                self.spCurrentIlluminanceHour = 9


                #Settings for displaying the opacity value on a box.
                self.sliderSpaceOpacity.valueChanged.connect(self.spOpacitySliderChanged)


                #Settings for color values of the illuminance plot.
                self.btnSelectColorLowerMask.clicked.connect(lambda:self.spMaskSettingsActivated(False))
                self.btnSelectColorUpperMask.clicked.connect(lambda:self.spMaskSettingsActivated(True))

                self.spIlluminanceMaxVal = 5000
                self.spIlluminanceMinVal = 1

                self.spIlluminanceMaxValDefault = 5000
                self.spIlluminanceMinValDefault = 1
                self.spIlluminanceUpperMaskValue = None
                self.spIlluminanceLowerMaskValue = None
                self.spIlluminanceUpperMaskColor = None
                self.spIlluminanceLowerMaskColor = None


                self.spMetricsMaxVal = 1.0
                self.spMetricsMinVal = 0.0
                self.spMetricsMaxValDefault = 1.0
                self.spMetricsMinValDefault = 0
                self.spMetricsUpperMaskValue = None
                self.spMetricsLowerMaskValue = None
                self.spMetricsUpperMaskColor = None
                self.spMetricsLowerMaskColor = None


                self.spCurrentPlotIsIlluminance = True


                self.txtSpaceColorsMax.setText(str(self.spIlluminanceMaxValDefault))
                self.txtSpaceColorsMin.setText(str(self.spIlluminanceMinValDefault))
                self.txtSpaceColorsMax.setValidator(floatValidator)
                self.txtSpaceColorsMin.setValidator(floatValidator)

                self.btnSpaceResetColors.clicked.connect(self.spResetColorSettings)
                self.btnSpaceSetColors.clicked.connect(self.spSetColorSettings)


                self.chkSpaceColors.clicked.connect(self.spRefreshPlots)
                self.spPlotIlluminanceColors = True


                #settings for contour values for the illuminance plot.
                self.cmbSpaceContourQuantity.currentIndexChanged.connect(self.spSetContourQuantity)
                #Put all contourboxes inside a list for easy iteration.
                self.spContourBoxes = [self.txtSpaceCountourValue1, self.txtSpaceCountourValue2, self.txtSpaceCountourValue3, self.txtSpaceCountourValue4,
                                       self.txtSpaceCountourValue5, self.txtSpaceCountourValue6, self.txtSpaceCountourValue7, self.txtSpaceCountourValue8]

                for contourBox in self.spContourBoxes:
                    contourBox.setValidator(floatValidator)

                self.chkSpaceContours.clicked.connect(self.spRefreshPlots)

                self.spContourValuesIlluminance = (50, 100, 500, 1000, 2000, 3000, 5000, 10000)
                self.spContourValuesIlluminanceDefault = (50, 100, 500, 1000, 2000, 3000, 5000, 10000)
                self.spContourValuesMetrics = (0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.0)
                self.spContourValuesMetricsDefault = (0.1, 0.2, 0.3, 0.4, 0.5, 0.7, 0.9, 1.0)

                self.btnSpaceResetContours.clicked.connect(self.spResetContourSettings)
                self.btnSpaceSetContours.clicked.connect(self.spSetContourSettings)

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

                self.btnSpaceSetColorScheme.clicked.connect(self.spAssignSpaceColorScheme)

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

                self.spAllFilesDict = self.dataAllFiles

                # Addedd this test as sometimes metrics are not calculated. In those cases it's just the illuminance data.
                try:
                    resultsFiles,resultsFilesNames = zip(*self.dataMetricsFilesList)
                    mainComboBoxContents = [illFileKeys[0]]+ sorted(list(resultsFiles))
                except ValueError:
                    mainComboBoxContents = [illFileKeys[0]]

                self.cmbSpacePlotType.clear()
                self.cmbSpacePlotType.addItems(mainComboBoxContents)
                self.cmbSpacePlotType.currentIndexChanged.connect(self.spPlotTypeSelect)


                self.cmbSpaceSelectIlluminanceFile.clear()
                self.cmbSpaceSelectIlluminanceFile.addItems(illFileKeys)
                self.cmbSpaceSelectIlluminanceFile.currentIndexChanged.connect(self.spLoadDifferentIlluminanceFile)


                self.spacePlotTypeDict = self.dataAllFilesAvailable


                self.txtSpaceMsgBox.setText(self.dataLog)



    def spSetContourSettings(self):
        contourList = []
        for box in self.spContourBoxes:
            if box.isEnabled() and box.text():
                contourList.append(float(str(box.text())))
        if self.spCurrentPlotIsIlluminance:
            self.spContourValuesIlluminance = list(contourList)
            self.spPlotIlluminance()
        else:
            self.spContourValuesMetrics = list(contourList)
            self.spPlotMetrics()

    def spResetContourSettings(self):
        self.cmbSpaceContourQuantity.setCurrentIndex(6)

        for idx,box in enumerate(self.spContourBoxes):
            if self.spCurrentPlotIsIlluminance:
                box.setText(str(self.spContourValuesIlluminanceDefault[idx]))
            else:
                box.setText(str(self.spContourValuesMetricsDefault[idx]))

    def spRefreshPlots(self):
        """
        This is required because there are certain events that just need to trigger the current plot.
        :return:
        """
        if self.spCurrentPlotIsIlluminance:
            self.spPlotIlluminance()
        else:
            self.spPlotMetrics()

    def spLoadDifferentIlluminanceFile(self):
        selectedIllFileKey = str(self.cmbSpaceSelectIlluminanceFile.currentText())
        selectedIllFile = self.spAllFilesDict[selectedIllFileKey]
        self.illData = Dayill(selectedIllFile,self.ptsFile)
        self.txtSpaceStatusDisplay.setText("Current space: {} \tCurrent data set: {}.\t Source:{}".format(self.dataSpaceNameSelected, selectedIllFileKey, selectedIllFile))
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

        if self.spCurrentPlotIsIlluminance:
            self.spCurrentColorScheme = currentColor
            self.spCurrentSpaceChartOpacityValue = self.sliderSpaceOpacity.value() / 100.0
            self.spPlotIlluminance()
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
                else:
                    self.spMetricsUpperMaskColor = selectedColor
            else:
                self.txtSpaceColorsLowerMask.setStyleSheet("background-color: rgb{}".format(selectedColor))
                if self.spCurrentPlotIsIlluminance:
                    self.spIlluminanceLowerMaskColor = selectedColor
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
                while currentHour<8759 and max(self.illData.timedata[currentHour]['data'].illarr)==0:
                    currentHour += 1

        else:
            currentHour -= timeStep
            currentDay = (currentHour+1)//24
            currentDayHour = currentHour%24
            if currentDayHour not in intervals:
                currentDay -= 1
                currentHour = currentDay*24+intervals[-1]
            if skipDarkHours:
                while currentHour>-1 and max(self.illData.timedata[currentHour]['data'].illarr)==0:
                    currentHour -= 1

        #If the current skipped hour turns out to be dark, then just rever to the original value.
        if skipDarkHours and -1<currentHour<8760 and  max(self.illData.timedata[currentHour]['data'].illarr)==0:
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
            Plot metrics or illuminance data based on the selection from the main combo box for space.

        """
        currentSelection = str(self.cmbSpacePlotType.currentText())
        filesDict = self.spacePlotTypeDict
        if filesDict:
            currentFile = filesDict[currentSelection]

            if currentFile.endswith(".ill"):
                selectedIllFileKey = [key for key,items in self.spAllFilesDict.items() if items == currentFile][0]
                self.illData = Dayill(currentFile,self.ptsFile)
                self.txtSpaceStatusDisplay.setText("Current space: {} \tCurrent data set: {}.\t Source:{}".format(self.dataSpaceNameSelected, selectedIllFileKey, currentFile))
                self.spPlotIlluminance()
                self.grpSpaceIlluminance.setVisible(True)
                self.spCurrentPlotIsIlluminance=True

                self.sliderSpaceOpacity.setValue(self.spCurrentSpaceChartOpacityValue * 100)
                currentColorScheme = self.spCurrentColorScheme

            elif currentFile.endswith(".res"):
                with open(currentFile)as metricsFile:
                    metricsData = map(float,metricsFile.read().split())
                    self.metricsData = list(metricsData)
                    self.currentMetricsName = currentSelection
                    self.spPlotMetrics()
                self.txtSpaceStatusDisplay.setText("Current space: {} \tCurrent data set: {}.\t Source:{}".format(self.dataSpaceNameSelected,currentSelection,currentFile))
                self.grpSpaceIlluminance.setVisible(False)
                self.spCurrentPlotIsIlluminance = False
                self.sliderSpaceOpacity.setValue(self.spCurrentSpaceChartOpacityValueMetrics * 100)
                currentColorScheme = self.spCurrentColorSchemeMetrics


                # currentIndex = [idx for idx,value in enumerate(self.cmbSpaceColorScheme.)]
                # print(currentIndex)

            #I am resetting the values for colors and contours everytime. Ideally I should be saving state for each occassion but that will result in too much data getting store in
            #each instance.
            self.spResetColorSettings()
            self.spResetContourSettings()

            if currentColorScheme.endswith("_r"):
                self.chkSpaceColorSchemeInvert.setChecked(True)
                currentColorScheme = currentColorScheme[:-2]
            else:
                self.chkSpaceColorSchemeInvert.setChecked(False)

            colorSchemes= zip(*self.spColorMapTuple)[1]

            currentColorIndex = colorSchemes.index(currentColorScheme)
            self.cmbSpaceColorScheme.setCurrentIndex(currentColorIndex)

    def spPlotIlluminance(self):
        if not self.spIlluminanceActivated:
            self.spToolbar = NavigationToolbar(self.spCanvas, self)
            self.layoutSpace.addWidget(self.spToolbar)
            self.layoutSpace.addWidget(self.spCanvas)
            self.spIlluminanceActivated = True


        xCor = self.illData.roomgrid.uniCor['x']
        yCor = self.illData.roomgrid.uniCor['y']
        data = self.illData.timedata[self.spCurrentIlluminanceHour]['data'].illarr

        # if len(data)<len(xCor)*len(yCor):
        #     data = data + [0]*(len(xCor)*len(yCor)-len(data))

        timeStamp = self.illData.timedata[self.spCurrentIlluminanceHour]['tstamp']
        timeStamp = timeStamp.strftime("%I:%M%p on %b %d")

        colorScheme = self.spCurrentColorScheme
        alphaVal = self.spCurrentSpaceChartOpacityValue

        upperMask = self.spIlluminanceUpperMaskColor
        lowerMask = self.spIlluminanceLowerMaskColor


        contourValues = self.spContourValuesIlluminance

        gridPlot(data, xCor, yCor,"Illuminance at {}".format(timeStamp),"X Coordinates","Y Coordinates",
                 fullDataGrid=self.illData.roomgrid.gridMatrixLocations, figVal=self.spFigure, colormap=colorScheme,
                 alpha=alphaVal, colorMax=self.spIlluminanceMaxVal, colorMin=self.spIlluminanceMinVal, lowerMask=lowerMask,
                 upperMask=upperMask, plotColors=self.chkSpaceColors.checkState(), plotContours=self.chkSpaceContours.checkState(),
                 contourValues=contourValues)

        self.spCanvas.draw()

    def spPlotMetrics(self):
        if not self.spIlluminanceActivated:
            self.spToolbar = NavigationToolbar(self.spCanvas, self)
            self.layoutSpace.addWidget(self.spToolbar)
            self.layoutSpace.addWidget(self.spCanvas)
            self.spIlluminanceActivated = True


        xCor = self.illData.roomgrid.uniCor['x']
        yCor = self.illData.roomgrid.uniCor['y']
        data = self.metricsData


        colorScheme = self.spCurrentColorSchemeMetrics
        alphaVal = self.spCurrentSpaceChartOpacityValueMetrics

        upperMask = self.spMetricsUpperMaskColor
        lowerMask = self.spMetricsLowerMaskColor

        #This replace is a quick hack for cases where Illuminance is abbreivated as Illuminance
        currentMetricsName = self.currentMetricsName.replace("Illum","Illuminance")

        gridPlot(data, xCor, yCor, currentMetricsName,"X Coordinates","Y Coordinates",
                 fullDataGrid=self.illData.roomgrid.gridMatrixLocations, figVal=self.spFigure, colormap=colorScheme,
                 alpha=alphaVal, colorMax=self.spMetricsMaxVal, colorMin=self.spMetricsMinVal, lowerMask=lowerMask,
                 upperMask=upperMask, plotColors=self.chkSpaceColors.checkState(), plotContours=self.chkSpaceContours.checkState(), contourValues=self.spContourValuesMetrics)

        self.spCanvas.draw()




def main(jsonFile=None,spaceID=None,*args):

    app = QtGui.QApplication(sys.argv)

    if len(sys.argv)>=3:
        jsonFile = sys.argv[-2]
        spaceID = int(sys.argv[-1])
    else:
        jsonFile=spaceID=None

    form = Spatial(jsonFile=jsonFile, spaceID=spaceID)
    form.show()
    app.exec_()

if __name__ =="__main__":
     sys.argv.extend([r"C:\C-SHAP\testC.json", 0])
     # sys.argv.extend([r'E:\debug2\base2wgangsig2.json',0])
     main()
