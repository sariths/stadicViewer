"""
This module defines a function called heatMaps. heatMaps uses matplotlib to generate annual plots.
"""


from __future__ import print_function
from __future__ import division
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.gridspec as gridspec


def heatMaps(data,xData,yData,colormap=None,figVal=None, alpha=None,colorMax=None,colorMin=None,
             interpolationVal=None,aspectValue='equal',xLabels=None,
             xLabelFormatter=None,orientationValue=None):
    """
    :param data:
    :param xData:
    :param yData:
    :param colormap:
    :param figVal:
    :param alpha:
    :param colorMax:
    :param colorMin:
    :param interpolationVal:
    :param aspectValue:
    :param xLabels:
    :param xLabelFormatter:
    :param orientationValue:
    :return:
    """


    fig = figVal
    fig.clf()

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

        ax.set_title(dataName,fontname='Arial',y=1.02,fontsize=12)


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

        cbar = fig.colorbar(cax,orientation=orientationValue)

        #Change the fontsize and also the number of ticks!
        cbarTicks = [colorMinVal+(colorMaxVal-colorMinVal)/5*idx for idx in range(6)]
        cbar.set_ticks(cbarTicks)
        cbar.ax.tick_params(labelsize=10)


    fig.set_tight_layout(True)
    return fig

