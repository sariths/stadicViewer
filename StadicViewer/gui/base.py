# coding=utf-8
from __future__ import print_function

from PyQt4 import QtCore,QtGui
from vis.gui import Ui_Form
import os,sys,operator
from data.procData import VisData
from software.stadic.readStadic import StadicProject
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar

# TODO: Define a jsonobject class that will then be inherited by others

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
                if data < 0:
                    s = ''

                if len(self.mode):

                        self.set_message('%s, %s' % (self.mode, s))
                else:
                    self.set_message(s)
        else:
            self.set_message(self.mode)

    def pick_event(self,event):
        print(event.ind)

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