"""
This script will create a standalone program for a pythonn script using py2exe.
The syntax for running this file is: python setup.py py2exe

The options, notes etc. for the syntax below can be found at: http://www.py2exe.org/index.cgi/ListOfOptions
Use console to launch this from cmd prompt. Copy mkl_avx2.dll and mkl_p4.dll into the dist folder to run.
"""







from distutils.core import setup
import py2exe,sys
import matplotlib
from distutils.filelist import findall
import os


# Removed from Excludes: 'libgdk-win32-2.0-0.dll'
#Removed from options: "dist_dir": "F:\Dropbox\StadicViewer\Deploy",
sys.path.append(r"C:\Users\Sarith\Anaconda2\Lib\site-packages\numpy\core")
sys.path.append(r'C:\Users\Sarith\Projects\sarith\sarith\pyscripts')
sys.path.append(r'C:\Users\Sarith\Projects\stadicViewer\StadicViewer')



dataFilesList = matplotlib.get_py2exe_datafiles() #Add matplotlib files.


dataFilesList += [(".",[r"C:\Users\Sarith\Anaconda2\Library\bin\mkl_avx.dll",r"C:\Users\Sarith\Anaconda2\Library\bin\mkl_p4.dll",
                        r"C:\Users\Sarith\Anaconda2\Library\bin\libiomp5md.dll",r"C:\Users\Sarith\Anaconda2\Library\bin\mkl_core.dll"])]

# "dll_excludes": ["MSVCP90.dll",'libgdk-win32-2.0-0.dll','mkl_avx.dll','mkl_p4.dll'],
#PyQt4.QtNetwork was added in this case because the program uses a web viewer.
setup(windows=[{"script" : r"C:\Users\Sarith\Projects\stadicViewer\StadicViewer\stadicVis.py"}],
      options={"py2exe" : {
                           "includes" : ["matplotlib.backends","matplotlib.backends.backend_tkagg","matplotlib.backends.backend_qt4agg","matplotlib.figure",
                                         "pylab","sip", "scipy","PyQt4","PyQt4.QtCore","PyQt4.QtGui","sys","signal","numpy","pdb","datetime","csv","itertools","os","matplotlib","functools",
                                         "scipy.special._ufuncs_cxx",'matplotlib','results'],
                           'packages':['FileDialog'],
                           'compressed':False,
                           "dist_dir": r"C:\Users\Sarith\Projects\stadicViewer\StadicViewer\vis1.3",
						   'bundle_files':3}},
      data_files=dataFilesList)