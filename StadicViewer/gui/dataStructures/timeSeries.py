"""
    Base module for processing all timeseries based data.
    Use this as the base module for processing illfiles,bf.txt,weafiles.
    Dependencies: none
    Python version : 2.7
"""

from __future__ import print_function
from __future__ import division

import logging
logger = logging.getLogger("__main__")
logging.basicConfig(format='%(asctime)s -%(levelname)s module:%(module)s function:%(funcName)s message--%(message)s')

import sys
import datetime as  _dt

def timeStamp(mval,dval,tval,yearval=2015):
        """return _dt object from month,date and time values"""
        hour = int(tval)
        minute = int((tval-hour)*60)
        return _dt.datetime(yearval,int(mval),int(dval),hour,minute)

def readTextFile(filename,delimiter=False):
        "Separate a textfile into lists"
        with open(filename,'r') as ptsfile:
            for lines in ptsfile:
                if delimiter:
                    yield lines.split(delimiter)
                else:
                    yield lines.split()

class TimeArray(object):
    """Base class for all the time series readStadicData. Use this to process illfiles, wea files etc."""

    def __init__(self,filename,timeoffset=False,delimiter=False):
        self.filename=filename

        self.timedata,self.extradata = self.readfile(filename,delimiter)  #Run readfile and extract readStadicData.



    def readfile(self,filenm,delimiter):
        """A generator to yield time stamps and numerical readStadicData
           Numerical readStadicData can be ill values, weather file values etc."""

        timefiledata = []
        timefileextra = {}
        fixtimeflag = False
        hour0=hour1=False


        if isinstance(filenm,(str,unicode)):
            timeobject = readTextFile(filenm,delimiter)
        else:
            timeobject = filenm


        for idx,lines in enumerate(timeobject):

                try:
                    floatlines = map(float,lines)
                    month,date,hour = floatlines[:3]
                    dataval = floatlines[3:]
                    ##Code to check if the first time value is 1.0. If so subtract every hour by 0.5

                    if not hour1 or hour0:
                        hour1 = hour
                        if hour0==1.0 and hour1==2.0:
                            #Go back to the array that stores timevalues and fix the hour and time stamp
                            timefiledata[0]['h']=0.5
                            timefiledata[0]['tstamp']=timeStamp(1,1,0.5)
                            fixtimeflag=True

                    if not hour0:
                        hour0 = hour

                    if fixtimeflag:
                        hour = hour-0.5
                    ##Code to check if the first time value is 1.0. If so subtract every hour by 0.5

                    timestamp = timeStamp(month,date,hour)

                    timefiledata.append({"m":month,"d":date,"h":hour,"readStadicData":dataval,"tstamp":timestamp})

                except ValueError:
                    print(sys.exc_info())
                    timefileextra[lines[0]]=lines[1]

        return (timefiledata,timefileextra)

#Test the module.
if __name__ ==  '__main__':
     __housekeeping__()
     illfile = TimeArray(r'examples\test_BF.txt')

     print(illfile.timedata[:5])
     print(illfile.extradata)

     epwFile = TimeArray(r'examples\statecollege.epw',delimiter=',')