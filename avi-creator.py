# @ File (label="Input directory", style="directory") inputdir 
# @ File (label="Output directory", style="directory") outputdir 
# @ String (label="Position", ) pos

import sys
import math

from ij import IJ, Prefs, ImagePlus
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from ij.plugin.frame import RoiManager
from ij.plugin import Straightener
from ij import WindowManager
from ij.process import ImageStatistics as IS
from ij.measure import ResultsTable
from java.awt import Polygon, Color
from ij.gui import Overlay, Roi, Line, PolygonRoi, Plot
from sc.fiji.analyzeSkeleton import AnalyzeSkeleton_, Edge, Point
from java.lang import Double
from java.util import ArrayList
from itertools import islice

import os
from os import path

def get_file_list(inputdir, img_ext=["tif", "tiff", pos=''):
    files = os.listdir(inputdir)
    img_group = [f for f in files if pos in f and f.split(".")[-1] in img_ext]
    return img_group

def open_image(imgfile):
	options = ImporterOptions()
	options.setId(imgfile)
	options.setSplitChannels(False)
	options.setColorMode(ImporterOptions.COLOR_MODE_COMPOSITE)
	imps = BF.openImagePlus(options)
	splitimps = [ImagePlus("%s-C-%i" % (imps[0].getTitle(), i),imps[0].getStack().getProcessor(i)) for i in range(1,imps[0].getNChannels()+1)] 
	for si in splitimps:
		si.setCalibration(imps[0].getCalibration().copy())
	return imps[0], splitimps

def create_stack(file_list):
    return

def create_filename(file_list):
    return file_list[0].avi

def save_avi(image_stack,fname):
    return
    
# Main code
inputdir = str(inputdir)
outputdir = str(outputdir)
if not path.isdir(inputdir):
    print inputdir, 'does not exist or is not a directory.'
else:
	file_list = get_file_list(inputdir, pos=pos)
    image_stack = create_stack(file_list)
    fname = create_filename(file_list)
    save_avi(image_stack, fname)
	print 'Done.\n'

