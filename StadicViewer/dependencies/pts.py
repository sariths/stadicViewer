"""
    This module defines two classes:
        1. Point is a simple 3d Point
        2. roomgrid is a collection of points in a room. that can be read off of a pts file or a zone file.
"""

from __future__ import print_function
from __future__ import division


import logging
logger = logging.getLogger("__main__")
logging.basicConfig(format='%(asctime)s -%(levelname)s module:%(module)s function:%(funcName)s message--%(message)s')



def __housekeeping__():
    try:
        __IPYTHON__
        raise Exception,"These scripts cannot be run from Ipython. Use standard python instead."
    except NameError:
        pass

    import os,sys
    currentfilename = __file__

    assert "RadScripts" in currentfilename,"\nThe path:{} is out of the RadScripts directory structure.\nSomething went horribly wrong!!".format(currentfilename)

    #Keep splitting the path till it ends with RadScripts.
    while not currentfilename.endswith("RadScripts"):
        currentfilename = os.path.split(currentfilename)[0]

     #Now that Radscripts root has been found append it to sys.path
    sys.path.append(currentfilename)

    logger.critical("{} successfully appended to sys.path".format(currentfilename))


import logging

class Point(object):
    def __init__(self,x,y,z,vector,idx=None):
        self.x = x
        self.y = y
        self.z = z
        self.vector = vector
        self.ptid = "({},{},{}),{}".format(self.x,self.y,self.z,self.vector)
        self.idx = idx #This is the location where the point occurs in the point occurs in the pts file or zone file.

    def __str__(self):
        """retrun a string representation of the point"""
        return "3D Point at x:{}, y:{}, z:{}. The vector is {}".format(self.x,self.y,self.z,self.vector)




