
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


import os as _os
import sys as sys
import copy as _copy
import operator as _op

from pts import Point as _point
from pts import RoomGrid as _rmgrd




class Illarr(object):
    """
        This class is a definition of the illuminance profile of a room/space.
        To be constructed, it needs illvalues and a corresponding points grid.
        Notes to self: Don't create zone inside this...create zone outside..
    """
    def __init__(self,illarr,roomgrid,vector=[0,0,1]):
        self.illarr = self.createIllArr(illarr)
        self.roomgrid = roomgrid




    def createIllArr(self,illarr):
        try:
            with open(illarr)as illfile: #If a pts file is not provided assume that this is a zone ill file. So read value into an array.
                illarr = [float(value.split()[-1])for value in illfile]
        except:
            illarr = illarr
        return illarr

    def __add__(self, other):
        """
            Operator overloading for addition
            Addition of two illarrays results in the creation of a newillarry with the added illuminance
            Addition shouldn't be allowed to mutate an existing zone. So, any addition, subtraction multiplication etc. should return a new Illarr.
        """
        try:

            self.illarr = map(_op.add,self.illarr,other.illarr)

        except:
            print(sys.exc_info())
        return self

    def __sub__(self, other):
        """
            Operator overloading for addition
            Addition of two illarrays results in the creation of a newillarry with the added illuminance
        """
        try:
            self.illarr = map(_op.sub,self.illarr,other.illarr)
        except:
            print(sys.exc_info())

        return self

    def __mul__(self, other):
        """
            Operator overloading for multiplication
            Multiply illuminance values with a scalar quantity.
        """
        try:
           self.illarr = map(_op.mul,self.illarr,[other]*len(self.illarr))
        except:
            print(sys.exc_info())

        return self


    @property
    def max_ill(self):
        maxval = max(self.illarr)
        maxpts = [idx for idx,val in enumerate(self.illarr) if val==maxval]
        maxpts = [ self.roomgrid.ptsdict[pt].ptid for pt in maxpts ]
        return {'max_ill':maxval,"points":maxpts}

    @property
    def min_ill(self):
        minval = min(self.illarr)
        minpts = [idx for idx,val in enumerate(self.illarr) if val==minval]
        minpts = [ self.roomgrid.ptsdict[pt].ptid for pt in minpts ]
        return {'min_ill':minval,"points":minpts}

    @property
    def summary(self):
        try:
            ave_val = sum(self.illarr)/len(self.illarr)
            ave_max = ave_val/self.max_ill['max_ill']
            ave_min = ave_val/self.min_ill['min_ill']
            max_min = ave_min/ave_max
            return {"av_ill":round(ave_val,2),"av_ill/max":round(ave_max,2),"av_ill/min":round(ave_min,2),"max/min":round(max_min,2)}
        except ZeroDivisionError:
            return {"av_ill":0,"av_ill/max":None,"av_ill/min":None,"max/min":None}


    def filterill(self,upper=None,lower=None,listpts=False,verbose=True,percent=False):
        """
            If only upper is provided then list all points equal to and above upper
            If only lower is provided then list all points equal to and below lower
            If upper and lower are provided list all points within that range.
            if listpts is True then list all the points for that particular option.
        """
        if not upper and not lower:
            raise  Exception("No upper and lower values were specified for filtering illuminance values")

        if upper and not lower:

            pts = [{'ptid': self.roomgrid.ptsdict[idx].ptid,'illval':illval,'ptobj':self.roomgrid.ptsdict[idx]} for idx,illval in enumerate(self.illarr) if illval>=upper]
            ptsnum = len(pts)
            if verbose:
                if listpts:
                    return {"Number of pts, out of a total {} pts, that are greater than or equal to {}".format(len(self.illarr),upper):ptsnum,"List of points":pts}
                else:
                    return {"Number of pts, out of a total {} pts, that are greater than or equal to {}".format(len(self.illarr),upper):ptsnum}
            elif percent:
                return round(ptsnum/len(self.illarr),3)
            else:
                return ptsnum

        if not upper and lower:

            pts = [{'ptid': self.roomgrid.ptsdict[idx].ptid,'illval':illval,'ptobj':self.roomgrid.ptsdict[idx]} for idx,illval in enumerate(self.illarr) if illval<=lower]
            ptsnum = len(pts)

            if verbose:
                if listpts:
                    return {"Number of pts, out of a total {} pts, that are lower than or equal to {}".format(len(self.illarr),lower):ptsnum,"List of points":pts}
                else:
                    return {"Number of pts, out of a total {} pts, that are lower than or equal to {}".format(len(self.illarr),lower):ptsnum}
            elif percent:
                return round(ptsnum/len(self.illarr),3)
            else:
                return ptsnum

        if upper and lower:

            pts = [{'ptid': self.roomgrid.ptsdict[idx].ptid,'illval':illval,'ptobj':self.roomgrid.ptsdict[idx]} for idx,illval in enumerate(self.illarr) if illval>=lower and illval<=upper]
            ptsnum = len(pts)

            if verbose:
                if listpts:
                    return {"Number of pts, out of a total {} pts, that between {} and {}".format(len(self.illarr),upper,lower):ptsnum,"List of points":pts}
                else:
                    return {"Number of pts, out of a total {} pts, that between {} and {}".format(len(self.illarr),upper,lower):ptsnum}
            elif percent:
                return round(ptsnum/len(self.illarr),3)
            else:
                return ptsnum

class Zoneill(Illarr):
    def __init__(self,zonefile):
        self.roomgrid = _rmgrd(zonefile)
        Illarr.__init__(self,zonefile,self.roomgrid)



if __name__ ==  '__main__':
    __housekeeping__()
    zone = Zoneill(r"F:\Backup\Thesis\Simulations_New\North\res\ELight_S_schLight_zone0.lum.ill")
    zone2 = Zoneill(r"F:\Backup\Thesis\Simulations_New\North\res\ELight_S_schLight_zone1.lum.ill")
    zone3 = Zoneill(r"F:\Backup\Thesis\Simulations_New\North\res\ELight_S_schLight_zone2.lum.ill")
    zone4= Zoneill(r"F:\Backup\Thesis\Simulations_New\North\res\ELight_S_schLight_zone3.lum.ill")
    zone5 = Zoneill(r'examples\zone.ill')
    print(zone5.illarr)
    x =zone5*0.4
    print(zone5.illarr)
    print(x.illarr)
    # zone6 = zoneill(r'examples\zone.ill')
    # print(zone6.roomgrid)
    print(zone5.max_ill)
    print(zone5.min_ill)
    print(zone5.roomgrid.ptsdict)
    print(zone5.roomgrid.ptsdict.popitem()[1].idx)

    print (zone2.filterill(upper=100,lower=25,listpts=False,verbose=False))