__author__ = 'Sarith'

import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.figure import Figure

def gridPlot(data,xData,yData,plotTitle,xLabel,yLabel,saveName=None,colormap=None):
    """

    :param data:
    :param xData:
    :param yData:
    :param plotTitle:
    :param xLabel:
    :param yLabel:
    :param saveName:
    :param colormap:
    :return:
    """
    xLen,yLen = map(len,(xData,yData))

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

    plt.xlim((min(xData),max(xData)))
    plt.xlabel(xLabel)
    plt.ylabel(yLabel)
    plt.ylim((min(yData),max(yData)))

    #For contours put colors = k for a single color
    plt.title(plotTitle)
    CS = plt.contour(y,x,plotData,colors='k',vmin=0,vmax=5000)
    plt.clabel(CS,inline=1,fontsize=10)
    plt.pcolormesh(y,x,plotData,cmap='YlOrBr',vmin=0,vmax=5000)

    plt.colorbar()

    if saveName:
        if os.path.exists(os.path.split(saveName)[0]):

            fig.savefig(saveName)

        else:
            raise IOError("The specified path {}, is not valid".format(saveName))
    else:
    # assert 0
        plt.show()


if __name__ == "__main__":
    from results.dayIll import Dayill
    from stadic.readStadic import StadicProject
    import matplotlib

    projectJson = r"E:\debug2\base2wgangsig2.json"
    project = StadicProject(projectJson)
    illFile = project.spaces[0].resultsFile
    ptsFile = project.spaces[0].analysisPointsFiles[0]
    illData = Dayill(illFile,ptsFile)

    xCor = illData.roomgrid.uniCor['x']
    yCor = illData.roomgrid.uniCor['y']

    for hours in range(8,17):
        data = illData.timedata[hours]['data'].illarr
        timeStamp = illData.timedata[hours]['tstamp']
        data += [0,0,0]
        gridPlot(data,xCor,yCor,"Illuminance Plot for {}".format(timeStamp),"X Coordinates","Y Coordinates",saveName=r'F:\contourSingle\Hour{}.png'.format(hours))


    # thermalPlots(gridDataYearly,listDates,listHours,"Hourly Illuminance Value for (x,y) = ({},{})".format(gridVal[0],gridVal[1]),"Days of the Year","Hours")


    # print(gridDataYearly)

