"""
    Define a daylighting array.
        Some features:
            Add zone to a daylighting array. To increase illuminance levels.

"""

from __future__ import division
from __future__ import print_function

import logging

logger = logging.getLogger("__main__")
logging.basicConfig(format='%(asctime)s -%(levelname)s module:%(module)s function:%(funcName)s message--%(message)s')


import logging as _log
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
               timestamps['data']=Illarr(timestamps['data'],self.roomgrid)
           return self

    def __add__(self, other):
        #Create a new timedata, then instantiate a new class of dayill and replace the time data in that with the new time data.
        #This seems like a very hacky way to do this thing...however it will work for the time being.
        newtimedata =[]
        newdayill = Dayill(self.illfile,self.ptsfile)

        for idx,timestamps in enumerate(self.timedata):
             newdayill.timedata[idx]['data'] = timestamps['data'] + other

        return newdayill
    def __sub__(self, other):
        newtimedata =[]
        newdayill = Dayill(self.illfile,self.ptsfile)

        for idx,timestamps in enumerate(self.timedata):
             newdayill.timedata[idx]['data'] = timestamps['data'] - other

        return newdayill
    def __mul__(self, other):
        newtimedata =[]
        newdayill = Dayill(self.illfile,self.ptsfile)

        for idx,timestamps in enumerate(self.timedata):
             newdayill.timedata[idx]['data'] = timestamps['data'] * other

        return newdayill


    def illLimits(self,maxval=None,minval=None,day=None,hrlst=False,verbose=False,percent=False):
        if not (maxval or minval):  #If neither upper and lower values are given then assume values of max,min as 2500,200
            maxval=2500
            minval =200

        return [timestamps['data'].filterill(maxval,minval,verbose=verbose,percent=percent)for timestamps in self.timedata]

    @property
    def max_ill(self):
         return [timestamps['data'].max_ill['max_ill'] for timestamps in self.timedata]

    @property
    def min_ill(self):
         return [timestamps['data'].min_ill['min_ill'] for timestamps in self.timedata]
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
                print(timeStamps['data'].filterill(upper=illuminance,verbose=False,listpts=True))


    def __str__(self):
        return self.summary_text

if __name__ =="__main__":

    _log.basicConfig(level=_log.ERROR,format="%(asctime)s %(message)s")
    daylight = Dayill(r"C:\Users\Sarith\Desktop\daylighting\Ov_2_Ec_1.0_GT_0.0_GB_1.0\annualSimulation\Ov_2_Ec_1.0_GT_0.0_GB_1.0_0.ill",r"C:\Users\Sarith\Desktop\daylighting\Ov_2_Ec_1.0_GT_0.0_GB_1.0\annualSimulation\Ov_2_Ec_1.0_GT_0.0_GB_1.0_0.pts")
    print(daylight.roomgrid)
    print(daylight.roomgrid.uniCorX)
    print(daylight.roomgrid.uniCorY)
    print(daylight.timedata[0])
    # zone = _Zoneill(r"F:\Backup\Thesis\Simulations_New\North\res\ELight_S_schLight_zone0.lum.ill")
    # zone2 = _Zoneill(r"F:\Backup\Thesis\Simulations_New\North\res\ELight_S_schLight_zone1.lum.ill")
    # zone3 = _Zoneill(r"F:\Backup\Thesis\Simulations_New\North\res\ELight_S_schLight_zone2.lum.ill")
    # zone4= _Zoneill(r"F:\Backup\Thesis\Simulations_New\North\res\ELight_S_schLight_zone3.lum.ill")
    # zone5 = zone3 + zone4
    # print('old',daylight.timedata[9]['data'].illarr)
    # print(zone2.illarr)
    # newday = daylight + zone2
    # print('old',daylight.timedata[9]['data'].illarr)
    # print('old+zone2',newday.timedata[9]['data'].illarr)
    #
    # day10 = daylight *10
    # print('old',daylight.timedata[9]['data'].illarr)
    # print('day10',day10.timedata[9]['data'].illarr)
    #
    # print(newday.timedata[9]['data'].illarr)
    # print('zone3',zone3.illarr)
    # print('zone4',zone4.illarr)
    # print('zon25',zone5.illarr)