class RoomGrid(object):

    def __init__(self,ptsfile):
        try:
            with open(ptsfile) as ptsstring:
                ptsfile = [line for line in ptsstring]

        except:
            pass
        self.ptsdict = self.procPtsFile(ptsfile)


    def procPtsFile(self,ptsfile,vector=[0,0,1]):
        """Return a dictionary containing points """
        ptsdict = {}

        for idx,lines in enumerate(ptsfile):

            try:
                linesnum = map(float,lines.split())
                x,y,z=linesnum[:3]
                assert len(linesnum)==6 #This assertion is meant for checking if there are 6 values in line, ie its a pts file. If yes get vector from the pts file. Else use default or user defined vector
                vector = linesnum[3:]
                temppt = Point(x,y,z,vector,idx)
                ptsdict[temppt.idx]=temppt
            except AssertionError: #If the assertion fails use the vector value which is defined default or specified.
                linesnum = map(float,lines.split())
                x,y,z=linesnum[:3]
                temppt = Point(x,y,z,vector,idx)
                ptsdict[temppt.idx]=temppt

            logging.info("x: {}y: {}z: {}v: {}".format(x,y,z,vector))

        return ptsdict

    @property
    def minMax(self):
        """return the minimum and maximum limits of x,y and z dimensions"""
        return {'x':(self.minX,self.maxX),'y':(self.minY,self.maxY),'z':(self.minZ,self.maxZ)}

    @property
    def minX(self):
        """
            Return the min X coordinate for the entire grid.
        :return:
        """
        return min([pt.x for pt in self.ptsdict.values()])

    @property
    def maxX(self):
        """
            Return the max X coordinate for the entire grid.
        :return:
        """
        return max([pt.x for pt in self.ptsdict.values()])

    @property
    def minY(self):
        """
            Return the min Y coordinate for the entire grid.
        :return:
        """
        return min([pt.y for pt in self.ptsdict.values()])

    @property
    def maxY(self):
        return max([pt.y for pt in self.ptsdict.values()])

    @property
    def minZ(self):
        return min([pt.z for pt in self.ptsdict.values()])

    @property
    def maxZ(self):
        return max([pt.z for pt in self.ptsdict.values()])

    @property
    def ptArray(self):
        """return an array of points sorted according to their index value"""
        ptslist = sorted(self.ptsdict.values(),key=lambda pt:pt.idx) #sort the points according to their index values.
        ptslist = [(pt.x,pt.y,pt.z,pt.vector)for pt in ptslist]

        return ptslist

    @property
    def ptArrayXYZ(self):
        return [(x,y,z)for x,y,z,vector in self.ptArray]

    @property
    def ptArrayX(self):
        return [x for x,y,z,vector in self.ptArray]

    @property
    def ptArrayY(self):
        return [y for x,y,z,vector in self.ptArray]

    @property
    def ptArrayZ(self):
        return [z for x,y,z,vector in self.ptArray]

    @property
    def uniCor(self):
        """return a dictionary containing of tuples of unique coordinates in x,y,z direction"""
        ptslist = self.ptsdict.values() #sort the points according to their index values.
        ptsx = sorted(set([pt.x for pt in ptslist]))
        ptsy = sorted(set([pt.y for pt in ptslist]))
        ptsz = sorted(set([pt.z for pt in ptslist]))
        maxgridsize = len(ptsx)*len(ptsy)*len(ptsz)
        actgridsize = len(self.ptsdict)
        return {'x':ptsx,'y':ptsy,'z':ptsz,'maxgridsize':maxgridsize,'actgridsize':actgridsize}

    @property
    def uniCorX(self):
        return self.uniCor['x']

    @property
    def uniCorY(self):
        return self.uniCor['y']

    @property
    def uniCorZ(self):
        return self.uniCor['z']

    @property
    def gridSizeMax(self):
        return self.uniCor['maxgridsize']

    @property
    def gridSizeActual(self):
        return self.uniCor['maxgridsize']

    @property
    def testUniformSpc(self):
        """Test if the points are uniformly spaced in x,y,z direction. Return a string with results
            This is a good indicator of whether results are suited for daysim or not.
            The points can either be equidistant or multiples.
        """

        spcdict = dict.fromkeys(('x_spacings','y_spacings','z_spacings'),())
        coord = self.uniCor
        rounder = lambda lst:[round(val,4)for val in lst] #lambda for rounding to 4 dec digits.
        x,y,z = rounder(sorted(coord['x'])),rounder(sorted(coord['y'])),rounder(sorted(coord['z'])) #Sort and round values for unique x,y,z coord

        if len(x)-1: #If there are more than 1 unique points in x..then check for spacing..same applies to other coords
             xspc= set(rounder([x[idx]-x[idx-1]for idx in range(1,len(x))]))
             spcdict['x_spacings']=sorted(xspc)
        if len(y)-1: #If there are more than 1 unique points in x..then check for spacing..same applies to other coords
             yspc= set(rounder([y[idx]-y[idx-1]for idx in range(1,len(y))]))
             spcdict['y_spacings']=sorted(yspc)
        if len(z)-1: #If there are more than 1 unique points in x..then check for spacing..same applies to other coords
             zspc= set(rounder([z[idx]-z[idx-1]for idx in range(1,len(z))]))
             spcdict['z_spacings']=sorted(zspc)
        return spcdict

    @property
    def gridMatrix(self):
        unicor = self.uniCor
        ptarray = self.ptArray


        x,y,z,maxgrid,act = unicor['x'],unicor['y'],unicor['z'],unicor['maxgridsize'],unicor['actgridsize']
        xlen,ylen,zlen = map(len,(x,y,z))
        xmin,ymin,zmin = map(min,(x,y,z))
        xmax,ymax,zmax = map(max,(x,y,z))

        #This lambda is for calculating on basis of grid pont
        grid = lambda point:(x.index(point[0])+1,y.index(point[1])+1,z.index(point[2])+1)

        gridscale = lambda point:(round(point[0]/xmin,3),round(point[1]/ymin,3),round(point[2]/zmin,3))

        if  (xmin-xmax):
            gridscalex = lambda point:round((point[0]-xmin)/(xmax-xmin),3)
        else:
            gridscalex = lambda point:0

        if  (ymin-ymax):
            gridscaley = lambda point:round((point[1]-ymin)/(ymax-ymin),3)
        else:
            gridscaley = lambda point:0

        if  (zmin-zmax):
            gridscalez = lambda point:round((point[1]-zmin)/(zmax-zmin),3)
        else:
            gridscalez = lambda point:0

        grids = [grid(point)for point in ptarray]
        scaledgrids = [(gridscalex(point),gridscaley(point),gridscalez(point)) for point in ptarray]

        return [{'grid':gridtuple,'scaledGrid':scaledgrids[idx]}for idx,gridtuple in enumerate(grids)]

    @property
    def gridMatrixFull(self):
        """
        This property returns the maximum possible grid points in a roomGrid.
        For example a roomgrid could have 10 (x) and 10 (y) unique coordinates. But the actual number of points in the points
        file could be only 80.
        This property will calculate all the possible coordiantes.
        The order followed is X,Y,Z.
        Return a 2d grid if Z has only dimension. Or else return a 3d grid.
        :return:
        """

        xCor = self.uniCorX
        yCor = self.uniCorY
        zCor = self.uniCorZ

        gridMatrix =[]

        for xVal in xCor:
            for yVal in yCor:
                for zVal in zCor:
                    gridMatrix.append((xVal,yVal,zVal))

        return gridMatrix

    @property
    def gridMatrixLocations(self):
        """
        This property returns the location of each point with resepct to the gridMatrixFull.
        For example a pts file with max possible 100 points could have 70 points.
        This property will return the location of those points wrt to the 100 point grid.
        Locations where the points exists in the pts file will have the locaiton index of the point while others will have None.
        This property is useful in creating a rectangular grid of points from a non rectangular shaped pts file.
        :return:
        """
        fullGridMatrix = self.gridMatrixFull
        ptArray = self.ptArrayXYZ
        locations = []
        for pointTuples in fullGridMatrix:
            if pointTuples in ptArray:
                locations.append(ptArray.index(pointTuples))
            else:
                locations.append(None)

        return locations

    @property
    def spacingX(self):
        coord = self.uniCorX
        rounder = lambda lst:[round(val,4)for val in lst] #lambda for rounding to 4 dec digits.
        unique = rounder(sorted(coord))
        if len(unique)-1:
            spacings =  sorted(set(rounder([unique[idx]-unique[idx-1]for idx in range(1,len(unique))])))
        else:
            spacings = ()
        return spacings
    @property
    def spacingY(self):
        coord = self.uniCorY
        rounder = lambda lst:[round(val,4)for val in lst] #lambda for rounding to 4 dec digits.
        unique = rounder(sorted(coord))
        if len(unique)-1:
            spacings =  sorted(set(rounder([unique[idx]-unique[idx-1]for idx in range(1,len(unique))])))
        else:
            spacings = ()
        return spacings

    @property
    def spacingZ(self):
        coord = self.uniCorZ
        rounder = lambda lst:[round(val,4)for val in lst] #lambda for rounding to 4 dec digits.
        unique = rounder(sorted(coord))
        if len(unique)-1:
            spacings =  sorted(set(rounder([unique[idx]-unique[idx-1]for idx in range(1,len(unique))])))
        else:
            spacings = ()
        return spacings
    def __str__(self):
        extents = self.minMax
        totalpts = len(self.ptsdict)
        unicor = self.uniCor
        unitest = self.testUniformSpc
        checkval = [len(coor) for coor in unitest.values()] #Get the length of list of unique coor in x,y,z
        checkspc = not any([False if (val==1)|(val==0) else True for val in checkval]) #return a list of true/false. False if val is 0 or 1. True otherwise. evaluate to False if any one value is True


        return """
        The total number of grid points is {}.
        Dimension limits: X:{}, Y:{}, Z:{}.
        Unique number of points in each dimension(X,Y,Z):({},{},{}).
        Maximum possible grid size: {}.
        Uniformly spaced grid points:{}""".format(totalpts,extents['x'],extents['y'],extents['z'],len(unicor['x']),len(unicor['y']),len(unicor['z']),unicor['maxgridsize'],checkspc)


if __name__ ==  '__main__':
    __housekeeping__()
    logging.basicConfig(level=logging.CRITICAL,format='%(asctime)s -%(levelname)s module:%(module)s function:%(funcName)s Message:%(message)s')
    # ptsval = proc_ptsfile(open(r'examples/new.pts'))
    with open(r"E:\SExample\data\Sp1_AutoGen.pts") as ptsfile:
        y = RoomGrid([line for line in ptsfile])
    print(RoomGrid(r"E:\SExample\data\Sp1_AutoGen.pts"))
    print(RoomGrid(r'F:\Dropbox\RadScripts\results\examples\zone.ill'))
    print("*~"*100)
    print(y)
    print(y.gridMatrix)
    print(y.ptArray)
    print(y.uniCor['x'])
    print(y.uniCor['y'])
    print(y.gridMatrix)

