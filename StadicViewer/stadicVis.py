from __future__ import  print_function

from PyQt4 import QtCore,QtGui
from vis.ui3 import Ui_Form
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import warnings
import os,sys

# sys.path.append(r'F:\Dropbox\RadScripts')

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
        self.grpContoursIlluminance.setEnabled(False)
        self.btnSpaceSettingsContour.setEnabled(False)

        #TODO: Metrics
        #TODO: Code the readStadic file to recognize metrics files.

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
        self.btnSelectColorLowerMask.clicked.connect(lambda:self.illuminanceMaskSettingsActivated(False))
        self.btnSelectColorUpperMask.clicked.connect(lambda:self.illuminanceMaskSettingsActivated(True))

        self.illuminanceMaxVal = 5000
        self.illuminanceMinVal = 1

        self.illuminanceMaxValDefault = 5000
        self.illuminanceMinValDefault = 1
        self.illuminanceUpperMaskValue = None
        self.illuminanceLowerMaskValue = None
        self.illuminanceUpperMaskColor = None
        self.illuminanceLowerMaskColor = None


        self.txtColorsMax.setText(str(self.illuminanceMaxValDefault))
        self.txtColorsMin.setText(str( self.illuminanceMinValDefault))
        self.txtColorsMax.setValidator(floatValidator)
        self.txtColorsMin.setValidator(floatValidator)

        self.btnSpaceResetColors.clicked.connect(self.resetColorSettings)
        self.btnSpaceSetColors.clicked.connect(self.setColorSettings)


        self.chkSpaceColors.clicked.connect(self.plotIlluminance)
        self.plotIlluminanceColors = True


        #settings for contour values for the illuminance plot.
        self.cmbSpaceContourQuantity.currentIndexChanged.connect(self.setContourQuantity)
        #Put all contourboxes inside a list for easy iteration.
        self.contourBoxes = [self.txtSpaceCountourValue1,self.txtSpaceCountourValue2,self.txtSpaceCountourValue3,self.txtSpaceCountourValue4,
                             self.txtSpaceCountourValue5,self.txtSpaceCountourValue6,self.txtSpaceCountourValue7]

        for contourBox in self.contourBoxes:
            contourBox.setValidator(floatValidator)

        self.chkSpaceContours.clicked.connect(self.plotIlluminance)

        #chartScheme Settings

        #Contstuctor Stuff
        colorMapTuple = (('Uniform01','viridis'),('Uniform02','inferno'),('Uniform03','plasma'),('Uniform04','magma'),('Blues','Blues'),
                        ('BlueGreen','BuGn'),('BluePurple','BuPu'),('GreenBlue','GnBu'),('Greens','Greens'),('Greys','Greys'),('Oranges','Oranges'),
                        ('OrangeRed','OrRd'),('PurpleBlue','PuBu'),('PurpleBlueGreen','PuBuGn'),('PurpleRed','PuRd'),('Purples','Purples'),
                        ('RedPurple','RdPu'),('Reds','Reds'),('YellowGreen','YlGn'),('YellowGreenBlue','YlGnBu'),('YellowOrangeBrown','YlOrBr'),
                        ('YellowOrangeRed','YlOrRd'),('Hot01','afmhot'),('Hot02','hot'),('Hot03','gist_heat'),('Autumn','autumn'),('Bone','bone'),('Cool','cool'),
                        ('Copper','copper'),('Spring','spring'),('Summer','summer'),('Winter','winter'))

        colorNames = [name for name,plotName in colorMapTuple]
        self.colorDict =dict(colorMapTuple)
        self.cmbSpaceColorScheme.addItems(colorNames)
        self.cmbSpaceColorScheme.setCurrentIndex(21)
        self.currentColorScheme = 'YlOrRd'
        self.currentSpaceChartOpacityValue = 1
        self.btnSpaceSetColorScheme.clicked.connect(self.assignSpaceColorScheme)


        self.txtSpaceStatusDisplay.setEnabled(False)


        #Open json file settings.
        self.btnOpenJson.clicked.connect(self.openJsonFileDirectly)
        self.btnSelectSpaceName.clicked.connect(self.loadVisualsFromOpenedJsonFile)

        self.btnSapceSelectFileTypeIlluminance.clicked.connect(self.loadDifferentIlluminanceFile)

        if jsonFile and spaceID is not None:
            self.jsonFile = jsonFile
            self.grpFileDialog.setEnabled(False)
            self.tabWidget.setEnabled(True)
            self.loadJson(jsonFile,spaceID)

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
        self.currentColorScheme = currentColor

        self.currentSpaceChartOpacityValue = self.sliderSpaceOpacity.value()/100.0

        # TODO:Change this to mean all plots later.
        self.plotIlluminance()


    def setContourQuantity(self):
        contourQuantity = int(self.cmbSpaceContourQuantity.currentText())
        for idx,contourBoxes in enumerate(self.contourBoxes):
            if (idx+2-1)>contourQuantity:
                contourBoxes.clear()
                contourBoxes.setEnabled(False)
            else:
                contourBoxes.setEnabled(True)


    def illuminanceMaskSettingsActivated(self,isUpperMask):
        colorDialog = QtGui.QColorDialog
        selectedColor = colorDialog.getColor()

        if selectedColor.isValid():
            selectedColor = selectedColor.getRgb()
            if isUpperMask:
                self.txtColorsUpperMask.setStyleSheet("background-color: rgb{}".format(selectedColor))
                self.illuminanceUpperMaskColor = selectedColor
            else:
                self.txtColorsLowerMask.setStyleSheet("background-color: rgb{}".format(selectedColor))
                self.illuminanceLowerMaskColor = selectedColor

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

    def resetColorSettings(self):
        self.txtColorsMax.setText(str(self.illuminanceMaxValDefault))
        self.txtColorsMin.setText(str (self.illuminanceMinValDefault))
        self.txtColorsLowerMask.setStyleSheet("")
        self.txtColorsUpperMask.setStyleSheet("")
        self.txtColorsUpperMask.clear()
        self.txtColorsUpperMask.setEnabled(False)
        self.txtColorsUpperMask.setPlaceholderText('')
        self.txtColorsLowerMask.clear()
        self.txtColorsLowerMask.setEnabled(False)
        self.txtColorsLowerMask.setPlaceholderText('')
        self.illuminanceLowerMaskColor = None
        self.illuminanceUpperMaskColor = None



        self.illuminanceMaxVal = float(self.txtColorsMax.text())
        self.illuminanceMinVal = float(self.txtColorsMin.text())

        self.plotIlluminance()


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
        # print(project.spaces[spaceID].log)



        illFilesExisting = [(fileKey,fileName) for fileKey,fileName in self.allFilesDict.items() if fileName]
        illFilesOnly = [fileKey for fileKey,fileName in illFilesExisting if fileName.endswith('.ill') and fileName != illFile]
        mainIllFile = [fileKey for fileKey,fileName in illFilesExisting if fileName.endswith('.ill') and fileName == illFile]

        illFilesOnly = mainIllFile + sorted(illFilesOnly)
        self.cmbSpaceSelectIlluminanceFile.clear()
        self.cmbSpaceSelectIlluminanceFile.addItems(illFilesOnly)

        self.ptsFile = ptsFile
        self.illData = Dayill(illFile,ptsFile)
        self.txtSpaceStatusDisplay.setText("Current space: {} \tCurrent data set: {}.\t Source:{}".format(self.spaceName,mainIllFile[0],illFile))


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

        gridPlot(data,xCor,yCor,"Illuminance Plot for {}".format(timeStamp),"X Coordinates","Y Coordinates",
                 fullDataGrid=self.illData.roomgrid.gridMatrixLocations,figVal=self.figure,colormap=colorScheme,
                 alpha=alphaVal,colorMax=self.illuminanceMaxVal,colorMin=self.illuminanceMinVal,lowerMask=lowerMask,
                 upperMask=upperMask,plotColors=self.chkSpaceColors.checkState(),plotContours=self.chkSpaceContours.checkState())

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
     # sys.argv.extend([r"E:\C-SHAP\testC.json", 0])
     main()
