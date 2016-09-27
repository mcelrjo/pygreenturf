#! /usr/bin/env python

'''pyGreenTurf is a simple Python script for converting RGB values from an image
into HSV (hue, saturation, value-- aka, hue, saturation, and brightness) and 
quantifying pixel count data based on a defined hue range.  For turf research, 
digital image analysis is utilized to determine the average green color of an
image and to determine the amount of green turf cover contained in an image.  
These data can be used as quantitative data relatable to turfgrass quality and
development. 

pyGreenTurf was written by Scott McElroy, Professor at Auburn University, over a
couple days after he got frustrated looking for the SigmaScan install cd.  
pyGreenTurf is completely free and is supported by Dr. McElroy if you ask 
politely.  Simply email him at mcelroy@auburn.edu.  
'''
try:
    import sys
except ImportError:
    print "This program requires sys.  Install before proceeding."

try:
    import numpy as np
except ImportError:
    sys.exit("This function requires numpy which is a component of scipy.  \n\
    Please install scipy before proceeding. It is highly \n\
    recommended that you install Enthought Canopy, which is free for academics \n\
    instead of trying to install scipy/numpy. If you cannot install Canopy and you are on a Mac \n\
    you need to first install XCode from the App Store, the install from MacPorts \n\
    at http://www.macports.org.  Before going \n\
    to this site.  Once MacPorts is installed you can install scipy which includes \n\
    numpy at http://www.scipy.org/install.html or by Googling install numpy.  MacPorts \n\
    is installed via a GUI window-- just click on the pkg once downloaded and it will \n\
    and it will install.  If you have terminal open you will need to shut terminal \n\
    down completely for the install to take effect.  Once this is done run the code \n\
    under Mac Packages- MacPorts on the scipy install website. Numpy is the workhorse \n\
    of pyGreenTurf calculations.")

try:
    from PIL import Image
except ImportError:
    sys.exit("This program requires PIL.  Please install PIL or pillow before proceeding.")
    
try:
    import os,csv,colorsys,time,re, platform, random
except ImportError:
    sys.exit("This program requires os, csv, sys, itertools, time, random, platform, and colorsys. To \n\
    determine which modules you are missing by typing help(os) in the prompt to \n\
    deterimine if os is missing then do this for each of the other modules. \n\
    You can google each of the modules to learn more about them and read \n\
    the code below to see how they are implemented. ")

print "When entering do not enter do not use quotes or \
a slash at the end of the last directory. \
Also do not include names of images in the directory path.\
pyGreenTurf will select all images in the directory for analysis \n"

path = raw_input("Enter a directory path: ")    

print "Set the minimium hue value, or lowerHue, to be included in the \
analysis.  Green color starts with a minimum hue of 60 to 80 with values \
below 60 having more yellow coloration.  Maximum hue values, referred to \
as upperHue are suggested at 141. Keep in mind that these settings are \
critical to data received and these values should be reported in any \
publication of digital image analysis."

lowerHue = raw_input("Enter a lower hue level (60 to 80 suggested): ")
print "\n"
upperHue = raw_input("Enter an upper hue level (120 to 140 suggested): ")

if int(lowerHue) > int(upperHue):
    sys.exit("You have entered a greater lower hue level than the upper hue level \n\
    which will result in no data output. Program aborted.")

minSat = float(raw_input("Enter a minimum saturation level between 0.0 to 1.0 \n\
0.0 to 0.3 is recommended: "))

if minSat > 1.0 or minSat < 0:
    sys.exit("You have entered a minimum saturation > 1.0  or < 0 which will \n\
    will result in erroneous data.  Program aborted.")
    

#print "Saturation values vary between 0 and 1 with lower saturation making the \
#image to appear more black.  Thus, you may want to set a minimum saturation \
#level to eliminate pixels that fall within the green hue range but are \
#appear more black in appearance."
#
#minSat = raw_input("Enter a minimum saturation level, normally between \
#0.0 and 0.25. Suggested 0.0: ")

compress = raw_input("Do you want to compress the images? Enter y for yes or n for no: ")

if compress == 'y' or compress == "Y" or compress == "yes" or compress == "Yes":
    compress = True
    print "WILL compress. CTRL-c to abort"
else:
    compress == False
    print "WILL NOT compress. CTRL-c to abort"
    basewidth = 300

