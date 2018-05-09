  
Step1: Download Rhino. The trial version will work for 90 days with full functionality.  
+ Rhino5: http://files.mcneel.com/dujour/exe/20170522/rh50_en-us_5.14.00522.08390.exe  

Step2: Download Grasshopper and and drag the file to Rhino view port (Rhino needs to be open and running).  
+	Grasshopper: http://files.mcneel.com/dujour/exe/grasshopper_0.9.76.0.rhi  

Step3: After installing Grasshopper, restart Rhino. Then type grasshopper on the Rhino commandline and a new window will open. 
Drag and drop ghpython on to the grasshopper window (canvas).  
+	GhPython: http://www.food4rhino.com/system/files/users-files/giuliomcneelcom/app/ghpython2.gha  

Step4: Install Daysim (no deviations in steps required)  
+	Daysim: http://web.mit.edu/SustainableDesignLab/projects/Daysim/DaysimSetup.msi  

Step5: Install OpenStudio (no deviations in steps required)  
+	OpenStudio: https://openstudio-builds.s3.amazonaws.com/2.5.0/OpenStudio-2.5.0.366cbe0e3a-Windows.exe  

Step6: Install Radiance (in C:\Radiance). Assigning the path to environment variables is optional.  
+	Radiance: https://github.com/NREL/Radiance/releases/download/5.2.0/radiance-5.2.0.7b8a6d421c-Windows.exe  

Step7: Download Falsecolor and copy the executable to the Radiance bin folder (C:\Radiance\bin).  
+	Falsecolor: https://raw.githubusercontent.com/mostaphaRoudsari/honeybee/master/resources/falsecolor2.exe  

Step8: Install Therm (optional but recommended, so that there are no false warnings)  
+	Therm: https://windows.lbl.gov/system/tdf/software/THERM7_6_01_SetupFull.exe?file=1&type=node&id=6689&force=  

Step9: Install Ladybug and Honeybee (the main version, which we now call as "Legacy").   
The download is a zip file. On extract it, you will find a series of files (userobjects).   
Select and drag all of the userObject files (downloaded with this instructions file) onto your Grasshopper canvas.    
You should see Ladybug and Honeybee appear as tabs on the grasshopper tool bar.  
+	Ladybug/Honeybee: https://www.dropbox.com/s/lv7chbwkn65rcs1/ladybug0066honeybee0063.zip?dl=0  

Step10: Install Ladybug[+] and Honeybee[+] (the main version, which we now call as "Legacy").   
This too is a zip file. On extracting, you will find a single .gh file in the root directory.   
Drag and drop the .gh file on Grasshopper canvas. There is a toggle to download Honeybee[+] and Ladybug[+]  
+	Ladybug[+]/Honeybee[+]: https://www.dropbox.com/s/h6su14mwh9459xz/honeybee-grasshopper0004.zip?dl=0  


Testing: A lot of complete examples can be found on Hydrashare: http://hydrashare.github.io/hydra/. One such example is:   
http://hydrashare.github.io/hydra/viewer?owner=mostaphaRoudsari&fork=hydra_1&id=Add_wall_depth_for_daylight_simulation&slide=0&scale=1&offset=0,0  
  
I tested my installation with this file and everything was working.   
