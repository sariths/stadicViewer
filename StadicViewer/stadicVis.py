
# coding=utf-8
from __future__ import  print_function

from PyQt4 import QtCore,QtGui

from gui.base import Base
from gui.spatial import Spatial
from gui.timeSeries import TimeSeries

import warnings
import sys

warnings.filterwarnings('ignore')

class StadicVis(Base,Spatial,TimeSeries):
    """
    The Base class sets up the Gui and also provides logic for opening a json file through a dialog.
    All the other classes define logic for separate tabs.
    """
    def __init__(self,parent=None,jsonFile=None,spaceID=None):

        Base.__init__(self,jsonFile=jsonFile,spaceID=spaceID)

        try:
            if self.dataSpaceNameSelected:
                Spatial.setupGui(self)
                TimeSeries.setupGui(self)
        except AttributeError:
            pass


    def __initializeCharts__(self):
        """
        This function is actually first defined by the base class as the
        actions for buttons are defined over there.
        :return:
        """
        Spatial.setupGui(self)
        TimeSeries.setupGui(self)


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
     # sys.argv.extend([r"C:\LF_ST\cl.json",0])
     # sys.argv.extend([r"C:\ST\Rick.json",0])
     # sys.argv.extend([r"E:\C-SHAP\testC.json", 0])
     # sys.argv.extend([r'E:\Stadic6\MG6.json',0])
     # sys.argv.extend([r"E:\SExample\SExample.json",0])
     # sys.argv.extend(([r"C:\East\HW6\HW6_Ho_Jiang.json",0]))
     # sys.argv.extend(["C:\donut\donut.json",0])
     main()
