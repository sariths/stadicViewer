

from __future__ import print_function
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.cm import get_cmap
from matplotlib.figure import Figure
import  matplotlib.dates as mdates


def gridPlot(data,xData,yData,plotTitle,xLabel,yLabel,saveName=None,colormap=None,fullDataGrid=None,figVal=None,alpha=None,lowerMask=None,
             upperMask=None,colorMax=None,colorMin=None,plotColors=None,plotContours=None,contourValues=None,interpolationVal=None,
             aspectValue='equal',xLabels=None,yLabels=None,xLabelFormatter=None,yLabelFormatter=None,layoutFormat=111,
             orientationValue=None):
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



    xData,yData = map(list,(xData,yData))
    xmin,xmax,ymin,ymax = min(xData),max(xData),min(yData),max(yData)


    xLen,yLen = map(len,(xData,yData))


    if len(data)!= xLen*yLen:
        assert len(fullDataGrid)==xLen*yLen,"The dimensions of the fullDataGrid(={}) and the dimensions of x Coordinates({}) and y Coordinates({}) do not match".format(len(fullDataGrid,xLen,yLen))
        dataForPlot = []
        for idx,values in enumerate(fullDataGrid):
            if values is not None:
                dataForPlot.append(data[values])
            else:
                dataForPlot.append(np.NaN)
    else:
        dataForPlot = list(data)

    plotDataOriginal = []
    for xIndex,xVal in enumerate(xData):
        plotDataSingle = []
        for yIndex,yVal in enumerate(yData):
            indexVal = yLen*xIndex+yIndex
            plotDataSingle.append(dataForPlot[indexVal])
        plotDataOriginal.append(plotDataSingle)




    if figVal:

        fig = figVal
        fig.clf()
        ax = figVal.add_subplot(layoutFormat)

    else:
        fig,ax = plt.subplots()


    x,y = np.meshgrid(yData,xData)

    plotData = np.array(plotDataOriginal)

    ax.axes.set_aspect('equal')
    ax.set_xlim((min(xData),max(xData)))
    ax.set_ylim((min(yData),max(yData)))
    # ax.set_xticks(fontsize=8)
    # ax.set_yticks(fontsize=8)

    ax.set_xlabel(xLabel,labelpad=5,fontsize=9)
    ax.set_ylabel(yLabel,labelpad =5,fontsize=9)
    ax.set_title(plotTitle,fontname='Arial',y=1.02,fontsize=12)


    if plotContours:
        #Settings for color mesh.
        #For contours put colors = k for a single color
        if not contourValues:
            contourValues = (50,100,200,500,1000,2000,3000,4000,5000)
        #The y =1.02 specifies how much far (in %) the title would be from the plt.
        CS = ax.contour(y,x,plotData,colors='k',vmin=0,vmax=5000,levels=contourValues,
                        hold='on')
        ax.clabel(CS,inline=1,fontsize=8,v=contourValues)


    if plotColors:

        xData += [xData[-1]+(xData[-1]-xData[-2])]
        yData += [yData[-1]+(yData[-1]-yData[-2])]

        x,y = np.meshgrid(yData,xData)
        #Settings for colormesh
        if not colormap:
            cmapVal = plt.cm.YlOrRd
            cmapVal.set_under((.753,.753,.753))
        else:
            cmapVal = colormap


        plotDataVal = np.transpose(plotData)
        # cax = ax.pcolormesh(y,x,plotData,cmap=cmapVal,vmin=colorMin,vmax=colorMax,alpha=alpha,aspect=aspectValue)
        #for imshow add : interpolation = 'nearest'
        cax = ax.imshow(plotDataVal,extent=[xmin,xmax,ymax,ymin],cmap=cmapVal,vmin=colorMin,vmax=colorMax,alpha=alpha,aspect=aspectValue,interpolation=interpolationVal)

        if xLabels and xLabelFormatter:
            ax.xaxis.set_major_locator(xLabels)
            ax.xaxis.set_major_formatter(xLabelFormatter)

        # if yLabels and yLabelFormatter:
        if yLabels:
            ax.set_yticklabels(('00:30','01:30','02:30','03:30','04:30',
                                '05:30','06:30','07:30','08:30','09:30',
                                '10:30', '11:30', '12:30', '13:30', '14:30',
                                '15:30', '16:30', '17:30', '18:30', '19:30',
                                '20:30','21:30','22:30','23:30'
                                ))
            ax.set_yticks(range(1,25,4))
            # ax.yaxis.set_major_formatter(yLabelFormatter)

        cax.cmap.set_bad((0.753,0.753,0.753))
        if not lowerMask:
            cax.cmap.set_under((0.753,0.753,0.753))
        else:
            r,g,b,a = lowerMask
            r,g,b = r/255,g/255,b/255
            cax.cmap.set_under((r,g,b))

        if upperMask:

            r,g,b,a = upperMask
            r,g,b = r/255,g/255,b/255
            cax.cmap.set_over((r,g,b))
        else:
            cmap = get_cmap(cmapVal) #Had to do this because None value does not seem to work.
            cax.cmap.set_over(cmap(1.0))
        #If the plot is too wide then place the color bar horizontally else keep it vertical.
        if not orientationValue:
            if xLen>1.3*yLen:
                orientationValue = 'horizontal'
            else:
                orientationValue = 'vertical'
            # plt.colorbar(orientation=orientationValue)
        fig.colorbar(cax,orientation=orientationValue)


    # im = ax.imshow(plotDataOriginal,extent=[xmin,xmax,ymax,ymin],interpolation='nearest')

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
        # data += [0,0,0]
        # gridPlot(data,xCor,yCor,"Illuminance Plot for {}".format(timeStamp),"X Coordinates","Y Coordinates",saveName=r'F:\contourSingle\Hour{}.png'.format(hours),fullDataGrid=illData.roomgrid.gridMatrixLocations)
        gridPlot(data,xCor,yCor,"Illuminance Plot for {}".format(timeStamp),"X Coordinates","Y Coordinates",fullDataGrid=illData.roomgrid.gridMatrixLocations)


    # thermalPlots(gridDataYearly,listDates,listHours,"Hourly Illuminance Value for (x,y) = ({},{})".format(gridVal[0],gridVal[1]),"Days of the Year","Hours")


    # print(gridDataYearly)

