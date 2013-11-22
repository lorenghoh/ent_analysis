import glob, os, sys
sys.path.append(os.getcwd() + '/lib/')
sys.path.append(os.getcwd() + '/cloudtracker/')

# Multiprocessing modules
import multiprocessing as mp
from multiprocessing import Pool
PROC = 60

import model_param as mc
from conversion import convert
import cloudtracker.main

### Parameters
conversion_module = True
cloudtracker_module = True
profiler_module = True

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
	
	convert.convert_stat()
	
	# bin3d2nc conversion
	filelist = glob.glob('%s/*.com3D' % (mc.input_directory))
	wrapper(pkg, 'convert', 'convert', filelist)
	
	# Move the netCDF files to relevant locations
	filelist = glob.glob('%s/*.nc' % (mc.input_directory))
	wrapper(pkg, 'nc_transfer', 'transfer', filelist)
	
	# generate_tracking
	filelist = glob.glob('%s/variables/*nc' % (mc.data_directory))
	wrapper(pkg, 'generate_tracking', 'main', filelist)
	
def run_cloudtracker():
	# Change the working directory for cloudtracker
	os.chdir('%s/cloudtracker/' % (cwd))
	model_config = mc.model_config
	
	# Swap input directory for cloudtracker 
	model_config['input_directory'] = mc.data_directory + '/tracking/'
	cloudtracker.main.main(model_config) 

def run_profiler():
	pkg = 'time_profiles'
	### time_profiles (with core & cloud entrainment profiles)
	os.chdir('%s/time_profiles' % (cwd))	
	
	# Ensure output folder exists
	if not os.path.exists('%s/time_profiles/cdf' % (cwd)):
		os.makedirs('%s/time_profiles/cdf' % (cwd))
		
	filelist = glob.glob('%s/variables/*.nc' % (mc.data_directory))
	wrapper(pkg, 'make_profiles', 'main', filelist)
	
	filelist = glob.glob('%s/core_entrain/*.nc' % (mc.data_directory))
	wrapper(pkg, 'core_entrain_profiles', 'main', filelist)
	
	filelist = glob.glob('%s/condensed_entrain/*.nc' % (mc.data_directory))
	wrapper(pkg, 'condensed_entrain_profiles', 'main', filelist)
	
if __name__ == '__main__':
	if(conversion_module):
		### File conversion (.bin3D -> netCDF)
		run_conversion()
	
	if(cloudtracker_module):
		### Cloudtracker
		run_cloudtracker()
	
	if(profiler_module):
		### Additional Profiles
		run_profiler()
		
	print 'Entrainment analysis completed'
	
