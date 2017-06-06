## STADICvis: STADIC data visualization engine.


### (Open Source) Dependencies
* Anaconda 2 (Contains Python 2.7, PyQT, Matplotlib and Numpy).
* Pycharm Community Edition 2016 (Any Python-based editor would do, but Pycharm is highly recommended).


## Testing the repository.
1. Fork the repository.
2. Run the file StadicViewer/stadicVis.py in Pycharm.
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
