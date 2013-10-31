#!/usr/bin/python                                                                                             
import os, glob
import multiprocessing as mp
from multiprocessing import Pool

import model_param as mc

PROC = 16

FILELIST = glob.glob(mc.input_directory + '*.bin3D')
BIN3D2NC = mc.input_directory + 'UTIL/bin3D2nc'

############################
### No need to edit the following script
def convert(filename):
	result = os.system(BIN3D2NC + ' ' + filename)
	print result
	
	if result != 0:
		print "Process aborted."
		raise "Conversion failed!"
		
def main():
	pool = mp.Pool(PROC)
	pool.map(convert, FILELIST)
	
	print 'All conversion processes completed.'

if __name__ == '__main__':
	main()
	