import glob, os, sys
sys.path.append(os.getcwd() + '/lib/')
sys.path.append(os.getcwd() + '/cloudtracker/')

import multiprocessing as mp
from multiprocessing import Pool
PROC = 16

import model_param as mc

def run_conversion(filelist):
	from conversion import *
	
	#convert.main()
	
	# generate_tracking
	for time_step, filename in enumerate(filelist):
		print "time_step: " + str(time_step)
		generate_tracking.main(time_step, filename)
		
def run_cloudtracker():
	import cloudtracker.main
	
	# Change the working directory for cloudtracker
	os.chdir('./cloudtracker')
	
	model_config = mc.model_config
	
	model_config['input_directory'] = model_config['data_directory'] + 'tracking/'
	cloudtracker.main.main(model_config)
	
	# Return to entrainment analysis directory
	os.chdir('../')	

def run_time_profiles(filelist):
	from time_profiles import make_profiles
	
	for time, filename in enumerate(files):
		make_profiles.main(time, filename)

def main():
	filelist = glob.glob('%s/variables/*.nc' % mc.data_directory)
	filelist.sort()

	### File conversion (.bin3d -> netCDF)
	#run_file_conversion(filelist)
	
	### Cloudtracker
	#run_cloudtracker()
	
	### Additional Profiles
	run_time_profiles(filelist)
	
if __name__ == '__main__':
	main()
	
	print 'Entrainment analysis completed'
	