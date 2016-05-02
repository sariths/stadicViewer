# coding=utf-8
"""
Contains code for parsing a stadic json file.

StadicProject is the main class, generated once for every STADIC json file. It can contain one or more __StadicSpace__s

"""
import json
import os


def fixPaths(details, spaceDirectory, subDirectory=None, fileName=None):
    """

    :param details:
    :param spaceDirectory:
    :param subDirectory:
    :param fileName:
    :return:
    """
    if subDirectory:
        if not os.path.isabs(subDirectory):
            finalPath = os.path.join(spaceDirectory,subDirectory)
        else:
            finalPath = subDirectory
    else:
        finalPath = spaceDirectory

    if fileName:
        if not os.path.isabs(fileName):
            finalPath = os.path.join(finalPath,fileName)
        else:
            finalPath = fileName

    if os.path.exists(finalPath):
        confirmationString = "The {} is located in {}".format(details,finalPath)
    else:

        confirmationString = "The {} was NOT found  in {}".format(details,finalPath)
        finalPath = None

    return finalPath,confirmationString




class __StadicSpace__:

    def __init__(self,spaceDict,illumUnit):
        self.spaceName = spaceDict['space_name']
        spaceDirectory = spaceDict['space_directory']
        self.directorySpace,directorySpaceExists = fixPaths('Space Directory', spaceDict['space_directory'])
        self.log = directorySpaceExists

        self.directoryResults,directoryResultsExists = fixPaths('Results Directory',spaceDirectory,spaceDict['results_directory'])
        self.log += "\n"+directoryResultsExists

        finalResultsIll = os.path.join(self.directoryResults,self.spaceName+".ill")
        finalResultsIll,finalResultsExists = fixPaths("Ill File",self.directorySpace,None,finalResultsIll)

        self.resultsFile = finalResultsIll

        #create a dictionary to list all the possible files that can be used for visualization.
        filesDict = {"Main Illuminance File":finalResultsIll}

        #Update 24th April 2016: This dictionary will store proper names for
        #   data sets which can be used for Chart titles etc.
        #   For example: UDI: Useful Daylight Illuminance between 200 and 300 lux
        namesDict = {}

        self.directoryInput,directoryInputExists = fixPaths('Input Directory',spaceDirectory,spaceDict['input_directory'])
        self.log += "\n"+directoryInputExists

        self.directoryIES,directoryIesExists = fixPaths('IES Directory',spaceDirectory,spaceDict['ies_directory'])
        self.log += "\n"+directoryIesExists

        self.directoryGeometry,directoryGeometryExists = fixPaths('Geometry Directory',spaceDirectory,spaceDict['geometry_directory'])
        self.log += "\n"+directoryGeometryExists

        self.fileGeometry,fileGeometryExists = fixPaths('Geometry File',spaceDirectory,self.directoryGeometry,spaceDict['geometry_file'])
        self.log += "\n"+fileGeometryExists

        self.fileMaterials,fileMaterialsExists = fixPaths('Materials File',spaceDirectory,self.directoryGeometry,spaceDict['material_file'])
        self.log += "\n"+fileMaterialsExists



        self.scheduleLighting,fileLightingScheduleExists = fixPaths('Lighting Schedule',spaceDirectory,self.directoryInput,spaceDict['lighting_schedule'])
        self.log += "\n"+fileLightingScheduleExists

        self.scheduleOccupancy,fileOccupancyScheduleExists = fixPaths('Lighting Schedule',spaceDirectory,self.directoryInput,spaceDict['occupancy_schedule'])
        self.log += "\n"+fileOccupancyScheduleExists

        filesDict['Lighting Schedule']= self.scheduleLighting
        filesDict['Occupancy Schedule']=self.scheduleOccupancy

        self.analysisPoints = self.__StadicAnalysisPoints(spaceDict['analysis_points'])
        pointsFiles = self.analysisPoints.files
        pointsFiles = [fixPaths('Analysis Points File ({})'.format(idx+1),spaceDirectory,self.directoryInput,pointsFile)for idx,pointsFile in enumerate(pointsFiles)]
        pointsFiles,filesPointsExists = zip(*pointsFiles)
        self.analysisPointsFiles = pointsFiles

        filesPointsExists = "\n".join(filesPointsExists)
        self.log += "\n"+filesPointsExists


        self.windowGroups = [self.__StadicWindowGroups(self.spaceName,self.directorySpace,self.directoryResults,windowGroup)for windowGroup in spaceDict['window_groups']]


        for windowGroup in self.windowGroups:
            filesDict.update(windowGroup.filesDict)
            self.log += windowGroup.log

        self.targetIlluminance = spaceDict['target_illuminance']


        self.metricsDA = self.__StadicMetricsDA(spaceDict['DA'])
        self.metricsCDA =  self.__StadicMetricsCDA(spaceDict['cDA'])
        self.metricsUDI = self.__StadicMetricsUDI(spaceDict['UDI'])
        self.metricsSDA = self.__StadicMetricsSDA(spaceDict['sDA'])
        self.metricsDF = spaceDict['DF']
        self.metricsOccupiedSDA = self.__StadicMetricsOccupiedSDA(spaceDict['occupied_sDA'])



        #Note that there are no fileNames specified for results file inside the STADIC json file.So, I am going to create the fileNames myself.
        metricsFileDa = self.spaceName+"_"+"DA.res"
        metricsFileCda = self.spaceName+"_"+"cDA.res"
        metricsFileDf = self.spaceName+"_"+"DF.res"
        metricsFileOccupiedSda = self.spaceName+"_"+"occupied_sDA.res"
        metricsFileUdiAbove = self.spaceName+"_"+"above_UDI.res"
        metricsFileUdiBelow = self.spaceName+"_"+"below_UDI.res"
        metricsFileUdi = self.spaceName +"_"+"UDI.res"
        metricsFileSDA = self.spaceName + "_"+"sDA.res"


        self.metricsFileDa,metricsFileDaExists = fixPaths("Daylight Autonomy Results File",spaceDirectory,self.directoryResults,metricsFileDa)
        filesDict["Metric: DA"]=self.metricsFileDa
        namesDict["Metric: DA"]= "Daylight Autonomy at %s %s"%(self.metricsDA.illuminance,illumUnit)
        self.log += "\n"+metricsFileDaExists

        self.metricsFilesDA,metricsFilesDAExists = fixPaths("Spatial Daylight Autonomy Results File",spaceDirectory,self.directoryResults,metricsFileSDA)
        filesDict["Metric: sDA"]=self.metricsFilesDA
        namesDict["Metric: sDA"]= \
            "Spatial Daylight Autonomy at %s %s\n " \
            "Start Time: %s, End Time: %s, Fraction:%s"%\
            (self.metricsDA.illuminance,illumUnit,self.metricsSDA.startTime,self.metricsSDA.endTime,self.metricsSDA.DAFraction)
        self.log += "\n"+metricsFileDaExists

        self.metricsFileCda,metricsFileCdaExists = fixPaths("Continuous Daylight Autonomy Results File",spaceDirectory,self.directoryResults,metricsFileCda)
        filesDict["Metric: cDA"]=self.metricsFileCda
        namesDict["Metric: cDA"] = "Continuous Daylight Autonomy at %s %s" % (
        self.metricsCDA.illuminance, illumUnit)
        self.log += "\n"+metricsFileCdaExists

        self.metricsFileDf,metricsFileDfExists = fixPaths("Daylight Factor Results File",spaceDirectory,self.directoryResults,metricsFileDf)
        filesDict["Metric: DF"]=self.metricsFileDf
        namesDict["Metric: DF"]="Daylight Factor"
        self.log += "\n"+metricsFileDfExists


        self.metricsFileOccupiedSda,metricsFileOccupiedSdaExists = fixPaths("Occupied Spatial Daylight Autonomy File",spaceDirectory,self.directoryResults,metricsFileOccupiedSda)
        filesDict["Metric: Occupied-sDA"]=self.metricsFileOccupiedSda
        namesDict["Metric: Occupied-sDA"]="Occupied Spatial Daylight Autonomy at %s %s (Fraction: %s)"%(
            self.metricsOccupiedSDA.illuminance,illumUnit,self.metricsOccupiedSDA.daFraction)
        self.log += "\n"+metricsFileOccupiedSdaExists

        self.metricsFileUdi,metricsFileUdiExists = fixPaths("Useful Daylight Illuminance File",spaceDirectory,self.directoryResults,metricsFileUdi)
        filesDict["Metric: UDI"]=self.metricsFileUdi
        namesDict["Metric: UDI"]="Useful Daylight Illuminance\nIlluminance between %s %s and %s %s"%(self.metricsUDI.minimum,illumUnit,self.metricsUDI.maximum,illumUnit)
        self.log += "\n"+metricsFileUdiExists

        self.metricsFileUdiAbove,metricsFileUdiAboveExists = fixPaths("Useful Daylight Illuminance (Above) File",spaceDirectory,self.directoryResults,metricsFileUdiAbove)
        filesDict["Metric: UDI (Above)"]=self.metricsFileUdiAbove
        namesDict["Metric: UDI (Above)"]="Useful Daylight Illuminance\nIlluminance above %s %s"%(self.metricsUDI.maximum,illumUnit)

        self.log += "\n"+metricsFileUdiAboveExists

        self.metricsFileUdiBelow,metricsFileUdiBelowExists = fixPaths("Useful Daylight Illuminance (Below) File",spaceDirectory,self.directoryResults,metricsFileUdiBelow)
        filesDict["Metric: UDI (Below)"]=self.metricsFileUdiBelow
        namesDict["Metric: UDI (Below)"] = "Useful Daylight Illuminance\nIlluminance below %s %s" % (
        self.metricsUDI.minimum, illumUnit)

        self.log += "\n"+metricsFileUdiBelowExists


        scheduleFileShades = self.spaceName+"_"+"shade.sch"

        self.scheduleShades,scheduleFileExists = fixPaths("Shade Settings File",spaceDirectory,self.directoryResults,scheduleFileShades)
        filesDict["Shade Settings"]=self.scheduleShades
        self.log += "\n"+scheduleFileExists


        if 'control_zones' in spaceDict:
            controlZones = spaceDict['control_zones']
            controlZoneNames = [str(controlZone['name']) for controlZone in controlZones]
            zoneIllFileNames = [self.spaceName+'_'+zoneName+'.ill' for zoneName in controlZoneNames]
            self.elecZoneFiles = []
            for idx,fileNames in enumerate(zoneIllFileNames):
                elecZoneFile,elecZoneFileExists = fixPaths('Electric Zone file for Zone: %s'%fileNames,
                                                           spaceDirectory,self.directoryResults,
                                                           fileNames)
                self.elecZoneFiles.append(elecZoneFile)
                filesDict['Electric Zone %s'%os.path.splitext(fileNames)[0]]=self.elecZoneFiles[idx]
                self.log += '\n'+elecZoneFileExists

        self.filesDict = dict(filesDict)
        self.namesDict = dict(namesDict)


    class __StadicWindowGroups:
        """
            Create a window group object
        """
        def __init__(self,spaceName,spaceDirectory,resFolder,windowDict):
            self.name = windowDict['name']
            self.log = "\n"

            baseFileName = spaceName+"_"+windowDict['name']+"_"+'base.ill'
            baseFileKey = windowDict['name']+"(WG), Base"

            baseDirectFileName = spaceName+"_"+windowDict['name']+"_"+'base_direct.ill'
            baseDirectFileKey = windowDict['name']+"(WG), Base Direct"


            fileBaseName,fileExists = fixPaths("Base Illuminance File for WindowGroup:{}".format(self.name),spaceDirectory,resFolder,baseFileName)
            self.log += "\n"+fileExists

            fileBaseDirectName,fileExists = fixPaths("Base Direct Illuminance File for WindowGroup:{}".format(self.name),spaceDirectory,resFolder,baseDirectFileName)
            self.log += "\n"+fileExists

            filesDict ={baseFileKey:fileBaseName,baseDirectFileKey:fileBaseDirectName}

            self.fileBase = fileBaseName
            self.fileBaseDirect = fileBaseDirectName


            settings = windowDict['shade_settings']
            settingsFiles = [spaceName+"_"+windowDict['name']+"_"+'set{}'.format(idx+1)+".ill" for idx,setting in enumerate(settings)]
            settingsFilesKeys = [windowDict['name']+"(WG), "+'set{}(Set.)'.format(idx+1) for idx,setting in enumerate(settings)]

            #Mar-20-2016: This step gets repeatd later on but I am doing this here to just append the file exists info to log.
            for index,files in enumerate(settingsFiles):
                fileName,fileExists = fixPaths("Illuminace File for WindowGroup:{}, Setting{}".format(self.name,index+1),spaceDirectory,resFolder,files)
                self.log += "\n"+fileExists


            directSettingsFiles = [spaceName+"_"+windowDict['name']+"_"+'set{}'.format(idx+1)+"_direct.ill" for idx,setting in enumerate(settings)]
            for index,files in enumerate(directSettingsFiles):
                fileName,fileExists = fixPaths("Direct Illuminace File for WindowGroup:{}, Setting{}".format(self.name,index+1),spaceDirectory,resFolder,files)
                self.log += "\n"+fileExists

            settingsFiles += directSettingsFiles
            settingsFilesKeys += [windowDict['name']+"(WG), "+'set{}(Set.), Direct'.format(idx+1) for idx,setting in enumerate(settings)]

            for idx,files in enumerate(settingsFiles):
                settingsFiles[idx],fileDetails=fixPaths("settingsFile",spaceDirectory,resFolder,files)

            filesDict.update(zip(settingsFilesKeys,settingsFiles))


            self.fileSettings = list(settingsFiles)

            signalFileName =spaceName+"_"+windowDict['name']+"_"+'shade.sig'
            signalFileKey = windowDict['name']+"(WG), ShdSigFile"

            signalFileName,fileExists = fixPaths('Signals File for WindowGroup:{}'.format(self.name),spaceDirectory,resFolder,signalFileName)
            self.fileShadeSignal = signalFileName
            self.log += "\n"+fileExists

            filesDict.update({signalFileKey:signalFileName})

            self.filesDict = dict(filesDict)

    class __StadicAnalysisPoints:
        """
            Analysis points can be
        """
        def __init__(self,analysisDict):
            self.files = analysisDict['files']
            self.xSpacing = analysisDict['x_spacing']
            self.ySpacing = analysisDict['y_spacing']
            self.zOffset = analysisDict['z_offset']
            self.offset = analysisDict['offset']
            self.modifier = analysisDict['modifier']

        def __str__(self):
            string = "~Analysis Points Details~\nFiles: {}".format(",".join(self.files))
            string +="\nxSpacing,ySpacing: ({0.xSpacing},{0.ySpacing})".format(self)
            string +="\nOffset:{0.offset}\nzOffset: {0.zOffset}".format(self)
            string +="\nModifier(s): {}\n".format(",".join(self.modifier))
            return string

    class __StadicMetricsDA:
        def __init__(self,daDict):
            self.illuminance = daDict['illuminance']
            self.calculate = daDict['calculate']

        def __str__(self):
            return "Daylight Autonomy Settings: Illuminance:{0.illuminance}, Calculate:{0.calculate}".format(self)

    class __StadicMetricsOccupiedSDA:
        def __init__(self,daDict):

            self.illuminance = daDict['illuminance']
            self.calculate = daDict['calculate']
            self.daFraction = daDict['DA_fraction']
        def __str__(self):
            return "Occupied Spatial Daylight Autonomy Settings: Illuminance:{0.illuminance}, Calculate:{0.calculate}, DA_Fraction:{0.daFraction}".format(self)

    class __StadicMetricsCDA:
        def __init__(self,daDict):
            self.illuminance = daDict['illuminance']
            self.calculate = daDict['calculate']

        def __str__(self):
            return "Continuous Daylight Autonomy Settings: Illuminance:{0.illuminance}, Calculate:{0.calculate}".format(self)

    class __StadicMetricsUDI:
        def __init__(self,daDict):
            self.minimum = daDict['minimum']
            self.calculate = daDict['calculate']
            self.maximum = daDict['maximum']
        def __str__(self):
            return "Useful Daylight Illuminance Settings: Maximum:{0.maximum}, Minimum:{0.minimum}, Calculate:{0.calculate}".format(self)

    class __StadicMetricsSDA:
        def __init__(self,daDict):
            self.illuminance = daDict['illuminance']
            self.calculate = daDict['calculate']
            self.DAFraction = daDict['DA_fraction']
            self.startTime = daDict['start_time']
            self.endTime = daDict['end_time']
            self.windowGroupSettings = daDict['window_group_settings']






        def __str__(self):
            string= "Spatial Daylight Illuminance Settings: Illuminance:{0.illuminance}, Calculate:{0.calculate}, StartTime:{0.startTime}, EndTime:{0.endTime}".format(self)
            string += ", DA Fraction:{}, WindowGroupSettings: {}".format(self.DAFraction,",".join(map(str,self.windowGroupSettings)))
            return string

    def __str__(self):
        return "SpaceName: {0.spaceName}, Location: {0.directorySpace}".format(self)


