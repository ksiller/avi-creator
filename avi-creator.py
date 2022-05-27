#@ File (label="Input directory", style="directory") inputdir 
#@ File (label="Output directory", style="directory") outputdir 
#@ String (label="Position") pos

import sys
import math

from ij import IJ, ImagePlus, ImageStack
from loci.plugins import BF
from loci.plugins.in import ImporterOptions
from jarray import array
import os

def get_file_list(inputdir, img_ext=["tif", "tiff"], pos=''):
    files = os.listdir(inputdir)
    img_group = [os.path.join(inputdir,f) for f in files if pos in f and f.split(".")[-1].lower() in img_ext]
    return img_group

def sort_func(item):
    #example: scan_Top Slide_R_p99_0_A01f12d3.TIF
    fname = os.path.basename(item)
    t = int(fname.split('_')[3][1:])
    return t

def sort_files(file_list):
    return sorted(file_list,key=sort_func)

def open_image(imgfile):
    options = ImporterOptions()
    options.setId(imgfile)
    options.setSplitChannels(False)
    imps = BF.openImagePlus(options)
    return imps[0]

def create_stack(file_list, stack_name):
    imps = [open_image(f) for f in file_list]
    #imp_array = array(imps, ImagePlus)
    stack = ImageStack(imps[0].getWidth(), imps[0].getHeight())
    for slice in imps:
        stack.addSlice(slice.getProcessor())
    stack_imp = ImagePlus(stack_name, stack)
    return stack_imp

def create_filename(pos):
    fname = os.path.splitext(pos)[0]
    fname = fname + '.avi'
    return fname

def save_avi(image_stack,avi_file):
    IJ.run(image_stack, "AVI... ", "compression=None frame=15 save="+avi_file)
    return
    
# Main code
inputdir = str(inputdir)
outputdir = str(outputdir)
print 'Searching for files in', inputdir
if not os.path.isdir(inputdir):
    print inputdir, 'does not exist or is not a directory.'
else:
    print 'Processing', pos
    file_list = get_file_list(inputdir, pos=pos)
    if len(file_list) > 0:
        sorted_list = sort_files(file_list)
        for fn in sorted_list:
            print fn
        stack_name = create_filename(pos)
        stack_imp = create_stack(sorted_list, stack_name)
        avi_file = os.path.join(outputdir,stack_name)
        save_avi(stack_imp, avi_file)
        print 'Saved', avi_file
    else:
        print 'No images found that match', pos,'.'  
print 'Done.\n'