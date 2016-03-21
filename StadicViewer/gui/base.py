# coding=utf-8
from __future__ import print_function

from PyQt4 import QtCore,QtGui
from StadicViewer.vis.gui import Ui_Form
import os,sys,operator
from StadicViewer.data.procData import VisData
from software.stadic.readStadic import StadicProject
# TODO: Define a jsonobject class that will then be inherited by others


class Base(QtGui.QDialog,Ui_Form,VisData):
    """
    This class sets up the UI from the imported pyuic file.
    It also instantiates the json object that will be avilable for all the tabs.
    """
    def __init__(self,parent=None,jsonFile=None,spaceID=0):
        super(Base,self).__init__(parent)
        self.setupUi(self)
        self.defaultWindowTitle = str(self.windowTitle())


        self.btnOpenJson.clicked.connect(self.__readJson__)
        self.btnSelectSpaceName.clicked.connect(self.__loadJson__)

        if jsonFile:
            VisData.__init__(self,jsonFile,spaceID)
            self.grpFileDialog.setVisible(False)
            self.grpFileDialog.setEnabled(False)

    def __readJson__(self):
        jsonFileName = QtGui.QFileDialog.getOpenFileName(self,"Select a json file to open","C:/","Json File (*.json)")
        if jsonFileName:
            jsonFileName = str(jsonFileName)
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

    def __loadJson__(self):
        jsonFileName = str(self.txtJsonPath.text())
        spaceIndex = self.cmbSpaceName.currentIndex()
        VisData.__init__(self,jsonFileName,spaceIndex)
        self.grpFileDialog.setEnabled(False)
        self.__initializeCharts__()

    def __initializeCharts__(self):
        """
        Placeholder for function that will be called in the main class
        :return:
        """
        pass
def main():
    app = QtGui.QApplication(sys.argv)

    if len(sys.argv)>=3:
        jsonFile= sys.argv[-2]
        spaceId = int(sys.argv[-1])
    else:
        jsonFile=spaceId=None

    form = Base(jsonFile=jsonFile,spaceID=spaceId)
    form.show()
    app.exec_()

if __name__ == "__main__":
    sys.argv.extend([r"C:\C-SHAP\testC.json", 0])
    main()