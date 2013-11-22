#!/usr/bin/python                                                                                             
import os, glob, shutil
import model_param as mc

SAM = mc.sam_directory
CONVERTER = SAM + '/UTIL/bin3D2nc '

############################
### No need to edit the following script
def convert(filename):	
	result = os.system(CONVERTER + filename)
	print result
	
	if result != 0:
		print "Process aborted."
		raise "Conversion failed!"
		
def convert_stat():
	stat_name = glob.iglob(SAM + '/OUT_STAT/*.stat').next()
	nc_name = stat_name.split('.')[0] + '.nc'
	
	result = os.system(SAM + '/UTIL/stat2nc ' + stat_name)
	print result
	
	if result != 0:
		print "Process aborted."
		raise "Conversion failed!"
	else:
		shutil.copy(nc_name, mc.data_directory)

	