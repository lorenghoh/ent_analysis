#!/usr/bin/env python

from pylab import *
import numpy
import cPickle
import glob
from netCDF4 import Dataset
import sys

from thermo import SAM
import var_calcs
import model_param as mc

#--------------

def make_profile(z_indexes, y_indexes, x_indexes,
                 data, vars, profiles):

    z = numpy.unique(z_indexes)
    for k in z:
        mask = (z_indexes == k)
        j = y_indexes[mask]
        i = x_indexes[mask]
        for name in vars:
            profiles[name][k] = vars[name](data, k, j, i)

    return profiles

#--------------

def index_to_zyx(index):
    ny, nx = mc.ny, mc.nx
    z = index / (ny*nx)
    index = index % (ny*nx)
    y = index / nx
    x = index % nx
    return numpy.array((z, y, x))

#--------------

def create_savefile(t, data, vars, profile_name):
    ids = data['ids'][:]
    z = data['z'][:]
    savefile = Dataset('cdf/%s_profile_%08d.nc' % (profile_name, t), 'w', format='NETCDF3_64BIT')
    
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

def make_profiles(profiles, cloud_data, vars, data, n):
    for item in ('condensed_entrain', ):
        variables = profiles[item]
                
        temp_profile = {}
        for name in vars:
            temp_profile[name] = ones_like(data['z'][:])*numpy.NaN

        indexes = cloud_data[item]
        if len(indexes) > 0:
            z, y, x = index_to_zyx(indexes)            
            results = make_profile(z, y, x,
                                   data, vars, temp_profile)
        else:
            results = temp_profile       
                                               
        for name in vars:
            variables[name][n, :] = results[name]


#------------------

def main(time, filename):
    vars = {
          'ETETCLD': var_calcs.etetcld,
          'DTETCLD': var_calcs.dtetcld,
          'EQTETCLD': var_calcs.eqtetcld,
          'DQTETCLD': var_calcs.dqtetcld,
          'ETTETCLD': var_calcs.ettetcld,
          'DTTETCLD': var_calcs.dttetcld,
          'EWTETCLD': var_calcs.ewtetcld,
          'DWTETCLD': var_calcs.dwtetcld,
          'VTETCLD': var_calcs.vtetcld,
          'MFTETCLD': var_calcs.mftetcld,
    }
    
    # Load CDF Files
    nc_file = Dataset(filename)
    stat_file = Dataset('%s/stat_1min.nc' % mc.data_directory)

    data = {'z': stat_file.variables['z'][:].astype(double),
            'RHO' : stat_file.variables['RHO'][time,:].astype(double),
            'PRES' : stat_file.variables['PRES'][time,:].astype(double)*100.}
    stat_file.close()

    # For each cloud, iterate over all times
    cloud_filename = '../cloudtracker/pkl/cloud_data_%08d.pkl' % time
    # Load the cloud data at that timestep
    clouds = cPickle.load(open(cloud_filename, 'rb'))
        
    ids = clouds.keys()
    ids.sort()
        
    data['ids'] = numpy.array(ids)
    for name in ('ETETCLD', 'DTETCLD',
                 'EQTETCLD', 'DQTETCLD',
                 'ETTETCLD', 'DTTETCLD',
                 'EWTETCLD', 'DWTETCLD',
                 'VTETCLD', 'MFTETCLD'):
        data[name] = nc_file.variables[name][0, :].astype(numpy.double)
                
    # For each cloud, create a savefile for each profile
    savefiles = {}
    profiles = {}
    for item in ('condensed_entrain',):
        savefile, variables = create_savefile(time, data, vars, item)
        savefiles[item] = savefile
        profiles[item] = variables
        
    for n, id in enumerate(ids):
        print "time: ", time, " id: ", id
        # Select the current cloud id
        cloud = clouds[id]
        cloud['condensed_entrain'] = numpy.hstack([cloud['condensed'], cloud['condensed_shell']])

        make_profiles(profiles, cloud, vars, data, n)
            
    for savefile in savefiles.values():
        savefile.close()

    nc_file.close()
   
if __name__ == "__main__":

    files = glob.glob('%s/condensed_entrain/*.nc' % mc.data_directory)
    files.sort()
    
    for time, filename in enumerate(files):
        main(time, filename)
