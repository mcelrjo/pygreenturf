pyGreenTurf:  User Instructions
pyGreenTurf is a digital image analysis tool designed for turfgrass scientists to quantify green turfgrass color (or lack thereof) in digital images.  While designed with turfgrass scientists and analysis of green color in mind, pyGreenTurf can be utilized for any images where the quantification of pixels within a specific hue and saturation range is desired.
pyGreenTurf is a Python script that can be run in command line or in development environments such as Enthought Canopy or Anaconda.  pyGreenTurf was developed in Canopy so it is highly recommended that Canopy be downloaded (Google: Enthought Canopy).  While pyGreenTurf can conceivable be run on any command line environment such as Terminal for Mac OS or Terminal Emulator for Linux, it has not been tested on the terminal emulator CygWin for Windows.  
Use with Canopy:  Download latest version of Canopy from Enthought website (Google it), open pyGreenTurf, run pyGreenTurf.  If certain packages have not been installed pyGreenTurf will kindly notify you of the needed packages.  Select Tool – Package Manager and type in the needed package and install.  Canopy will install the package.  Rerun pyGreenTurf.  If other packages are needed, install those and proceed until you are prompted to enter the path to the directory of images.
Enthought offers free Canopy licenses for academic institutions.  See the follow website to request your license:
https://store.enthought.com/licenses/academic/

Running in Command Line:  If you are familiar with and use command line, then the set up and use will be very straight forward.  Regardless of your familiarity with command line, open Terminal (Mac OS) and type the following in command line to determine if python is installed and your current version:
% python –V
[Note: don’t type the %, it is there to represent the command line.]
There are two possible responses:
Python 2.7.6 (or another version) or –bash: python: command not found.  
If python is not found, you must first download Python at https://www.python.org/downloads/.  Select the latest version of Python 2. Do not install Python 3 as pyGreenTurf is written in Python 2.  
Now, for those of you who have never used the command line.  On your Mac (if you have never used the command line and you are using Linux then you are a truly rare person indeed) open the Terminal program.  In terminal, type ls.  This will list everything in the current director you are in.  Now, type pwd.  This will give you the present working directory.  Congrats you have just learned two command line tools.  If you want to learn more, as with anything, google ‘learn command line’ and you will find numerous tools for learning command line.
The following packages are needed for pyGreenTurf functionality:
numpy (contained in scipy), os, sys, PIL (python image library, also known as pillow), time, re, platform, colorsys, csv, random
Many of these packages are pre-installed with the Python distribution.  If they are not installed, the easiest way to install is to install pip, which is a package installation tool Python packages.  Type % pip –V to determine if pip is installed. If not, see https://pip.pypa.io/en/stable/installing/ for installation instructions.  If pip is installed, many packages can be installed by simply typing
% pip install Pillow
and replace “Pillow” (which is PIL) for the appropriate package if not available.

Installing scipy/numpy:  Numpy arrays are the workhorse of the data analysis of pyGreenTurf.  Without numpy arrays, pyGreenTurf could not function. Numpy installation is slightly more challenging than other installations as it requires the installation of XCode, MacPorts, and scipy/numpy.  First, install XCode from the App Store. Next, install MacPorts at http://www.macports.org by clicking on “Installing MacPorts” on the left column, scroll to “Installing MacPorts” section, and select the appropriate package by clicking on your version of Mac OS.  Run the package once downloaded to complete the installation. MacPorts is installed via a GUI window-- just click on the pkg once downloaded and it will and it will install. If you have terminal open you will need to shut terminal down completely for the installation to take effect. Once MacPorts is installed you can install scipy which includes numpy at http://www.scipy.org/install.html or by Googling install numpy. On this website there will be the latest version of the following command that can be entered into command line:

% sudo apt-get install python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose

Package Installation Complete: Once all packages have been installed it is time to try out pyGreenTurf.  Run the following code in command line:

% python pyGreenTurf_0.2.5.py
 [Note: The version of pyGreenTurf is 0.2.5.  New versions will have a different number.  Just run the version you have.]
If you get the following message “[Errno 2] No such file or directory”, you must change directory (cd command) to the directory containing pyGreenTurf or you must supply the complete path to pyGreenTurf (ex., /usr/local/bin/pyGreenTurf.py).
pyGreenTurf will prompt with the following (bolded text are direct prompts):

Enter a directory path:
-	Enter the path to the directory containing the images:
o	Ex. C:\user\study\year1  -- for Windows
o	Ex. /user/study/year1    -- for Mac
Enter a lower hue level (60 to 80 suggested):
-	The lower hue level excludes all values below this level.
Enter an upper hue level (120 to 140 suggested):
-	The upper hue level excludes hue values above this level.
Enter a lower saturation level 0.0 to 1.0 (0.0 to 0.3 suggested):
-	Lower saturation does not count pixels below this minimum saturation level.  Maximum saturation level is always set to 1.0.
Do you want to compress the images?  Enter y for yes or n for no:
-	‘y’ will commit to compressing the images, ‘n’ will commit to not compressing the images.
Base width to compress pixels is set to 300.  Would you like to set a different base width for compression? Enter y for yes or n for no:
If ‘y’ is selected
Enter the base pixel width to compress images:  
If ‘n’ is selected
	Compression will not occur and analysis will proceed with uncompressed images.
 

Table 1.  Variables saved to csv file following analysis of images by pyGreenTurf.
Variable	Definition
ImagePath	Full path to the image file.  Ex. C:/usr/local/bin/DMC001.jpg
ImageName	Name of the imaged analyzed excluding the path.  Ex. DMC001.jpg
GreenPixels	Number of pixels counted from the image contained within the defined hue and saturation range. 
TotalPixels	Total number of pixels contained in the image.
PercentGreen	Percentage of pixels within the defined hue and saturation range.  Calculated as (GreenPixels/TotalPixels)*100
AverageGreen	Average hue of only pixels contained within the defined hue and saturation range.
AverageHue	Average hue of all pixels in the image.
HueStdDev	Standard deviation of all pixels in the image.
HueVar	Variance of all pixels in the image.
HueMean:VarRatio	Average hue to variance ratio for all pixels in the image.  Calculated as AverageHue/HueVar.
DGCI	Dark Green Color Index as defined by Karcher and Richardson (2003). DGCI is calculated for each individual pixel contained in the image and then average across all pixels for the image.                                                 DGCI = ((hue -60)/60)) + (1.0 - saturation) + (1.0 - value)/3.0
MeanSat	Average saturation for all pixels contained in the image.
MeanValue	Average value (also known as brightness) for all pixels contained in the image.
PixelDiversity	The average absolute difference in pixel hue values for 10,000 randomly selected pixels in the image.  PixelDiversity is calculated by randomly selecting two pixels from an image and determining the absolute hue difference between the two pixels.  The second pixel is retained and a third pixel is selected at random and the absolute hue difference is measured.  Next the third is retained, a fourth is selected,, the absolute difference is calculated, and the process is repeated for 10,000 pixel selections. 


