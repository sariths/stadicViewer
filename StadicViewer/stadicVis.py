# coding=utf-8
# coding=utf-8
from __future__ import  print_function

from PyQt4 import QtCore,QtGui
from StadicViewer.vis.ui4 import Ui_Form
from gui.spatial import Spatial
from gui.timeSeries import TimeSeries

import warnings
import os,sys,operator

class StadicVis(Spatial,TimeSeries):
    def __init__(self,parent=None,jsonFile=None,spaceID=None):

        # super(StadicVis,self).__init__(parent)
        Spatial.__init__(self,jsonFile=jsonFile,spaceID=spaceID)

        self.setupTimeSeries()


        # super(TimeSeries,self).__init__()
        # TimeSeries.__init__(self)

def main(jsonFile=None,spaceID=None,*args):

    app = QtGui.QApplication(sys.argv)

    if len(sys.argv)>=3:
        jsonFile = sys.argv[-2]
        spaceID = int(sys.argv[-1])
    else:
        jsonFile=spaceID=None

    form = StadicVis(jsonFile=jsonFile, spaceID=spaceID)
    form.show()
    app.exec_()

if __name__ =="__main__":
     sys.argv.extend([r"C:\C-SHAP\testC.json", 0])
     # sys.argv.extend([r'E:\debug2\base2wgangsig2.json',0])
     main()
