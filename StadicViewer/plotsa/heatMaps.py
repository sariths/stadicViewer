# -*- coding: utf-8 -*-
"""
Prototypes for thermal plots.
"""
# The color options for cmaps selected by Dr. Mistrick are None, Grey and Purple.


import matplotlib.pyplot as plt
import numpy as np
import os

def thermalPlots(data,xData,yData,plotTitle,xLabel,yLabel,saveName=None,colormap=None):
    xLen,yLen = map(len,(xData,yData))
    print(xLen,yLen)
    plotData = []
    for xIndex,xVal in enumerate(xData):
        plotDataSingle = []
        for yIndex,yVal in enumerate(yData):
            indexVal = yLen*xIndex+yIndex
            plotDataSingle.append(data[indexVal])
        plotData.append(plotDataSingle)

    fig,ax = plt.subplots()
    x,y = np.meshgrid(yData,xData)
    plotData = np.array(plotData)

    plt.axes().set_aspect(5)
    plt.xlim((min(xData),max(xData)))
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.ylim((min(yData),max(yData)))


    plt.title(plotTitle)
    plt.pcolormesh(y,x,plotData,cmap=colormap,vmin=0,vmax=5000)

        #If the plot is too wide then place the color bar horizontally else keep it vertical.
    if xLen>1.3*yLen:
        orientationValue = 'horizontal'
    else:
        orientationValue = 'vertical'
    # plt.colorbar(orientation=orientationValue)
    plt.colorbar(orientation=orientationValue)

    # plt.colorbar()

    if saveName:
        if os.path.exists(os.path.split(saveName)[0]):

            fig.savefig(saveName)

        else:
            raise IOError("The specified path {}, is not valid".format(saveName))
    else:
    # assert 0
        plt.show()


    # fig,ax = plt.subplots()
    # heatmap = plt.pcolor(plotData)
    # plt.xticks(xData)
    # plt.yticks(yData)
    # fig.savefig(r'd:\something.png')
    # print(plotData[0])
    # pass



if __name__ == "__main__":
    from results.dayIll import Dayill
    from stadic.readStadic import StadicProject
    import matplotlib
    print(matplotlib.get_backend())
    projectJson = r"E:\debug2\base2wgangsig2.json"
    project = StadicProject(projectJson)
    illFile = project.spaces[0].resultsFile
    ptsFile = project.spaces[0].analysisPointsFiles[0]
    illData = Dayill(illFile,ptsFile)

    xCor = illData.roomgrid.uniCor['x']
    yCor = illData.roomgrid.uniCor['y']

    gridIndex = 0
    gridVal = illData.roomgrid.ptArray[gridIndex]
    print("The selected location is %s"%str(gridVal))

    gridDataYearly = [timedatahour['data'].illarr[gridIndex]for timedatahour in illData.timedata]
    listDates = range(1,366)
    listHours = range(1,25)

    # thermalPlots(gridDataYearly,listDates,listHours,"Hourly Illuminance Value for (x,y) = ({},{})".format(gridVal[0],gridVal[1]),"Days of the Year","Hours")

    cmapList = ['Blues', 'BuGn', 'BuPu','GnBu', 'Greens', 'Greys', 'Oranges', 'OrRd','PuBu', 'PuBuGn', 'PuRd', 'Purples', 'RdPu','Reds', 'YlGn', 'YlGnBu', 'YlOrBr', 'YlOrRd']
    cmapList +=  ['afmhot', 'autumn', 'bone', 'cool','copper', 'gist_heat', 'gray', 'hot','pink', 'spring', 'summer', 'winter']
    cmapList += ['viridis', 'inferno', 'plasma', 'magma']
    cmapRev = [val+"_r" for val in cmapList]
    cmapList.extend(cmapRev)
    cmapList += [None]

    for colorScheme in cmapList:
        fileName = os.path.join(r'F:\colorSchemes',str(colorScheme)+'.png')
        thermalPlots(gridDataYearly,listDates,listHours,"Hourly Illuminance Value for (x,y) = ({},{})\nColor Scheme:{}".format(gridVal[0],gridVal[1],colorScheme),
                     "Days of the Year","Hours",colormap=colorScheme,saveName=fileName)

    # print(gridDataYearly)
