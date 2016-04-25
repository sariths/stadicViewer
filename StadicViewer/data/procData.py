# coding=utf-8
"""
    Contains a class to process data files.
"""

from __future__ import print_function

from results.dayIll import Dayill
from software.stadic.readStadic import StadicProject

class VisData(object):
    def __init__(self,fileName=None,spaceIndex=0):


        self.dataJsonFileName = fileName


        self.dataAllFiles = {} #List all possible files.

        self.dataAllFilesAvailable = {} #Filter all the available files, ie the ones that are not None.

        self.dataDayIllFilesList = []  #FileKey,FileName tuples for all the daylight ill files. The main ill file will be on the top of this list.
        self.dataMetricsFilesList = [] #Similar list for metrics files.
        self.dataSignalsFilesList = [] #Similar for signals files
        self.dataScheduleFilesList = []
        self.dataSettingsFilesList = [] #These files end with .sch and can be files such as shade settings files etc.

        self.dataTimeSeriesLists =[] #These are tuples which contain keys,8760lists of data.

        self.dataWindowGroupNames = None

        self.dataPtsFile =None
        self.dataProject = None
        self.dataSpaceNames = []
        self.dataSpaceNameSelected = []

        self.dataLog = None

        if fileName:
            if fileName.lower().endswith(".json"):
                self.dataLoadJson(fileName, spaceIndex)
            elif fileName.lower().endswith(".hea"):
                pass #Add code for daysim header files later if needed.


    def dataLoadJson(self, fileName, spaceIndex):
        """
        Extract info from json files.

        :param fileName:
        :param spaceIndex:
        :return:
        """
        project = StadicProject(fileName)
        self.dataProject = project

        self.dataSpaceIndex = spaceIndex

        self.dataPtsFile =  project.spaces[spaceIndex].analysisPointsFiles[0]
        self.dataSpaceNames = [project.spaces[idx].spaceName for idx, space in enumerate(project.spaces)]
        self.dataSpaceNameSelected = self.dataSpaceNames[spaceIndex]
        self.dataSpaceNamesDict = project.spaces[spaceIndex].namesDict


        self.dataAllFiles = project.spaces[spaceIndex].filesDict
        self.dataAllFilesAvailable  = dict([(fileKey, fileName) for fileKey, fileName in self.dataAllFiles.items() if fileName])


        mainIllFile = project.spaces[spaceIndex].resultsFile


        self.dataDayIllFilesList = [(fileKey, fileName) for fileKey, fileName in self.dataAllFilesAvailable.items() if fileName.lower().endswith(".ill")
                                    and fileName != mainIllFile
                                    and 'electric zone' not in fileKey.lower()]

        self.dataElectricIllFilesList = [(fileKey,fileName) for fileKey,fileName in self.dataAllFilesAvailable.items() if 'electric zone' in fileKey.lower()]


        if mainIllFile: #If the main illuminance file exists, insert it at 0 position.
            self.dataDayIllFilesList.insert(0, ("Main Illuminance File", mainIllFile))


        fileFilter = lambda dataDict,extension:[(fileKey,fileName) for fileKey,fileName in dataDict.items() if fileName.lower().endswith(extension)]

        self.dataMetricsFilesList = fileFilter(self.dataAllFilesAvailable, '.res')
        self.dataSignalsFilesList = fileFilter(self.dataAllFilesAvailable, '.sig')
        self.dataScheduleFilesList = fileFilter(self.dataAllFilesAvailable, '.csv')
        self.dataSettingsFilesList = fileFilter(self.dataAllFilesAvailable, '.sch')

        self.dataWindowGroupNames = [group.name for group in project.spaces[spaceIndex].windowGroups]


        self.dataTimeSeriesLists = self.dataExtractTimeSeriesData(self.dataSignalsFilesList + self.dataScheduleFilesList + self.dataSettingsFilesList)

        self.dataLog = project.spaces[0].log
        #TODO: Implement a lookup dictionary for years.
        dataYearFirstDayDict = {4:2015,3:2014,2:2013,6:2011,5:2010,1:2007,7:2006}
        dataFirstDay = self.dataProject.firstDay
        self.dataYear = dataYearFirstDayDict[dataFirstDay]


    def dataExtractTimeSeriesData(self, lists):
        listData = []
        windowGroupQuant = len(self.dataWindowGroupNames)
        for keyVal,fileName in lists:
            data = []
            with open(fileName)as dataFile:
                if fileName.lower().endswith('.csv'):
                    for lines in dataFile:
                        lineSplit = lines.split(',')
                        dataValue = float(lineSplit[-1])
                        data.append(dataValue)
                    listData.append((keyVal,data))

                elif fileName.lower().endswith('.sig'):
                    for lines in dataFile:
                        lineSplit = lines.split()
                        dataValue = float(lineSplit[-1])
                        data.append(dataValue)
                    listData.append((keyVal,data))

                elif fileName.lower().endswith(".sch"):
                    #Need to all this below becauase sch files are of the format Month Date Time 'SetWindowGroup1' 'SetWindowGroup2'....'SetWindowGroupN'
                    for lines in dataFile:
                        lineSplit = lines.split()
                        dataValue = map(float,lineSplit[-windowGroupQuant:])
                        data.append(dataValue)
                    data = (zip(*data))
                    for idx,value in enumerate(data):
                        windowGroupName = "Shade Set., Win.Group: "+self.dataWindowGroupNames[idx]
                        listData.append((windowGroupName,value))




        return listData
        # for fileKey,fileName in self.allFiles.items():
        #     print(fileKey,fileName)

    def dataExtractTimeSeriesIlluminanceData(self, fileName, location):
        """
        The location refers to the location on the pts file.
        """
        illData = []
        if fileName:
            with open(fileName)as illFile:
                for lines in illFile:
                    lineSplit = lines.split()[3:]
                    illData.append( float(lineSplit[location]))
            illData
        else:
            illData= [None]*8760

        return illData
if __name__ == "__main__":
    file1 = r"E:\C-SHAP\testC.json"
    file2= r"E:\SExample\SExample.json"
    vis = VisData(fileName=file1)
