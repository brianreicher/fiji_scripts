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
	gd.addStringField("Name: ", "Default (<file name>_upsampled_<scaling_rate>")
	gd.addStringField("Path to Save Files: ", "Default (original image location)")  
	gd.addSlider("Scaling Rate: ", 1, 20, 100)  
	gd.showDialog()  
	#Dialog box takes file_name and scale_value input params
	if gd.wasCanceled():
		return
	# Read out the options  
	name = gd.getNextString()
	save = gd.getNextString()
	scale = gd.getNextNumber()  
	return name, save, scale

options = getOptions()
if options is not None:  
  name, save, scale = options  #Export user input params
  print('Cubic Upsampling Parameters: ' + name, save, scale)

open_images = []  
for id in WM.getIDList():  
  open_images.append(WM.getImage(id))

def cubic_upsample(im): #Upsample helper func
	return IJ.run(im, 'Scale...', 'x=' + str(scale) + ' y=' + str(scale) + ' interpolation=Bicubic create')

def get_file_name(file_name): #Uses auto-generated filename unless default option is changed
	if options[0].startswith('Default'):
		return file_name
	else:
		return options[0]

def get_save_path(): #Returns the users desired path for saving upsampled tiffs
	if options[1].startswith('Default'):
		return folder #Saves to original location if default param is unchaged
	else:
		return options[1] #Saves to desired location if default param is changed

save_path = get_save_path() #Initiates save_path variable

#Generates and saves upsampled file to the listed directory
for i in range(0, len(open_images)):
	cubic_upsample(open_images[i])
	upsampled_image = IJ.getImage()
	usi = str(upsampled_image)
	start, end = usi.index('['),  usi.index(' ')
	usi_sub = usi[start+2:end-7] #Trim file name to exclude info and .tif string
	FileSaver(upsampled_image).saveAsTiff(save_path+usi_sub+'_upsampled_'+str(options[2])+'_.tif')
	#Add file info to contain --upsampled tag and pixel scale size
