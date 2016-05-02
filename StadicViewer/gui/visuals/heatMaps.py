

from __future__ import print_function
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.cm import get_cmap
from matplotlib.figure import Figure
import  matplotlib.dates as mdates
import matplotlib.gridspec as gridspec


def heatMaps(data,xData,yData,plotTitle=None,xLabel=None,yLabel=None,
             colormap=None,figVal=None, alpha=None,colorMax=None,colorMin=None,
             interpolationVal=None,aspectValue='equal',xLabels=None,yLabels=None,
             xLabelFormatter=None,yLabelFormatter=None,layoutFormat=111,
             orientationValue=None):
    """
    If fullDataGrid is provided then use that to fill up the rectangular grid.

    """



    fig = figVal
    fig.clf()

    # if len(data)==1:
    #     fig.set_figheight(3)
    # else:
    #     fig.set_figheight(8)


    xData, yData = map(list, (xData, yData))
    xmin, xmax, ymin, ymax = min(xData), max(xData), min(yData), max(yData)

    xLen, yLen = map(len, (xData, yData))

    layoutFormat = len(data)*100
    if len(data)==1:
        gs = gridspec.GridSpec(4, 1)
    else:
        gs = gridspec.GridSpec(len(data), 1)
    for idx,(dataName,dataSet) in enumerate(data):

        if len(data)==1:
        # ax = figVal.add_subplot(layoutFormat+idx+11)
            ax = figVal.add_subplot(gs[1:3])
        else:
            ax = figVal.add_subplot(gs[idx])
        dataForPlot = list(dataSet)

        plotDataOriginal = []


        for xIndex,xVal in enumerate(xData):
            plotDataSingle = []
            for yIndex,yVal in enumerate(yData):
                indexVal = yLen*xIndex+yIndex
                plotDataSingle.append(dataForPlot[indexVal])
            plotDataOriginal.append(plotDataSingle)


        plotData = np.array(plotDataOriginal)


        ax.set_xlim((min(xData),max(xData)))
        ax.set_ylim((min(yData),max(yData)))



        # ax.set_xlabel(xLabel,labelpad=5,fontsize=9)
        # ax.set_ylabel(yLabel,labelpad =5,fontsize=9)
        ax.set_title(dataName,fontname='Arial',y=1.02,fontsize=12)


        # xData += [xData[-1]+(xData[-1]-xData[-2])]
        # yData += [yData[-1]+(yData[-1]-yData[-2])]

        #Settings for colormesh
        if not colormap:
            cmapVal = plt.cm.YlOrRd
            cmapVal.set_under((.753,.753,.753))
        else:
            cmapVal = colormap


        plotDataVal = np.transpose(plotData)


        colorMaxVal = colorMax[idx]
        colorMinVal = colorMin[idx]
        cax = ax.imshow(plotDataVal,extent=[xmin,xmax,ymax,ymin],cmap=cmapVal,
                        vmin=colorMinVal,vmax=colorMaxVal,alpha=alpha,aspect=aspectValue,
                        interpolation=interpolationVal)

        if xLabels and xLabelFormatter:
            ax.xaxis.set_major_locator(xLabels)
            ax.xaxis.set_major_formatter(xLabelFormatter)
            ax.xaxis.set_tick_params(labelsize=10)
        # if yLabels and yLabelFormatter:
        # if yLabels:
        # hourVal = ('00:30','01:30','02:30','03:30','04:30',
        #                     '05:30','06:30','07:30','08:30','09:30',
        #                     '10:30', '11:30', '12:30', '13:30', '14:30',
        #                     '15:30', '16:30', '17:30', '18:30', '19:30',
        #                     '20:30','21:30','22:30','23:30'
        #                     )
        # hourVal = ('00:30','05:30','11:30', '17:30','23:30')

        # ax.set_yticks(range(0,24,4))
        # ax.set_yticklabels(hourVal)

        # ax.yaxis.set_major_formatter(yLabelFormatter)
        cbar = fig.colorbar(cax,orientation=orientationValue)

        #Change the fontsize and also the number of ticks!
        cbarTicks = [colorMinVal+(colorMaxVal-colorMinVal)/5*idx for idx in range(6)]
        cbar.set_ticks(cbarTicks)
        cbar.ax.tick_params(labelsize=10)


    fig.set_tight_layout(True)
    return fig

