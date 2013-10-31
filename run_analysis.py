import glob, os, sys
sys.path.append(os.getcwd() + '/lib/')
sys.path.append(os.getcwd() + '/cloudtracker/')

import model_param as mc
	
if __name__ == '__main__':
	### File conversion (.bin3d -> netCDF)
	from conversion import *
	#convert.main()
	
	# generate_tracking
	filelist = glob.glob('%s/variables/*.nc' % mc.data_directory)
	filelist.sort()
	nt = len(filelist)

	#for time_step, filename in enumerate(filelist):
	#	print "time_step: " + str(time_step)
	#	generate_tracking.main(time_step, filename)
	
	### Cloudtracker
	from cloudtracker import main
	# Change the working directory for cloudtracker
	os.chdir('./cloudtracker')
	
	model_config = mc.model_config
	
	model_config['input_directory'] = model_config['data_directory'] + 'tracking/'
	main.main(model_config)
	
	# Return to entrainment analysis directory
	os.chdir('../')	
	
	### Additional Profiles