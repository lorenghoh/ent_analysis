import glob, os, sys
sys.path.append(os.getcwd() + '/lib/')
sys.path.append(os.getcwd() + '/cloudtracker/')

# Multiprocessing modules
import multiprocessing as mp
from multiprocessing import Pool
PROC = 4

import model_param as mc
import cloudtracker.main

### Parameters
conversion = False
cloudtracker = True
profiler = False

# Default working directory for ent_analysis package
cwd = os.getcwd()

def wrapper(module_name, script_name, function_name, filelist):
	pkg = __import__ (module_name, globals(), locals(), ['*'])
	md = getattr(pkg, script_name)
	fn = getattr(md, function_name)
	
	pool = mp.Pool(PROC)
	pool.map(fn, filelist)
	
def run_conversion():
	pkg = 'conversion'
	
	# Ensure the data folders exist at the target location
	if not os.path.exists(mc.data_directory):
		os.makedirs(mc.data_directory)
		
	if not os.path.exists('%s/variables/' % (mc.data_directory)):
		os.makedirs('%s/variables/' % (mc.data_directory))
	if not os.path.exists('%s/tracking/' % (mc.data_directory)):
		os.makedirs('%s/tracking/' % (mc.data_directory))
	if not os.path.exists('%s/core_entrain/' % (mc.data_directory)):
		os.makedirs('%s/core_entrain/' % (mc.data_directory))
	if not os.path.exists('%s/condensed_entrain/' % (mc.data_directory)):
		os.makedirs('%s/condensed_entrain/' % (mc.data_directory))
	
	# bin3d2nc conversion
	filelist = glob.glob('%s/*.com3D' % (mc.input_directory))
	#wrapper(pkg, 'convert', 'convert', filelist)
	
	# Move the netCDF files to relevant locations
	filelist = glob.glob('%s/*.nc' % (mc.input_directory))
	#wrapper(pkg, 'nc_transfer', 'transfer', filelist)
	
	# generate_tracking
	filelist = glob.glob('%s/variables/*nc' % (mc.data_directory))
	wrapper(pkg, 'generate_tracking', 'main', filelist)
	
def run_cloudtracker():
	# Change the working directory for cloudtracker
	os.chdir('%s/cloudtracker' % (cwd))
	model_config = mc.model_config
	
	# Swap input directory for cloudtracker 
	model_config['input_directory'] = \
		model_config['data_directory'] + 'tracking/'
	
	cloudtracker.main.main(model_config)

def run_profiler(filelist):
	### time_profiles
	os.chdir('%s/time_profiles' % (cwd))	
	
	if not os.path.exists('%s/time_profiles/cdf' % (cwd)):
		os.makedirs('%s/time_profiles/cdf' % (cwd))
	
	pool = mp.Pool(PROC)
	pool.map(time_profiles_wrapper, enumerate(filelist))
	
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
	
if __name__ == '__main__':
	if(conversion):
		### File conversion (.bin3D -> netCDF)
		run_conversion()
	
	if(cloudtracker):
		### Cloudtracker
		run_cloudtracker()
	
	if(profiler):
		### Additional Profiles
		run_profiler()
		
	print 'Entrainment analysis completed'
	
