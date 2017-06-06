# coding=utf-8

"""
This is the base script for launching the STADIC readStadicData visualization software.
"""

from __future__ import  print_function

from PyQt4 import QtGui

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
    #If this file is being compiled into an executable, then only the main() command should be left below this space.
    #For troubleshooting, see Note 1 below.

     #Note1: Uncomment the sys.argv statement below to launch a project directly. It is assumed that his project is
    # already present on the disc. If not, it can be copied from the testProjects directory on to the C: drive.

     sys.argv.extend([r"C:\example1\Mistrick_Stadic_Example.json",0])

     main()