if compress == True:
    changeBase = raw_input("Base width for compression is set at 300 pixels. \n \
    Would you like to set a different base width for compression? Enter y for yes or n for no: ")
    change = False
 
    if changeBase == 'y' or changeBase == "Y" or changeBase == "yes" or changeBase == "Yes":
        change = True
    
    if change == True:
        basewidth = int(raw_input("Enter a basewidth to compress images. Suggested 300:"))
        print "pyGreenTurf will compress your images with a base pixel value of ", \
        str(basewidth), " if you do not want to compress, press control-c and start over."
        
    if change == False:
        basewidth = 300.0
        print "pyGreenTurf will compress your images with a base pixel value of ", \
        str(basewidth), " if you do not want to compress, press control-c and start over."
        
def generateNewPath(path, basewidth):
    '''generateNewPath generates a new path for compressed images.  If the user
    elects to not compress images then generateNewPath will not be executed. 
    path:  STR, Original entered path
    basewidth:  INT, base pixel width of image compression
    RETURN: STR, new path generated in which compressed pixels will be stored
    '''
    if platform.system() == 'Windows':   
        newPath = path+"\\resized_" + str(basewidth)
        if not os.path.exists(newPath):
            os.makedirs(newPath)
    else:
        newPath = path+ "/resized_" + str(basewidth)
        if not os.path.exists(newPath):
            os.makedirs(newPath)
    return newPath


def resizeImages(image, newPath, baseWidth):
    '''This function resizes and renames images, storing the new images in 
    a new file that can then be analyzed.
    image: STR, this is the full string path of the image.
    newPath:  STR, this is the new path generated by generateNewPath
    basewidth:  INT, base pixel width of image compression
    RETURN: nothing, images are saved in newPath directory
    '''
    loc, imageName = os.path.split(image)
    
    img = Image.open(image)
    
    if platform.system() == 'Windows':

        #Break apart the image name to rename the image
        pattern = ('(\S+)(\.)(\S+)')
        compilePattern = re.compile(pattern)
        first, period, end = compilePattern.search(imageName).groups()
        #allMatches = compilePattern.search(imageName)
        #first, period, end = allMatches.groups()
        newName = newPath + "\\" + first + "_resized_" + str(baseWidth) + period + end
    else:
        pattern = ('(\S+)(\.)(\S+)')
        compilePattern = re.compile(pattern)
        first, period, end = compilePattern.search(imageName).groups()
        newName = newPath + "/" + first + "_resized_" + str(baseWidth) + period + end
        
    #Now resize the image
        
    wpercent = (baseWidth / float(img.size[0]))
    hsize = int((float(img.size[1]) * float(wpercent)))
    img2 = img.resize((baseWidth, hsize), Image.ANTIALIAS)
    img2.save(newName)
    
def batchResizeImages(originalPath, newPath, baseWidth):
    '''batchResizeImages calls resizeImages to compress images with basewidth
    set by user or with default value of 300.  
    originalPath: STR, the original input path.  Names of original images are 
    extracted from these images.
    newPath:  STR, this is the new path generated by generateNewPath
    basewidth
    '''
    
    bigImages, bigImagesList = createImageList(originalPath)
    
    for image in bigImages:
        try:
            i = Image.open(image)
            i.close()
            resizeImages(image, newPath, baseWidth)
        except IOError:
            print image + ' is not an image.  Skipping that one.'

def createImageList(path):
    
    imageList = []
    #imageNamesList = []

    listdir = os.listdir(path)
    
    if platform.system() == 'Windows':
    
        for i in listdir:
            imageList.append(path + '\\' + i)
    else:
        for i in listdir:
            imageList.append(path + '/' + i)
        
    return imageList, listdir

def greenPixelCounter(img, lowerhue, upperhue, minsat):
    
    imgArray = np.array(img)
    
    hueAngles = []
    
    DGCI = []
    sat = []
    val = []
    
    for i in range(len(imgArray)):
        for j in imgArray[i]:
            #print j[0], j[1], j[2]
            
            h,s,v = colorsys.rgb_to_hsv(float(j[0])/255., float(j[1])/255., float(j[2])/255.)
            hue = h *360
            hueAngles.append(hue)
            sat.append(s)
            val.append(v)
            DGCI.append((((hue-60.0)/60.0)+ (1.0-s)+(1.0-v))/3.0)
         
    count = 0
    pixelDiversity = randomPixelJumper(img, imgArray)
    hues = np.array(hueAngles)
    satArray = np.array(sat)
    valArray = np.array(val)
    DGCIarray = np.array(DGCI)
    greenHues = []
    possible =0
    pos = -1
    for i in hues:
        possible += 1
        pos += 1
        if i > float(lowerhue) and i < float(upperhue) and satArray[pos] > float(minsat):
            count += 1
            greenHues.append(i)
            
    greenHuesArray = np.array(greenHues)

    return count, possible, (count/float(possible))*100, greenHuesArray.mean(), hues.mean(),  hues.std(), hues.var(), hues.mean()/hues.var(), DGCIarray.mean(), satArray.mean(), valArray.mean(), pixelDiversity
    
