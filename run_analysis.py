import glob, os, sys
sys.path.append(os.getcwd() + '/lib/')
sys.path.append(os.getcwd() + '/cloudtracker/')

# Multiprocessing modules
import multiprocessing as mp
from multiprocessing import Pool
PROC = 24

import model_param as mc
from conversion import convert
import cloudtracker.main

# Default working directory for ent_analysis package
cwd = os.getcwd()

# Output profile names
profiles = {'condensed', 'condensed_env', 'condensed_edge', \
	'condensed_shell' , 'core', 'core_env', 'core_edge', 'core_shell', \
	'plume', 'condensed_entrain', 'core_entrain', 'surface'}

def wrapper(module_name, script_name, function_name, filelist):
	pkg = __import__ (module_name, globals(), locals(), ['*'])
	md = getattr(pkg, script_name)
	fn = getattr(md, function_name)
	
	pool = mp.Pool(PROC)
	pool.map(fn, filelist)
	
def run_conversion():
	pkg = 'conversion'
	os.chdir(mc.input_directory)
	
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
	
	# Generate cloud field statistic 
	convert.convert_stat()
	
	# bin3d2nc conversion
	filelist = glob.glob('./*.bin3D')
	wrapper(pkg, 'convert', 'convert', filelist)
	
	# Move the netCDF files to relevant locations
	filelist = glob.glob('./*.nc')
	wrapper(pkg, 'nc_transfer', 'transfer', filelist)
	
	# generate_tracking
	filelist = glob.glob('%s/variables/*nc' % (mc.data_directory))
	wrapper(pkg, 'generate_tracking', 'main', filelist)
	
def run_cloudtracker():
	# Change the working directory for cloudtracker
	os.chdir('%s/cloudtracker/' % (cwd))
	model_config = mc.model_config
	
	# Update nt
	model_config['nt'] = mc.nt
	
	# Swap input directory for cloudtracker 
	model_config['input_directory'] = mc.data_directory + '/tracking/'
	cloudtracker.main.main(model_config) 

def run_profiler():
	### Time Profiles
	pkg = 'time_profiles'
	os.chdir('%s/time_profiles' % (cwd))	
	
	# Ensure output folder exists
	if not os.path.exists('%s/time_profiles/cdf' % (cwd)):
		os.makedirs('%s/time_profiles/cdf' % (cwd))
		
	# Main thermodynamic profiles
	filelist = glob.glob('%s/variables/*.nc' % (mc.data_directory))
	wrapper(pkg, 'make_profiles', 'main', filelist)
	
	filelist = glob.glob('%s/core_entrain/*.nc' % (mc.data_directory))
	wrapper(pkg, 'core_entrain_profiles', 'main', filelist)
	
	filelist = glob.glob('%s/condensed_entrain/*.nc' % (mc.data_directory))
	wrapper(pkg, 'condensed_entrain_profiles', 'main', filelist)
	
	# Chi Profiles
	filelist = glob.glob('cdf/core_env*.nc')
	wrapper(pkg, 'chi_core', 'makechi', filelist)
	
	filelist = glob.glob('cdf/condensed_env*.nc')
	wrapper(pkg, 'chi_condensed', 'makechi', filelist)
	
	# Surface Profiles (based on cloud tracking algorithm)
	wrapper(pkg, 'surface_profiles', 'main', range(mc.nt))

def run_id_profiles():
	### ID Profiles
	pkg = 'id_profiles'
	os.chdir('%s/id_profiles' % (cwd))

	# Ensure output folder exists
	if not os.path.exists('%s/id_profiles/cdf' % (cwd)):
		os.makedirs('%s/id_profiles/cdf' % (cwd))

	wrapper(pkg, 'all_profiles', 'main', profiles)

if __name__ == '__main__':
	run_conversion()
	run_cloudtracker()
	run_profiler()
	#run_id_profiles()
	
	print 'Entrainment analysis completed'
	
