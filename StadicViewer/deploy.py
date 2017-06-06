"""
This script will create a standalone program for a pythonn script using py2exe.
The syntax for running this file is: python deploy.py py2exe

The options, notes etc. for the syntax below can be found at: http://www.py2exe.org/index.cgi/ListOfOptions
Use console to launch this from cmd prompt. Copy mkl_avx2.dll and mkl_p4.dll into the dist folder to run.
"""


from distutils.core import setup
import py2exe,sys
import matplotlib
from distutils.filelist import findall
import os

def pathCheck(namePathTuple,message=''):
    for name,path,pathType in namePathTuple:
        assert os.path.exists(path),'The %s %s  was not found in %s. %s'%(name,pathType,path,message)


dirAnaconda = r'C:\Anaconda2'
stadicViewerPath = r'C:\Users\sarith\scripts\stadicViewer\StadicViewer'
distributionDirectory = r'C:\Users\Sarith\Dekstop\stadicVis'

mainDirTuple = [("Anaconda installation",'directory',dirAnaconda),('STADIC python repository','directory',stadicViewerPath),
                ('Distribution (exe files)','directory',distributionDirectory)]
#Check if paths exist.
pathCheck(mainDirTuple)

#lambda function for joining paths.
dataFile = lambda x: os.path.join(os.path.join(dirAnaconda,r'Library\bin'),x)



# Removed from Excludes: 'libgdk-win32-2.0-0.dll'
sys.path.append(stadicViewerPath)



dataFilesList = matplotlib.get_py2exe_datafiles() #Add matplotlib files.

dataFilesList += [(".",[dataFile("mkl_avx.dll"),
                        dataFile("mkl_p4.dll"),
                        dataFile("libiomp5md.dll"),
                        dataFile("mkl_core.dll")])]

# "dll_excludes": ["MSVCP90.dll",'libgdk-win32-2.0-0.dll','mkl_avx.dll','mkl_p4.dll'],
#PyQt4.QtNetwork was added in this case because the program uses a web viewer.
setup(windows=[{"script" : os.path.join(stadicViewerPath,'stadicVis.py')}],
      options={"py2exe" : {
                           "includes" : ["matplotlib.backends","matplotlib.backends.backend_tkagg",
                                         "matplotlib.backends.backend_qt4agg","matplotlib.figure",
                                         "pylab","sip", "scipy","PyQt4","PyQt4.QtCore","PyQt4.QtGui",
                                         "sys","signal","numpy","pdb","datetime","csv","itertools","os",
                                         "matplotlib","functools",
                                         "scipy.special._ufuncs_cxx",'matplotlib'],
                           'packages':['FileDialog'],
                           'compressed':False,
                           "dist_dir": distributionDirectory,
						   'bundle_files':3}},
      data_files=dataFilesList)