#!/usr/bin/python                                                                                             
import os, glob, shutil
import multiprocessing as mp

import model_param as mc

PROC = 16

FILELIST = glob.glob(mc.input_directory + '*.com3D')
SAM = mc.sam_directory
CONVERTER = SAM + '/UTIL/com3D2nc '

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
		
def main():
	pool = mp.Pool(PROC)
	pool.map(convert, FILELIST)
	
	print 'All conversion processes completed.'

if __name__ == '__main__':
	main()
	