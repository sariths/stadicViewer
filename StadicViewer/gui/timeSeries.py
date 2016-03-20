# coding=utf-8
from __future__ import  print_function

from PyQt4 import QtCore,QtGui
from StadicViewer.vis.ui4 import Ui_Form
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QT as NavigationToolbar
import warnings
import os,sys,operator


from visuals.heatMaps import thermalPlots


class TimeSeries(QtGui.QDialog, Ui_Form):
   def setupTimeSeries(self):

       self.tsFigure = Figure()
       self.tsCanvas = FigureCanvas(self.tsFigure)
       self.tsPlotsActivated = False

       self.tsToolbar = NavigationToolbar(self.tsCanvas,self)
       self.layoutTimeSeries.addWidget(self.tsToolbar)
       self.layoutTimeSeries.addWidget(self.tsCanvas)

       self.sliderTimeSeriesOpacity.valueChanged.connect(self.tsOpacitySliderChanged)

   def tsOpacitySliderChanged(self):
       self.txtTimeSeriesOpacityValue.setText(str(self.sliderTimeSeriesOpacity.value()))