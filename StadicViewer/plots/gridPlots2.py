

from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.figure import Figure



def gridPlot(data,xData,yData,plotTitle,xLabel,yLabel,saveName=None,colormap=None,fullDataGrid=None,figVal=None):
    """
    If fullDataGrid is provided then use that to fill up the rectangular grid.

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


    if len(data)!= xLen*yLen:
        assert len(fullDataGrid)==xLen*yLen,"The dimensions of the fullDataGrid(={}) and the dimensions of x Coordinates({}) and y Coordinates({}) do not match".format(len(fullDataGrid,xLen,yLen))
        dataForPlot = []
        for idx,values in enumerate(fullDataGrid):
            if values is not None:
                dataForPlot.append(data[values])
            else:
                dataForPlot.append(-1)
    else:
        dataForPlot = list(data)

    plotData = []
    for xIndex,xVal in enumerate(xData):
        plotDataSingle = []
        for yIndex,yVal in enumerate(yData):
            indexVal = yLen*xIndex+yIndex
            plotDataSingle.append(dataForPlot[indexVal])
        plotData.append(plotDataSingle)

    if figVal:

        fig = figVal
        fig.clf()
        ax = figVal.add_subplot(111)
    else:
        fig,ax = plt.subplots()


    x,y = np.meshgrid(yData,xData)
    plotData = np.array(plotData)

    ax.axes.set_aspect('equal')
    ax.set_xlim((min(xData),max(xData)))
    ax.set_ylim((min(yData),max(yData)))
    # ax.set_xticks(fontsize=8)
    # ax.set_yticks(fontsize=8)

    ax.set_xlabel(xLabel,labelpad=5,fontsize=9)
    ax.set_ylabel(yLabel,labelpad =5,fontsize=9)
    ax.set_title(plotTitle,fontname='Arial',y=1.02,fontsize=12)


    #Settings for color mesh.
    #For contours put colors = k for a single color
    contourValues = (50,100,200,500,1000,2000,3000,4000,5000,10000,20000)
    #The y =1.02 specifies how much far (in %) the title would be from the plt.
    CS = ax.contour(y,x,plotData,colors='k',vmin=0,vmax=5000,levels=(50,100,200,500,1000,2000,3000,4000,5000))
    ax.clabel(CS,inline=1,fontsize=8,v=contourValues)


    #Settings for colormesh
    cmapVal = plt.cm.YlOrRd
    cmapVal.set_under('Gray')
    cax = ax.pcolormesh(y,x,plotData,cmap=cmapVal,vmin=1,vmax=5000)


    #If the plot is too wide then place the color bar horizontally else keep it vertical.
    if xLen>1.3*yLen:
        orientationValue = 'horizontal'
    else:
        orientationValue = 'vertical'
    # plt.colorbar(orientation=orientationValue)
    fig.colorbar(cax,orientation=orientationValue)




    if saveName:
        if os.path.exists(os.path.split(saveName)[0]):

            fig.savefig(saveName,aspect=15)

        else:
            raise IOError("The specified path {}, is not valid".format(saveName))
    else:
    # assert 0
        if __name__ == "__main__":
            plt.show()
            # fig.show()
        else:
            return fig


if __name__ == "__main__":
    from results.dayIll import Dayill
    from stadic.readStadic import StadicProject
    import matplotlib

    projectJson = r"E:\C-SHAP\testC.json"
    # projectJson = r'E:\debug2\base2wgangsig2.json'
    # projectJson = r"E:\SExample\SExample.json"
    project = StadicProject(projectJson)
    illFile = project.spaces[0].resultsFile
    ptsFile = project.spaces[0].analysisPointsFiles[0]
    illData = Dayill(illFile,ptsFile)

    xCor = illData.roomgrid.uniCor['x']
    yCor = illData.roomgrid.uniCor['y']

    print(illData.roomgrid.ptArrayXYZ)

    print(illData.roomgrid.gridMatrix)
    print(illData.roomgrid.uniCorX)
    print(illData.roomgrid.testUniformSpc)
    print(illData.roomgrid.gridSizeMax)
    print(illData.roomgrid.gridMatrixFull,len(illData.roomgrid.gridMatrixFull))
    print(illData.roomgrid.gridMatrixLocations)
    # print(illData.roomgrid.gridMatrixLocations)
    print(len(filter(lambda x:False if x is None else True,illData.roomgrid.gridMatrixLocations)))

    print(illData.roomgrid)
    ptsGrid = {}
    #
    # for xcord in xCor:
    #     for yCor in


    print(len(illData.roomgrid.ptsdict))
    print(illData.roomgrid.ptsdict[0])
    print(illData.roomgrid.ptsdict[1])
    print(illData.roomgrid.ptsdict[2])


    print(xCor,len(xCor))
    print(yCor,len(yCor))

    for hours in range(4591,4610):
        data = illData.timedata[hours]['data'].illarr
        timeStamp = illData.timedata[hours]['tstamp']
        data += [0,0,0]
        # gridPlot(data,xCor,yCor,"Illuminance Plot for {}".format(timeStamp),"X Coordinates","Y Coordinates",saveName=r'F:\contourSingle\Hour{}.png'.format(hours),fullDataGrid=illData.roomgrid.gridMatrixLocations)
        gridPlot(data,xCor,yCor,"Illuminance Plot for {}".format(timeStamp),"X Coordinates","Y Coordinates",fullDataGrid=illData.roomgrid.gridMatrixLocations)


    # thermalPlots(gridDataYearly,listDates,listHours,"Hourly Illuminance Value for (x,y) = ({},{})".format(gridVal[0],gridVal[1]),"Days of the Year","Hours")


    # print(gridDataYearly)

