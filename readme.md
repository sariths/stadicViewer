## STADICvis: STADIC data visualization engine.

![GitHub Logo](/StadicViewer/gui/__dump/titleImage.png)




### (Open Source) Dependencies
These should be installed in the below order.
* [Anaconda 2](https://repo.continuum.io/archive/Anaconda2-4.1.1-Windows-x86.exe) (Contains Python 2.7, PyQT, Matplotlib and Numpy)
* [PyQT v4](https://downloads.sourceforge.net/project/pyqt/PyQt4/PyQt-4.11.4/PyQt4-4.11.4-gpl-Py2.7-Qt4.8.7-x32.exe?r=https%3A%2F%2Fsourceforge.net%2Fprojects%2Fpyqt%2Ffiles%2FPyQt4%2FPyQt-4.11.4%2F&ts=1496769938&use_mirror=superb-sea2)
* [Pycharm Community Edition 2017](https://download.jetbrains.com/python/pycharm-community-2017.1.3.exe). Any Python-based editor would do, but Pycharm is highly recommended.
* py2exe (Needed for compiling to exe. Will add instructions later).


## Testing the repository.
1. Fork the repository.
2. Run the file StadicViewer/stadicVis.py.
3. For a more thorough test, save one of the examples in the testProjects
directory in the right location and open that project using stadicVis.py.



#### June 6 2016: Notes for first full public release.
1. Reorganized modules and removed unnecessary relative paths.
2. Added an example folder.
3. Better docstrings for all modules and packages.
4. Removed a few redundant files.

#### May 2 2016: Version 1.03 Release notes.
1. Made plots smoother by using IMShow instead of Pcolor Mesh (that also means bug-fix from data truncation!).
2. Added an extra check-box to support 1.
3. Incorporated metrics.
4. Added tooltips.
5. Added the incorporation of shade settings files (if present, will show shade settings below illuminance title).
6. Fixed the issue with lowest illuminace being 1. Now its 0. 
