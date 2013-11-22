import sys, os, glob
from netCDF4 import Dataset as data

profile = 'core' # Profile name
vars = {'ids', 't', 'z', 'AREA'} # Target variables

# Configure filelist from time_profiles
filelist = glob.glob('../time_profiles/cdf/%s_profile_*.nc' % (profile))
nt = len(filelist)

def initialize():
	savefile=data('cdf/%s_profile_aggregate.nc' % profile, 'w', format='NETCDF4')
	
	savefile.createDimension('ids', None)
	savefile.createDimension('t', None)
	savefile.createDimension('z', 144)
	
	for name in vars:
		if name not in ('ids', 't', 'z'):
			savefile.createVariable(name, 'd', ('ids', 't', 'z'))
	
	savefile.close()

def get_data(time):
	# Open file
	ncfile = data('../time_profiles/cdf/%s_profile_%08d.nc' % (profile, time))
	savefile=data('cdf/%s_profile_aggregate.nc' % profile, 'a')
	
	print '../time_profiles/cdf/%s_profile_%08d.nc' % (profile, time), "\n"
	
	for name in ncfile.variables:
		if name not in ('ids', 'z') and name in (vars):
			for ids in range (len(ncfile.variables['ids'][:])):
				savefile.variables[name][ids, time, :] = ncfile.variables[name][ids, :]
	
	# Close file
	ncfile.close()
	savefile.close()

def main():	
	initialize()
	
	# If needed, parallelize following loop
	for time in range(nt):
		print "Processing data at time: ", time + 1, "/", nt
		get_data(time)
	
if __name__ == "__main__":
	main()
