"""
This module defines the class for a Daylight illuminance file.
"""

from __future__ import division
from __future__ import print_function

import logging

logger = logging.getLogger("__main__")
logging.basicConfig(format='%(asctime)s -%(levelname)s module:%(module)s function:%(funcName)s message--%(message)s')

from ill import Illarr
import pts
import timeSeries


class Dayill(timeSeries.TimeArray):
    """Make this as a subclass of time array. Embed ill arrays into this"""

    def __init__(self,illfile,ptsfile):

            timeSeries.TimeArray.__init__(self, illfile) #Call the constructor from timeseries array. This will define self.timedata and self.extradata
            self.roomgrid = pts.RoomGrid(ptsfile) #create a dictionary of points from the pts file.
            self.illfile = illfile
            self.ptsfile = ptsfile
            self.timedata_TO_ill()



    def proc_ptsfile(self,ptsfile):
        with open(ptsfile)as pts:
            return [line for line in pts]

    def timedata_TO_ill(self):
           for timestamps in self.timedata:
               timestamps['readStadicData']=Illarr(timestamps['readStadicData'],self.roomgrid)
           return self

    def __add__(self, other):
        #Create a new timedata, then instantiate a new class of dayill and replace the time readStadicData in that with the new time readStadicData.
        #This seems like a very hacky way to do this thing...however it will work for the time being.
        newtimedata =[]
        newdayill = Dayill(self.illfile,self.ptsfile)

        for idx,timestamps in enumerate(self.timedata):
             newdayill.timedata[idx]['readStadicData'] = timestamps['readStadicData'] + other

        return newdayill
    def __sub__(self, other):
        newtimedata =[]
        newdayill = Dayill(self.illfile,self.ptsfile)

        for idx,timestamps in enumerate(self.timedata):
             newdayill.timedata[idx]['readStadicData'] = timestamps['readStadicData'] - other

        return newdayill
    def __mul__(self, other):
        newtimedata =[]
        newdayill = Dayill(self.illfile,self.ptsfile)

        for idx,timestamps in enumerate(self.timedata):
             newdayill.timedata[idx]['readStadicData'] = timestamps['readStadicData'] * other

        return newdayill


    def illLimits(self,maxval=None,minval=None,day=None,hrlst=False,verbose=False,percent=False):
        if not (maxval or minval):  #If neither upper and lower values are given then assume values of max,min as 2500,200
            maxval=2500
            minval =200

        return [timestamps['readStadicData'].filterill(maxval,minval,verbose=verbose,percent=percent)for timestamps in self.timedata]

    @property
    def max_ill(self):
         return [timestamps['readStadicData'].max_ill['max_ill'] for timestamps in self.timedata]

    @property
    def min_ill(self):
         return [timestamps['readStadicData'].min_ill['min_ill'] for timestamps in self.timedata]
    @property
    def summary_text(self):
        roomgridsummary = str(pts.RoomGrid(self.ptsfile))
        return roomgridsummary

    def metricSDA(self,illuminance=300,startTime=8,endTime=18,daFraction=0.5):
        """
            Note that
        """
        for timeStamps in self.timedata:
            if startTime<= timeStamps['h']<=endTime:
                print(timeStamps['readStadicData'].filterill(upper=illuminance,verbose=False,listpts=True))


    def __str__(self):
        return self.summary_text

if __name__ =="__main__":
    pass

