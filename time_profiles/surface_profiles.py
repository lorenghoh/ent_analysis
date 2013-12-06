#!/usr/bin/env python
#Runtime (690, 130, 128, 128): 3 hours 40 minutes

from pylab import *
import numpy
import cPickle
from netCDF4 import Dataset
import sys, os

from thermo import SAM
import model_param as mc

# Load mean cloud field stat
stat_file = Dataset(mc.get_stat())
data = {'z': stat_file.variables['z'][:].astype(double),
    'RHO' : stat_file.variables['RHO'][0,:].astype(double),
    'PRES' : stat_file.variables['PRES'][0,:].astype(double)*100.}
stat_file.close()

def create_savefile(t, data, vars, profile_name):
    ids = data['ids'][:]
    z = data['z'][:]
    savefile = Dataset('cdf/%s_profile_%08d.nc' % (profile_name, t), 'w')
    
    # Create savefile
    savefile.createDimension('ids', len(ids))
    savefile.createDimension('z', len(z))

    tsavevar = savefile.createVariable('ids', 'd', ('ids',))
    tsavevar[:] = ids[:]
    zsavevar = savefile.createVariable('z', 'd', ('z',))
    zsavevar[:] = z[:]

    variables = {}
    for name in vars:
        variables[name] = savefile.createVariable(name, 'd', ('ids', 'z'))
        
    return savefile, variables

#--------------

def make_profiles(variables, cloud_data, vars, data, n):
    temp = {'core': 'CORE_SURFACE', 'condensed': 'CONDENSED_SURFACE'}
    
    for item in temp:                
        temp_profile = {}
        for name in vars:
            temp_profile[name] = zeros_like(data['z'][:])

        indexes = cloud_data[item]
        if len(indexes) > 0:
            indexes2 = indexes + mc.nx*mc.ny
            a = ~numpy.in1d(indexes, indexes2, assume_unique=True)
            indexes2 = indexes - mc.nx*mc.ny
            b = ~numpy.in1d(indexes, indexes2, assume_unique=True)
        
            z, y, x = mc.index_to_zyx(indexes)
        
            x2  = (x+1) % mc.nx
            indexes2 = mc.zyx_to_index(z, y, x2)
            c = ~numpy.in1d(indexes, indexes2, assume_unique=True)
            x2  = (x-1) % mc.nx
            indexes2 = mc.zyx_to_index(z, y, x2)
            d = ~numpy.in1d(indexes, indexes2, assume_unique=True)

            y2  = (y+1) % mc.ny
            indexes2 = mc.zyx_to_index(z, y2, x)
            e = ~numpy.in1d(indexes, indexes2, assume_unique=True)
            y2  = (y-1) % mc.ny
            indexes2 = mc.zyx_to_index(z, y2, x)
            f = ~numpy.in1d(indexes, indexes2, assume_unique=True)
            
            area = mc.dx*mc.dy*(a+b) + mc.dy*mc.dz*(c+d) + mc.dx*mc.dz*(e+f)

            for k in numpy.unique(z):
                mask = z == k
                temp_profile[temp[item]][k] = area[mask].sum()
            
        results = temp_profile       
                                               
        variables[temp[item]][n, :] = results[temp[item]]


#------------------

def main(t):
	vars = ('CORE_SURFACE', 'CONDENSED_SURFACE')

	# For each cloud, iterate over all times
	cloud_filename = '../cloudtracker/pkl/cloud_data_%08d.pkl' % t
	# Load the cloud data at that timestep
	clouds = cPickle.load(open(cloud_filename, 'rb'))

	ids = clouds.keys()
	ids.sort()

	data['ids'] = numpy.array(ids)

	# For each cloud, create a savefile for each profile
	savefile, variables = create_savefile(t, data, vars, 'surface')

	for n, id in enumerate(ids):
		print "time: ", t, " id: ", id
		# Select the current cloud id
		cloud = clouds[id]
		make_profiles(variables, cloud, vars, data, n)
            
        savefile.close()
