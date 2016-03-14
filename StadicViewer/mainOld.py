from __future__ import print_function
from  __future__ import division

import sys
import os
import time

from stadic.readStadic import StadicProject
from results.pts import RoomGrid
from results.dayIll import Dayill
import itertools
import operator
print(time.ctime())

def getData(jsonFile,spaceId):


    project = StadicProject(jsonFile)
    space = project.spaces[spaceId]
    # print(space.resultsFile)
    daylight = Dayill(space.resultsFile,space.analysisPointsFiles[0])
    print(daylight.roomgrid)
    print(space.analysisPointsFiles[0])
    print(space.filesDict.items())
    # illDict = {}
    # counter = 0
    for fileDescr,fileName in space.filesDict.items():
        print(fileDescr,":",fileName)
        # if fileName.endswith(".ill") and "Direct" in fileDescr:
        #     counter += 1
        #     illDict[counter]=Dayill(fileName,space.analysisPointsFiles[0])
        #     print(fileDescr,":",fileName)
    # print(counter)


    print("*~"*50)
    # wg1File = space.windowGroups[0].fileBase
    # wg1FileDirect = space.windowGroups[0].fileBaseDirect
    # print(wg1FileDirect)
    # daylight = Dayill(wg1File,space.analysisPointsFiles[0])
    # # daylight = Dayill(space.resultsFile,space.analysisPointsFiles[0])
    #
    # # print(daylight.roomgrid)
    # # print(daylight.max_ill)
    # for lines in daylight.illLimits(verbose=True,maxval=1000,percent=True):
    #     print(lines)

    # daylight.metricSDA()
    print(time.ctime())
def tryCombinations(jsonFile,spaceID):
    project = StadicProject(jsonFile)
    space = project.spaces[spaceID]

    illDict = {}
    counter = 0


    for fileDescr,fileName in space.filesDict.items():

        if fileName.endswith(".ill") and "Direct" in fileDescr and 'set' not in fileDescr.lower():
            print('using',fileDescr)
            illDict[counter]=Dayill(fileName,space.analysisPointsFiles[0])
            counter += 1

    print(illDict)
    combinationQuant = range(len(illDict))
    combinations = []
    for L in range(0, len(illDict)+1):
        for subset in itertools.combinations(combinationQuant, L):
            combinations.append(subset)

    print(len(combinations))

    with open(r'e:\test.txt','w')as somefile:
        counter = 0
        for idx,dataVal in enumerate(illDict[0].timedata):
            comboVal = []
            for combo in combinations:
                if combo:
                    startList = [0]*len(dataVal['data'].illarr)
                    for key,val in illDict.items():
                        if key in combo:
                            startList = map(operator.add,startList,illDict[key].timedata[idx]['data'].illarr)
                    percent = len([pt for pt in startList if pt>1000])/len(startList)

                    comboVal.append((percent,combo))
                    counter +=1
            print(comboVal,file=somefile)

    print(counter)
        # print(dataVal['data'].illarr)

    print(time.ctime())

if __name__ == "__main__":
    # getData(r"E:\debug2\base2wgangsig2.json",0)
    getData(r"E:\C-SHAP\testC.json",0)