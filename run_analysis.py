import glob, os, sys
sys.path.append(os.getcwd() + '/lib/')

import model_param as mc
	
if __name__ == '__main__'
	### File conversion (.bin3d -> netCDF)
	from conversion import *
	# bin3d2nc
	#convert.main()

	# generate_tracking
	filelist = glob.glob('%s/variables/*.nc' % mc.data_directory)
	print mc.data_directory + 'variables/*.nc'

	filelist.sort()
	nt = len(filelist)

	for time_step, filename in enumerate(filelist):
		print "time_step: " + str(time_step)
		generate_tracking.main(time_step, filename)

	### Cloudtracker

	### Additional Profiles