from __future__ import  print_function

from PyQt4 import QtCore,QtGui
from vis.ui2 import Ui_Form

from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

import os,sys

# sys.path.append(r'F:\Dropbox\RadScripts')

from visuals.gridPlots import gridPlot
from visuals.heatMaps import thermalPlots

from results.dayIll import Dayill
from software.stadic.readStadic import StadicProject


class Main(QtGui.QDialog,Ui_Form):
    def __init__(self,parent=None,jsonFile=None,spaceID=None):
        super(Main,self).__init__(parent)
        self.setupUi(self)

        #Setup matplotlib inside Qt.
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        #Remove these flags later.
        self.groupBox.setVisible(False)



        self.calDateTimeIllum.dateChanged.connect(self.plotIlluminance)
        self.cmbTimeIllum.currentIndexChanged.connect(self.plotIlluminance)
        self.illuminanceActivated = False

        if jsonFile and spaceID is not None:
            self.loadJson(jsonFile,spaceID)

    def loadJson(self,jsonFileName,spaceID):
        projectJson = jsonFileName
        # projectJson = r"E:\C-SHAP\testC.json"
        # projectJson = r'E:\debug2\base2wgangsig2.json'
        # projectJson = r"E:\SExample\SExample.json"
        project = StadicProject(projectJson)
        illFile = project.spaces[0].resultsFile
        ptsFile = project.spaces[0].analysisPointsFiles[0]
        self.illData = Dayill(illFile,ptsFile)

        hourFormat = self.illData.timedata[0:24]
        hourFormat = [hourVal['tstamp'].strftime("%I:%M %p") for hourVal in hourFormat]
        self.cmbTimeIllum.clear()
        self.cmbTimeIllum.addItems(map(str,hourFormat))
        self.cmbTimeIllum.setCurrentIndex(9)

    def plotIlluminance(self):
        if not self.illuminanceActivated:
            self.toolbar = NavigationToolbar(self.canvas,self)
            self.layoutIlluminance.addWidget(self.toolbar)
            self.layoutIlluminance.addWidget(self.canvas)
            self.illuminanceActivated = True

        dateVal = self.calDateTimeIllum.dateTime().date().dayOfYear()
        hours = (dateVal-1)*24+self.cmbTimeIllum.currentIndex()
        xCor = self.illData.roomgrid.uniCor['x']
        yCor = self.illData.roomgrid.uniCor['y']
        data = self.illData.timedata[hours]['data'].illarr

        # if len(data)<len(xCor)*len(yCor):
        #     data = data + [0]*(len(xCor)*len(yCor)-len(data))

        timeStamp = self.illData.timedata[hours]['tstamp']
        timeStamp = timeStamp.strftime("%I:%M%p on %b %d")

        gridPlot(data,xCor,yCor,"Illuminance Plot for {}".format(timeStamp),"X Coordinates","Y Coordinates",fullDataGrid=self.illData.roomgrid.gridMatrixLocations,figVal=self.figure)


        self.canvas.draw()



def main(jsonFile=None,spaceID=None,*args):

    app = QtGui.QApplication(sys.argv)

    if len(sys.argv)>=3:
        jsonFile = sys.argv[-2]
        spaceID = int(sys.argv[-1])

        form = Main(jsonFile=jsonFile,spaceID=spaceID)
        form.show()
        app.exec_()

if __name__ =="__main__":
     sys.argv.extend([r"E:\C-SHAP\testC.json", 0])
     print(sys.argv)
     main()