def openImage(imageLocation):
    '''Imaged is opend from a given location so it can analyzed in subsequent 
    functions that call openImage.
    Return:  an opened image.  Image is closed in subsequent functions that 
    call openImage
    '''
    img = Image.open(imageLocation)
    return img
  
def createCSVFile(path):
    '''Given a path, a csvFile is created using the last file name in the path
    plus the asctime with spaces and semicolons removed.
    Return:  a csv to which data will be written
    '''

    if platform.system() == 'Windows':
    
        basePath, lastFile = os.path.split(path)
        fileName = path + "\\" + lastFile +time.asctime().replace(" ","").replace(":","_") + ".csv"
        f = open(fileName, 'wt')
  
    else:
        basePath, lastFile = os.path.split(path)
        fileName = path + "/" + lastFile +time.asctime().replace(" ","").replace(":","_") + ".csv"
        f = open(fileName, 'wt')
  
    return f 
    
def randomPixelJumper(img, imgArray):
    #img = Image.open(image)
    
    #imgArray = np.array(img)
    
    x = random.randint(0, img.size[1])
    y = random.randint(0, img.size[0])
    
    h,s,v = colorsys.rgb_to_hsv(float(imgArray[x,y,0])/255., float(imgArray[x,y,1])/255., float(imgArray[x,y,2])/255.)
    hue  = h * 360.0
    hueDiffs = []

    for i in range(10000):
        
        x = random.randint(0, img.size[1]-1)
        y = random.randint(0, img.size[0]-1)
        
        h,s,v = colorsys.rgb_to_hsv(float(imgArray[x,y,0])/255., float(imgArray[x,y,1])/255., float(imgArray[x,y,2])/255.)
        newHue = h*360.0
        hueDiffs.append(abs(hue-newHue))
        hue = newHue
        
    hueDiffsArray = np.array(hueDiffs)
        
    return hueDiffsArray.mean()
    
def analyzeAndWriteToFile(path, compress, lowerHue, upperHue, baseWidth):
    
    if compress == True:
        newPath = generateNewPath(path, baseWidth)
    else: 
        newPath = path
        
    if compress == True:
        batchResizeImages(path, newPath, baseWidth)   
    
    imageList, imageNameList = createImageList(newPath)
    
    CSVFile = createCSVFile(newPath)
    
    writer = csv.writer(CSVFile, lineterminator = "\n")
    writer.writerow(("ImagePath", "ImageName", "GreenPixels", "TotalPixels","PercentGreen", "AverageGreen", "AverageHue","HueStdDev", "HueVar", "HueMean:VarRatio", "DGCI", "MeanSaturation", "MeanValue", "PixelDiversity"))

    counter = 0
    for image in imageList:
        try:
            img = openImage(image)
            if isinstance(img, Image.Image):
                greenPix, totalPix, perGreen, avgGreen, avgHue, stdev, var, mean2var, dcgi, sat, val, pixD = greenPixelCounter(img, lowerHue, upperHue, minSat)
                writer.writerow((image, imageNameList[counter], greenPix, totalPix, perGreen, avgGreen, avgHue, stdev, var, mean2var, dcgi, sat, val, pixD))
                counter += 1
                print image
            else:
                print image + " format not recognized by pyGreenTurf so skipping that one."
                counter +=1
        
        except IOError:
            print image + " is not an image so we will skip that one."
            counter += 1

    writer.writerow(("min hue:", lowerHue, "max hue:", upperHue, 'min sat:', minSat))

    CSVFile.close()

if __name__ == '__main__':
    analyzeAndWriteToFile(path, compress, lowerHue, upperHue, basewidth)
    
#http://stackoverflow.com/questions/25102461/python-rgb-matrix-of-an-image
#https://opensource.com/life/15/2/resize-images-python

#read this explanation
#https://avaminzhang.wordpress.com/2013/09/04/python-convert-rgb-to-hsv/
#http://www.cs.uregina.ca/Links/class-info/325/PythonPictures/
