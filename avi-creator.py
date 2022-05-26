#@ File (label="Input directory", style="directory") inputdir 
#@ File (label="Output directory", style="directory") outputdir 
#@ String (label="Position") pos
#@ Boolean (label="Register Stack", value=False) register 

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

def sort_files(file_list):
    return sorted(file_list)

def open_image(imgfile):
    options = ImporterOptions()
    options.setId(imgfile)
    options.setSplitChannels(False)
    # options.setColorMode(ImporterOptions.COLOR_MODE_COMPOSITE)
    imps = BF.openImagePlus(options)
    return imps[0]

def create_stack(file_list, stack_name, register=True):
    file_list = [file_list[i] for i in range(3)]
    imps = [open_image(f) for f in file_list]
    #imp_array = array(imps, ImagePlus)
    stack = ImageStack(imps[0].getWidth(), imps[0].getHeight())
    for slice in imps:
        stack.addSlice(slice.getProcessor())
    stack_imp = ImagePlus(stack_name, stack)
    if register: 
        IJ.run(stack_imp, "Linear Stack Alignment with SIFT", "initial_gaussian_blur=1.60 steps_per_scale_octave=3 minimum_image_size=64 maximum_image_size=1024 feature_descriptor_size=4 feature_descriptor_orientation_bins=8 closest/next_closest_ratio=0.92 maximal_alignment_error=25 inlier_ratio=0.05 expected_transformation=Rigid interpolate");
        registered = IJ.getImage()
        return registered
    else:
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
if not os.path.isdir(inputdir):
    print inputdir, 'does not exist or is not a directory.'
else:
    file_list = get_file_list(inputdir, pos=pos)
    if len(file_list) > 0:
        sorted_list = sort_files(file_list)
        stack_name = create_filename(pos)
        stack_imp = create_stack(sorted_list, stack_name, register)
        avi_file = os.path.join(outputdir,stack_name)
        save_avi(stack_imp, avi_file)
    else:
        print ('No images found that match', pos,'.')  
print 'Done.\n'
