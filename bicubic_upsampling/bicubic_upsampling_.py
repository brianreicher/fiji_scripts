import os
from os import path 
from ij import IJ 
from ij import WindowManager as WM
from ij.io import FileSaver, DirectoryChooser 
from ij.gui import GenericDialog  


dc = DirectoryChooser("Choose a folder")  
folder = dc.getDirectory()  
if folder is None:  
  print "User canceled the dialog!"  
else:  
  print "Selected folder:", folder 

folder_contents = os.listdir(folder) #List contents of selected director
images = []
for file in folder_contents:
	if file.endswith('tif'): #Prune for .tif files only
		images.append(file)
for i in images:
	IJ.open(folder + i)

def getOptions():  
	gd = GenericDialog("Options")  
	gd.addDirectoryField('Ouput Directory for all Files', folder)
	gd.addSlider("Upsampling Factor: ", 1, 20, 100)  
	gd.showDialog()  
	#Dialog box takes file_name and scale_value input params
	if gd.wasCanceled():
		return
	# Read out the options  
	save = gd.getNextString()
	scale = gd.getNextNumber()  
	return save, scale

options = getOptions()
if options is not None:  
  save, scale = options  #Export user input params
  print('Cubic Upsampling Parameters: ' + save, scale)

open_images = []  
for id in WM.getIDList():  
  open_images.append(WM.getImage(id))

def cubic_upsample(im): #Upsample helper func
	return IJ.run(im, 'Scale...', 'x=' + str(scale) + ' y=' + str(scale) + ' interpolation=Bicubic create')

#Generates and saves upsampled file to the listed directory
for i in range(0, len(open_images)):
	cubic_upsample(open_images[i])
	upsampled_image = IJ.getImage()
	usi = str(upsampled_image)
	start, end = usi.index('['),  usi.index(' ')
	usi_sub = usi[start+2:end-7] + '_upsampled_'+str(options[1])+'.tif' #Trim file name to exclude info and .tif string
	print('Succesfully saved at ' + options[0]+ usi_sub)
	FileSaver(upsampled_image).saveAsTiff(options[0]+usi_sub)
	#Add file info to contain --upsampled tag and pixel scale size

