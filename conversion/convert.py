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
	
	print "Converting stat file..."
	print stat_name
	
	path, name = os.path.split(stat_name)
	name = os.path.splitext(name)
	
	nc_name = name[0] + '.nc'
	nc_name = os.path.join(path, nc_name)
	
	nc_new = name[0] + '_stat.nc'
	nc_new = os.path.join(mc.data_directory, nc_new)
	
	result = os.system(SAM + '/UTIL/stat2nc ' + stat_name)
	print result
	
	if result != 0:
		print "Process aborted."
		raise "Conversion failed!"
	else: 
		shutil.copy(nc_name, nc_new)
	