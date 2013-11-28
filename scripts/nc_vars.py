import sys, os, glob
from netCDF4 import Dataset as data

profile = 'core' 
vars = ['ids', 't', 'z', 'AREA', 'PRES', 'TABS']
ent_vars = ['MFTETCOR', 'ETETCOR', 'DTETCOR']

# Configure filelist from time_profiles
filelist = glob.glob('../time_profiles/cdf/%s_profile_*.nc' % (profile))
nt = len(filelist)

def initialize():
	savefile=data('cdf/%s_profile_data.nc' % profile, 'w', format='NETCDF3_64BIT')
	
	savefile.createDimension('ids', None)
	savefile.createDimension('t', nt)
	savefile.createDimension('z', 128)
	
	for name in vars:
		if name not in ('ids', 't', 'z'):
			print "Created variable \"", name, "\""
			savefile.createVariable(name, 'd', ('ids', 't', 'z'))
			
	for name in ent_vars:
		if name not in ('ids', 't', 'z'):
			print "Created variable \"", name, "\""
			savefile.createVariable(name, 'd', ('ids', 't', 'z'))

def get_data(time):
	print 'Opening data files...\n'
	
	# Open file
	nc_file = data('../time_profiles/cdf/%s_profile_%08d.nc' % (profile, time))
	savefile=data('cdf/%s_profile_data.nc' % profile, 'a')
	
	print '../time_profiles/cdf/%s_profile_%08d.nc' % (profile, time), "\n"
	
	## Core profile
	for name in vars:
		if name not in ('ids', 't', 'z') and name in (vars):
			savefile.variables[name][:, time, :] = \
				nc_file.variables[name][:, :128]
				
	nc_file.close()
	
	ent_file = data('../time_profiles/cdf/%s_entrain_profile_%08d.nc' % (profile, time))
	
	## Core entrainment profile
	for name in ent_vars:
		if name not in ('ids', 't', 'z') and name in (ent_vars):
			savefile.variables[name][:, time, :] = \
				ent_file.variables[name][:, :128]
	
	ent_file.close()
	savefile.close()

def main():	
	initialize()
	
	# If needed, parallelize following loop
	for time in range(nt):
		print "Processing data at time: ", time , "/", nt - 1
		get_data(time)
	
if __name__ == "__main__":
	main()