class StadicProject:
    def __init__(self,jsonFile):
        self.log = ""

        self.__jsonDict = self.__readJson(jsonFile)

        self.jsonFile = jsonFile

        self.__processJson()

    class __StadicRadianceParameters:
        """
            Separate class for reading and arranging radiance materials.
        """
        def __init__(self,paraDict):
            #Read the dictionary containing the radiance parameters and then set the values based on that.
            for key,value in paraDict.items():
                setattr(self,key,value)
        def __repr__(self):
            settingsString = "aa:{0.aa}, ab:{0.ab}, dj:{0.dj}, ad:{0.ad}, sj:{0.sj}, dc:{0.dc},".format(self)
            settingsString += "st:{0.st}, lw:{0.lw}, as:{0.as}, ar:{0.ar}, lr:{0.lr}, dt:{0.dt}, dr:{0.dr}, ds:{0.ds}, dp:{0.dp}".format(self)
            return settingsString

    def __readJson(self,jsonFile):
        """
            Try to read a json file and return a dictionary. If fails then raise Exception and let the user know.
        """
        try:
            with open(jsonFile)as jsonData:
                return json.load(jsonData)

        except ValueError:
            raise Exception("The json file could not be read properly. It is probably corrupted")

    def __processJson(self):
        """
            Extract data from a json file that has been read.
        """
        dataDict = dict(self.__jsonDict)
        genData = dataDict['general'] #Get all the general info regarding the project
        spaceData = dataDict['spaces']

        self.projectDirectory = genData['project_directory']

        self.epwFile,epwFileExists = fixPaths('EPW File',self.projectDirectory,genData['epw_file'])

        self.unitsImport = genData['import_units']
        self.unitsDisplay = genData['display_units']
        self.targetIlluminance = genData['target_illuminance']
        self.firstDay = genData['first_day']
        self.buildingRotation = genData['building_rotation']
        self.unitsIlluminance = genData['illum_units']
        self.skyDivisions = genData['sky_divisions']
        self.sunDivisions = genData['sun_divisions']
        self.groundReflectance = genData['ground_reflectance']
        self.radianceParameters = {key:self.__StadicRadianceParameters(value)for key,value in genData['radiance_parameters'].items()}

        self.daylightSavings = genData['daylight_savings_time']
        self.spaces = [__StadicSpace__(spaceDict,illumUnit = self.unitsIlluminance) for spaceDict in spaceData]


if __name__ == '__main__':
    x = StadicProject(r"C:\LF_ST\cl.json")
    print(x.log)

    print(x.groundReflectance)
    print(x.spaces[0].filesDict)
    # print(x.spaces[0].log)
    # print("*"*20)