# coding=utf-8
from __future__ import print_function

from PyQt4 import QtCore,QtGui
from StadicViewer.vis.ui4 import Ui_Form
import os,sys,operator

# TODO: Define a jsonobject class that will then be inherited by others


class Base(QtGui.QDialog,Ui_Form):
    def __init__(self,parent=None,jsonFile=None,spaceID=None):
        super(Base,self).__init__(parent)
        self.setupUi(self)

def main():
    app = QtGui.QApplication(sys.argv)
    form = Base()
    form.show()
    app.exec_()

if __name__ == "__main__":
    main()