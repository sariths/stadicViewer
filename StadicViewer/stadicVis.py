from __future__ import  print_function

from PyQt4 import QtCore,QtGui
from vis.ui4 import Ui_Form
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import warnings
import os,sys,operator



from visuals.gridPlots import gridPlot
from visuals.heatMaps import thermalPlots

from results.dayIll import Dayill
from software.stadic.readStadic import StadicProject

warnings.filterwarnings('ignore')

class Main(QtGui.QDialog,Ui_Form):
    def __init__(self,parent=None,jsonFile=None,spaceID=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)

        self.defaultWindowTitle = str(self.windowTitle())

        # TODO: Disable runtime warnings eventually.


        # TODO:Contours
        self.grpContoursIlluminance.setEnabled(True)
        self.btnSpaceSettingsContour.setEnabled(True)




        #Setup matplotlib inside Qt.
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)


        #Validator for setting values
        floatValidator = QtGui.QDoubleValidator(0.0,20000.0,3)

        #Settings for showing and hiding color and contours.
        self.grpColoursIlluminance.setVisible(False)
        self.grpContoursIlluminance.setVisible(False)
        self.btnSpaceSettingsContour.clicked.connect(self.toggleContourSettings)
        self.btnSpaceSettingsColours.clicked.connect(self.toggleColorSettings)


        #Initiate a dictioanry for ill files.
        self.allFilesDict = {}

        #Code for manipulating navigation settings for illuminance.
        #Code for manipulating navigation settings for illuminance.

        self.timeStepIlluminance = 1 #This attribute determines the time step for stepping between different illuminance plots.

        #Changing/clicking any of the below controls should trigger the illuminance plots.
        self.calSpaceDateTimeIllum.dateChanged.connect(self.setCurrentIlluminanceHourCalendar)
        self.cmbSpaceTimeIllum.currentIndexChanged.connect(self.setCurrentIlluminanceHourCalendar)


        self.btnSpacePrevHour.clicked.connect(lambda:self.setCurrentIlluminanceHourTimeStep(False))
        self.btnSpaceNextHour.clicked.connect(lambda:self.setCurrentIlluminanceHourTimeStep(True))

        #If the timestep settings are changed, change the time step but don't trigger the illuminance plot.
        self.cmbSpaceIlluminanceStepType.currentIndexChanged.connect(self.updateIlluminanceTimeStep)
        self.cmbSpaceIluminanceStepValue.currentIndexChanged.connect(self.updateIlluminanceTimeStep)


        self.illuminanceActivated = False
        self.currentIlluminanceHour = 9


        #Settings for displaying the opacity value on a box.
        self.sliderSpaceOpacity.valueChanged.connect(self.spaceOpacitySliderChanged)


        #Settings for color values of the illuminance plot.
        self.btnSelectColorLowerMask.clicked.connect(lambda:self.maskSettingsActivated(False))
        self.btnSelectColorUpperMask.clicked.connect(lambda:self.maskSettingsActivated(True))

        self.illuminanceMaxVal = 5000
        self.illuminanceMinVal = 1

        self.illuminanceMaxValDefault = 5000
        self.illuminanceMinValDefault = 1
        self.illuminanceUpperMaskValue = None
        self.illuminanceLowerMaskValue = None
        self.illuminanceUpperMaskColor = None
        self.illuminanceLowerMaskColor = None


        self.metricsMaxVal = 1.0
        self.metricsMinVal = 0.0
        self.metricsMaxValDefault = 1.0
        self.metricsMinValDefault = 0
        self.metricsUpperMaskValue = None
        self.metricsLowerMaskValue = None
        self.metricsUpperMaskColor = None
        self.metricsLowerMaskColor = None


        self.currentPlotIsIlluminance = True


        self.txtColorsMax.setText(str(self.illuminanceMaxValDefault))
        self.txtColorsMin.setText(str( self.illuminanceMinValDefault))
        self.txtColorsMax.setValidator(floatValidator)
        self.txtColorsMin.setValidator(floatValidator)

        self.btnSpaceResetColors.clicked.connect(self.resetColorSettings)
        self.btnSpaceSetColors.clicked.connect(self.setColorSettings)


        self.chkSpaceColors.clicked.connect(self.refreshPlots)
        self.plotIlluminanceColors = True


        #settings for contour values for the illuminance plot.
        self.cmbSpaceContourQuantity.currentIndexChanged.connect(self.setContourQuantity)
        #Put all contourboxes inside a list for easy iteration.
        self.contourBoxes = [self.txtSpaceCountourValue1,self.txtSpaceCountourValue2,self.txtSpaceCountourValue3,self.txtSpaceCountourValue4,
                             self.txtSpaceCountourValue5,self.txtSpaceCountourValue6,self.txtSpaceCountourValue7,self.txtSpaceCountourValue8]

        for contourBox in self.contourBoxes:
            contourBox.setValidator(floatValidator)

        self.chkSpaceContours.clicked.connect(self.refreshPlots)

        self.contourValuesIlluminance = (50,100,500,1000,2000,3000,5000,10000)
        self.contourValuesIlluminanceDefault = (50,100,500,1000,2000,3000,5000,10000)
        self.contourValuesMetrics = (0.1,0.2,0.3,0.4,0.5,0.7,0.9,1.0)
        self.contourValuesMetricsDefault = (0.1,0.2,0.3,0.4,0.5,0.7,0.9,1.0)

        self.btnSpaceResetContours.clicked.connect(self.resetContourSettings)
        self.btnSpaceSetContours.clicked.connect(self.setContourSettings)


        #chartScheme Settings

        #Contstuctor Stuff
        self.colorMapTuple = (('Uniform01','viridis'),('Uniform02','inferno'),('Uniform03','plasma'),('Uniform04','magma'),('Blues','Blues'),
                        ('BlueGreen','BuGn'),('BluePurple','BuPu'),('GreenBlue','GnBu'),('Greens','Greens'),('Greys','Greys'),('Oranges','Oranges'),
                        ('OrangeRed','OrRd'),('PurpleBlue','PuBu'),('PurpleBlueGreen','PuBuGn'),('PurpleRed','PuRd'),('Purples','Purples'),
                        ('RedPurple','RdPu'),('Reds','Reds'),('YellowGreen','YlGn'),('YellowGreenBlue','YlGnBu'),('YellowOrangeBrown','YlOrBr'),
                        ('YellowOrangeRed','YlOrRd'),('Hot01','afmhot'),('Hot02','hot'),('Hot03','gist_heat'),('Autumn','autumn'),('Bone','bone'),('Cool','cool'),
                        ('Copper','copper'),('Spring','spring'),('Summer','summer'),('Winter','winter'))

        colorNames = [name for name,plotName in self.colorMapTuple]
        self.colorDict =dict(self.colorMapTuple)
        self.cmbSpaceColorScheme.addItems(colorNames)
        self.cmbSpaceColorScheme.setCurrentIndex(21)

        self.currentColorScheme = 'YlOrRd'
        self.currentSpaceChartOpacityValue = 1

        self.currentColorSchemeMetrics = 'YlOrRd'
        self.currentSpaceChartOpacityValueMetrics = 1

        self.btnSpaceSetColorScheme.clicked.connect(self.assignSpaceColorScheme)


        self.txtSpaceStatusDisplay.setEnabled(False)


        #Open json file settings.
        self.btnOpenJson.clicked.connect(self.openJsonFileDirectly)
        self.btnSelectSpaceName.clicked.connect(self.loadVisualsFromOpenedJsonFile)


        self.cmbSpacePlotType.currentIndexChanged.connect(self.plotTypeSelect)
        self.spacePlotTypeDict = None

        if jsonFile and spaceID is not None:
            self.jsonFile = jsonFile
            self.grpFileDialog.setEnabled(False)
            self.tabWidget.setEnabled(True)
            self.loadJson(jsonFile,spaceID)

    def setContourSettings(self):
        contourList = []
        for box in self.contourBoxes:
            if box.isEnabled() and box.text():
                contourList.append(float(str(box.text())))
        if self.currentPlotIsIlluminance:
            self.contourValuesIlluminance = list(contourList)
            self.plotIlluminance()
        else:
            self.contourValuesMetrics = list(contourList)
            self.plotMetrics()

    def resetContourSettings(self):
        self.cmbSpaceContourQuantity.setCurrentIndex(6)

        for idx,box in enumerate(self.contourBoxes):
            if self.currentPlotIsIlluminance:
                box.setText(str(self.contourValuesIlluminanceDefault[idx]))
            else:
                box.setText(str(self.contourValuesMetricsDefault[idx]))


    def refreshPlots(self):
        """
        This is required because there are certain events that just need to trigger the current plot.
        :return:
        """
        if self.currentPlotIsIlluminance:
            self.plotIlluminance()
        else:
            self.plotMetrics()

    def loadDifferentIlluminanceFile(self):
        selectedIllFileKey = str(self.cmbSpaceSelectIlluminanceFile.currentText())
        selectedIllFile = self.allFilesDict[selectedIllFileKey]
        self.illData = Dayill(selectedIllFile,self.ptsFile)
        self.txtSpaceStatusDisplay.setText("Current space: {} \tCurrent data set: {}.\t Source:{}".format(self.spaceName,selectedIllFileKey,selectedIllFile))
        self.plotIlluminance()


    def openJsonFileDirectly(self):
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

    def loadVisualsFromOpenedJsonFile(self):
        self.txtSpaceStatusDisplay.clear()
        self.loadJson(self.jsonFile,self.cmbSpaceName.currentIndex())
        self.tabWidget.setEnabled(True)

    def assignSpaceColorScheme(self):
        currentColor = self.colorDict[str(self.cmbSpaceColorScheme.currentText())]

        if self.chkSpaceColorSchemeInvert.checkState():
            currentColor += "_r"

        if self.currentPlotIsIlluminance:
            self.currentColorScheme = currentColor
            self.currentSpaceChartOpacityValue = self.sliderSpaceOpacity.value()/100.0
            self.plotIlluminance()
        else:

            self.currentColorSchemeMetrics = currentColor
            self.currentSpaceChartOpacityValueMetrics = self.sliderSpaceOpacity.value()/100.0
            self.plotMetrics()

        # TODO:Change this to mean all plots later.



    def setContourQuantity(self):
        contourQuantity = int(self.cmbSpaceContourQuantity.currentText())
        for idx,contourBoxes in enumerate(self.contourBoxes):
            if (idx+2-1)>contourQuantity:
                contourBoxes.clear()
                contourBoxes.setEnabled(False)
            else:
                contourBoxes.setEnabled(True)


    def maskSettingsActivated(self, isUpperMask):
        colorDialog = QtGui.QColorDialog
        selectedColor = colorDialog.getColor()

        if selectedColor.isValid():
            selectedColor = selectedColor.getRgb()
            if isUpperMask:
                self.txtColorsUpperMask.setStyleSheet("background-color: rgb{}".format(selectedColor))
                if self.currentPlotIsIlluminance:
                    self.illuminanceUpperMaskColor = selectedColor
                else:
                    self.metricsUpperMaskColor = selectedColor
            else:
                self.txtColorsLowerMask.setStyleSheet("background-color: rgb{}".format(selectedColor))
                if self.currentPlotIsIlluminance:
                    self.illuminanceLowerMaskColor = selectedColor
                else:
                    self.metricsLowerMaskColor = selectedColor

    def setCurrentIlluminanceHourCalendar(self):
        """
        Plot illuminance based on a selection from the calendar
        """
        dateVal = self.calSpaceDateTimeIllum.dateTime().date().dayOfYear()
        self.currentIlluminanceHour = (dateVal-1)*24+self.cmbSpaceTimeIllum.currentIndex()
        self.plotIlluminance()

    def setCurrentIlluminanceHourTimeStep(self,stepForward):
        currentHour = self.currentIlluminanceHour
        currentHourOriginal = currentHour
        skipDarkHours = self.chkSpaceSkipDarkHours.checkState()
        timeStep = self.timeStepIlluminance

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
            self.currentIlluminanceHour = currentHour
            self.plotIlluminance()

    def updateIlluminanceTimeStep(self):
        """
        Update illuminance time step in case corresponding controls are updated.
        :return:
        """
        #0 corresponds to hour while 1 corresponds to day.
        timeStepType = {0:1,1:24}[self.cmbSpaceIlluminanceStepType.currentIndex()]
        timeStepMultiplier = int(self.cmbSpaceIluminanceStepValue.currentText())
        self.timeStepIlluminance = timeStepMultiplier*timeStepType


    def spaceOpacitySliderChanged(self):
        opacityValue = self.sliderSpaceOpacity.value()
        self.txtSpaceOpacityValue.setText(str(opacityValue))

    def toggleContourSettings(self):
        visibility = self.grpContoursIlluminance.isVisible()

        if not visibility:
            self.btnSpaceSettingsContour.setText("Hide Settings")
            self.grpContoursIlluminance.setVisible(True)
        else:
            self.btnSpaceSettingsContour.setText("Show Settings")
            self.grpContoursIlluminance.setVisible(False)

    def setColorSettings(self):
        if self.currentPlotIsIlluminance:
            try:
                self.illuminanceUpperMaskValue = float(str(self.txtColorsUpperMask.text()))
            except ValueError:
                pass
            try:
                self.illuminanceLowerMaskValue = float(self.txtColorsLowerMask.text())
            except ValueError:
                pass
            self.illuminanceMaxVal = float(self.txtColorsMax.text())
            self.illuminanceMinVal = float(self.txtColorsMin.text())
            self.plotIlluminance()

        else:
            try:
                self.metricsUpperMaskValue = float(str(self.txtColorsUpperMask.text()))
            except ValueError:
                pass
            try:
                self.metricsLowerMaskValue = float(self.txtColorsLowerMask.text())
            except ValueError:
                pass
            self.metricsMaxVal = float(self.txtColorsMax.text())
            self.metricsMinVal = float(self.txtColorsMin.text())
            self.plotMetrics()


    def resetColorSettings(self):
        self.txtColorsLowerMask.setStyleSheet("")
        self.txtColorsUpperMask.setStyleSheet("")
        self.txtColorsUpperMask.clear()
        self.txtColorsUpperMask.setEnabled(False)
        self.txtColorsUpperMask.setPlaceholderText('')
        self.txtColorsLowerMask.clear()
        self.txtColorsLowerMask.setEnabled(False)
        self.txtColorsLowerMask.setPlaceholderText('')

        if self.currentPlotIsIlluminance:
            self.txtColorsMax.setText(str(self.illuminanceMaxValDefault))
            self.txtColorsMin.setText(str (self.illuminanceMinValDefault))
            self.illuminanceLowerMaskColor = None
            self.illuminanceUpperMaskColor = None
            self.illuminanceMaxVal = float(self.txtColorsMax.text())
            self.illuminanceMinVal = float(self.txtColorsMin.text())
            self.plotIlluminance()
        else:
            self.txtColorsMax.setText(str(self.metricsMaxValDefault))
            self.txtColorsMin.setText(str (self.metricsMinValDefault))
            self.metricsLowerMaskColor = None
            self.metricsUpperMaskColor = None

            self.metricsMaxVal = float(self.txtColorsMax.text())
            self.metricsMinVal = float(self.txtColorsMin.text())

            self.plotMetrics()


    def toggleColorSettings(self):
        visibility = self.grpColoursIlluminance.isVisible()

        if not visibility:
            self.btnSpaceSettingsColours.setText("Hide Settings")
            self.grpColoursIlluminance.setVisible(True)
        else:
            self.btnSpaceSettingsColours.setText("Show Settings")
            self.grpColoursIlluminance.setVisible(False)


    def loadJson(self,jsonFileName,spaceID):
        projectJson = jsonFileName

        project = StadicProject(projectJson)
        illFile = project.spaces[spaceID].resultsFile
        ptsFile = project.spaces[spaceID].analysisPointsFiles[0]

        self.spaceName =project.spaces[0].spaceName

        self.allFilesDict = project.spaces[spaceID].filesDict

        self.txtSpaceMsgBox.setText(project.spaces[spaceID].log)




        filesExisting = [(fileKey,fileName) for fileKey,fileName in self.allFilesDict.items() if fileName]

        #Get the names and keys for all the results files.
        resultsFilesOnly = [(fileKey,fileName)for fileKey,fileName in filesExisting if fileName.endswith(".res")]
        resultsFilesOnly = sorted(resultsFilesOnly,key=operator.itemgetter(1))


        #Make a list of all the ill files.
        illFilesOnly = [fileKey for fileKey,fileName in filesExisting if fileName.endswith('.ill') and fileName != illFile]
        illFilesOnlyNames = [fileName for fileKey,fileName in filesExisting if fileName.endswith('.ill') and fileName != illFile]
        mainIllFile = [fileKey for fileKey,fileName in filesExisting if fileName.endswith('.ill') and fileName == illFile]

        illFilesOnly = mainIllFile + sorted(illFilesOnly)

        if illFile:
            resultsFilesOnly.insert(0,("Illuminance",illFile))

        else:
            resultsFilesOnly.insert(0,("Illuminance",illFilesOnlyNames[0]))

        self.cmbSpacePlotType.clear()
        self.cmbSpacePlotType.addItems([fileKey for fileKey,fileName in resultsFilesOnly])

        self.spacePlotTypeDict = dict(resultsFilesOnly)

        self.cmbSpaceSelectIlluminanceFile.clear()
        self.cmbSpaceSelectIlluminanceFile.addItems(illFilesOnly)
        self.cmbSpaceSelectIlluminanceFile.currentIndexChanged.connect(self.loadDifferentIlluminanceFile)

        self.ptsFile = ptsFile

        if illFile:
            self.illData = Dayill(illFile,ptsFile)
            self.txtSpaceStatusDisplay.setText("Current space: {} \tCurrent data set: {}.\t Source:{}".format(self.spaceName,mainIllFile[0],illFile))
        else:
            self.illData = Dayill(illFilesOnlyNames[0],ptsFile)
            self.txtSpaceStatusDisplay.setText("Current space: {} \tCurrent data set: {}.\t Source:{}".format(self.spaceName,illFilesOnly[0],illFilesOnlyNames[0]))


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





        newWindowTitle =  jsonFileName+"  --  "+self.defaultWindowTitle
        self.setWindowTitle(newWindowTitle)

    def plotTypeSelect(self):
        """
            Plot metrics or illuminance data based on the selection from the main combo box for space.

        """
        currentSelection = str(self.cmbSpacePlotType.currentText())
        filesDict = self.spacePlotTypeDict
        if filesDict:
            currentFile = filesDict[currentSelection]

            if currentFile.endswith(".ill"):
                selectedIllFileKey = [key for key,items in self.allFilesDict.items() if items == currentFile][0]
                self.illData = Dayill(currentFile,self.ptsFile)
                self.txtSpaceStatusDisplay.setText("Current space: {} \tCurrent data set: {}.\t Source:{}".format(self.spaceName,selectedIllFileKey,currentFile))
                self.plotIlluminance()
                self.grpSpaceIlluminance.setVisible(True)
                self.currentPlotIsIlluminance=True

                self.sliderSpaceOpacity.setValue(self.currentSpaceChartOpacityValue*100)
                currentColorScheme = self.currentColorScheme

            elif currentFile.endswith(".res"):
                with open(currentFile)as metricsFile:
                    metricsData = map(float,metricsFile.read().split())
                    self.metricsData = list(metricsData)
                    self.currentMetricsName = currentSelection
                    self.plotMetrics()
                self.txtSpaceStatusDisplay.setText("Current space: {} \tCurrent data set: {}.\t Source:{}".format(self.spaceName,currentSelection,currentFile))
                self.grpSpaceIlluminance.setVisible(False)
                self.currentPlotIsIlluminance = False
                self.sliderSpaceOpacity.setValue(self.currentSpaceChartOpacityValueMetrics*100)
                currentColorScheme = self.currentColorSchemeMetrics


                # currentIndex = [idx for idx,value in enumerate(self.cmbSpaceColorScheme.)]
                # print(currentIndex)

            self.resetColorSettings()
            self.resetContourSettings()

            if currentColorScheme.endswith("_r"):
                self.chkSpaceColorSchemeInvert.setChecked(True)
                currentColorScheme = currentColorScheme[:-2]
            else:
                self.chkSpaceColorSchemeInvert.setChecked(False)

            colorSchemes= zip(*self.colorMapTuple)[1]

            currentColorIndex = colorSchemes.index(currentColorScheme)
            self.cmbSpaceColorScheme.setCurrentIndex(currentColorIndex)

    def plotIlluminance(self):
        if not self.illuminanceActivated:
            self.toolbar = NavigationToolbar(self.canvas,self)
            self.layoutIlluminance.addWidget(self.toolbar)
            self.layoutIlluminance.addWidget(self.canvas)
            self.illuminanceActivated = True


        xCor = self.illData.roomgrid.uniCor['x']
        yCor = self.illData.roomgrid.uniCor['y']
        data = self.illData.timedata[self.currentIlluminanceHour]['data'].illarr

        # if len(data)<len(xCor)*len(yCor):
        #     data = data + [0]*(len(xCor)*len(yCor)-len(data))

        timeStamp = self.illData.timedata[self.currentIlluminanceHour]['tstamp']
        timeStamp = timeStamp.strftime("%I:%M%p on %b %d")

        colorScheme = self.currentColorScheme
        alphaVal = self.currentSpaceChartOpacityValue

        upperMask = self.illuminanceUpperMaskColor
        lowerMask = self.illuminanceLowerMaskColor


        contourValues = self.contourValuesIlluminance

        gridPlot(data,xCor,yCor,"Illuminance at {}".format(timeStamp),"X Coordinates","Y Coordinates",
                 fullDataGrid=self.illData.roomgrid.gridMatrixLocations,figVal=self.figure,colormap=colorScheme,
                 alpha=alphaVal,colorMax=self.illuminanceMaxVal,colorMin=self.illuminanceMinVal,lowerMask=lowerMask,
                 upperMask=upperMask,plotColors=self.chkSpaceColors.checkState(),plotContours=self.chkSpaceContours.checkState(),
                 contourValues=contourValues)

        self.canvas.draw()

    def plotMetrics(self):
        if not self.illuminanceActivated:
            self.toolbar = NavigationToolbar(self.canvas,self)
            self.layoutIlluminance.addWidget(self.toolbar)
            self.layoutIlluminance.addWidget(self.canvas)
            self.illuminanceActivated = True


        xCor = self.illData.roomgrid.uniCor['x']
        yCor = self.illData.roomgrid.uniCor['y']
        data = self.metricsData


        colorScheme = self.currentColorSchemeMetrics
        alphaVal = self.currentSpaceChartOpacityValueMetrics

        upperMask = self.metricsUpperMaskColor
        lowerMask = self.metricsLowerMaskColor

        #This replace is a quick hack for cases where Illuminance is abbreivated as Illuminance
        currentMetricsName = self.currentMetricsName.replace("Illum","Illuminance")

        gridPlot(data,xCor,yCor,currentMetricsName,"X Coordinates","Y Coordinates",
                 fullDataGrid=self.illData.roomgrid.gridMatrixLocations,figVal=self.figure,colormap=colorScheme,
                 alpha=alphaVal,colorMax=self.metricsMaxVal,colorMin=self.metricsMinVal,lowerMask=lowerMask,
                 upperMask=upperMask,plotColors=self.chkSpaceColors.checkState(),plotContours=self.chkSpaceContours.checkState(),contourValues=self.contourValuesMetrics)

        self.canvas.draw()

def main(jsonFile=None,spaceID=None,*args):

    app = QtGui.QApplication(sys.argv)

    if len(sys.argv)>=3:
        jsonFile = sys.argv[-2]
        spaceID = int(sys.argv[-1])
    else:
        jsonFile=spaceID=None

    form = Main(jsonFile=jsonFile,spaceID=spaceID)
    form.show()
    app.exec_()

if __name__ =="__main__":
     sys.argv.extend([r"C:\C-SHAP\testC.json", 0])
     # sys.argv.extend([r'E:\debug2\base2wgangsig2.json',0])
     main()
