import glob, os, sys
sys.path.append(os.getcwd() + '/lib/')
sys.path.append(os.getcwd() + '/cloudtracker/')

# Multiprocessing modules
import multiprocessing as mp
from multiprocessing import Pool
PROC = 12

import model_param as mc
import cloudtracker.main

from conversion import *
from time_profiles import *
from id_profiles import *

### Parameters
conversion = True
cloudtracker = False
profiler = False
time_profiles = False
id_profiles = False # Turned off unless needed

# Default working directory for ent_analysis package
cwd = os.getcwd()

def wrapper(fnc, (time_step,  filenema)):
	pool = np.Pool(PROC)
	return

def run_conversion(filelist):
	if not os.path.exists(mc.data_directory)
		os.makedirs(mc.data_directory)
	
	# bin3d2nc conversion
	pool = mp.Pool(PROC)
	pool.map(convert.main, filelist)
	
	return 
	
	# generate_tracking
	# Wrap the module for multi-processing
	pool = mp.Pool(PROC)
	pool.map(conv_wrapper, enumerate(filelist))
	
def conv_wrapper((time_step, filename)):
	generate_tracking.main(time_step, filename)
	
def run_cloudtracker():
	# Change the working directory for cloudtracker
	os.chdir('%s/cloudtracker' % (cwd))
	
	model_config = mc.model_config
	
	# Swap input directory for cloudtracker 
	model_config['input_directory'] = model_config['data_directory'] + 'tracking/'
	cloudtracker.main.main(model_config)

def run_profiler(filelist):
	if(time_profiles):
		### time_profiles
		os.chdir('%s/time_profiles' % (cwd))	
		
		if not os.path.exists('%s/time_profiles/cdf' % (cwd))
			os.makedirs('%s/time_profiles/cdf' % (cwd))
		
		pool = mp.Pool(PROC)
		pool.map(time_profiles_wrapper, enumerate(filelist))
	
	if(id_profiles):
		### id_profiles
		os.chdir('%s/id_profiles' % (cwd))
		core_profiles.main('core')
		
	# Core entrainment profiles
	os.chdir('%s/time_profiles' %(cwd))
	
	files = glob.glob('%s/core_entrain/*.nc' % mc.data_directory)
	files.sort()

	pool = mp.Pool(PROC)
	pool.map(core_ent_wrapper, enumerate(files))
	
	# Condensed entrainment profiles
	files = glob.glob('%s/core_entrain/*.nc' % mc.data_directory)
	files.sort()

	pool = mp.Pool(PROC)
	pool.map(core_ent_wrapper, enumerate(files))
	
def time_profiles_wrapper((time_step, filename)):
	make_profiles.main(time_step, filename)
	
def core_ent_wrapper((time_step, filename)):
	core_entrain_profiles.main(time_step, filename)

def main():
	filelist = glob.glob('%s/variables/*.nc' % mc.data_directory)
	filelist.sort()

	if(conversion):
		### File conversion (.bin3d -> netCDF)
		run_conversion(filelist)
	
	if(cloudtracker):
		### Cloudtracker
		run_cloudtracker()
	
	if(profiler):
		### Additional Profiles
		run_profiler(filelist)
	
if __name__ == '__main__':
	main()
	
	print 'Entrainment analysis completed'
	
