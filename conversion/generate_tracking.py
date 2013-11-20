#!/usr/bin/env python
"""
This program generates a pkl file containing a list of dictionaries.
Each dictionary in the list represents a cloudlet.
The dictionaries have the structure:
{'core': array of ints of core points,
'plume': array of ints of plume points,
'u_core': ,
'v_core': ,
'w_core': ,
'u_plume': ,
'v_plume': ,
'w_plume': }
pkl files are saved in cf/ subdirectory indexed by time
"""

import numpy
import cPickle
import sys
from pylab import *
from netCDF4 import Dataset
import glob

from thermo import SAM
import model_param as mc

def main(filename):
    time_step = mc.time_parser(filename)
    
    # Load all the data needed to calculation core, clouds, updrafts, etc
    # at the current time_step.
    print "Loading Data..."

    nc_file = Dataset(filename)    
    tabs_field = nc_file.variables['TABS'][0,:].astype(double)
    qv_field = nc_file.variables['QV'][0,:].astype(double)/1000.
    qn_field = nc_file.variables['QN'][0,:].astype(double)/1000.
    p_field = nc_file.variables['p'][:].astype(double)*100.
    
    cloud_field = qn_field > 0.

    thetav_field = SAM.theta_v(p_field[:, numpy.newaxis, numpy.newaxis],
                               tabs_field, qv_field, qn_field, 0.)
                               
    buoy_field = (thetav_field > 
         (thetav_field.mean(2).mean(1))[:, numpy.newaxis, numpy.newaxis])

    u_field = nc_file.variables['U'][0,:].astype(double)
    u_field[:, :-1, :] += u_field[:, 1:, :]
    u_field[:, -1, :] += u_field[:, 0, :]
    u_field = u_field/2.

    v_field = nc_file.variables['V'][0,:].astype(double)
    v_field[:, :, :-1] += v_field[:, :, 1:]
    v_field[:, :, -1] += v_field[:, :, 0]
    v_field = v_field/2.

#    print "Load w"
    w_field = nc_file.variables['W'][0,:].astype(double)
    w_field[:-1, :, :] += w_field[1:, :, :]
    w_field[:-1, :, :] = w_field[:-1, :, :]/2.

    up_field = w_field > 0.

    core_field = up_field & buoy_field & cloud_field

#    print "Load plume"
    tr_field = nc_file.variables['TR01'][0,:].astype(double)
    x = nc_file.variables['x'][:].astype(double)
    y = nc_file.variables['y'][:].astype(double)
    z = nc_file.variables['z'][:].astype(double)

    tr_mean = tr_field.reshape((len(z), len(y)*len(x))).mean(1)
    tr_stdev = numpy.sqrt(tr_field.reshape((len(z), len(y)*len(x))).var(1))
    tr_min = .05*numpy.cumsum(tr_stdev)/(numpy.arange(len(tr_stdev))+1)
    
#    plume_field = (tr_field > numpy.max(numpy.array([tr_mean + tr_stdev, tr_min]), 0)[:, numpy.newaxis, numpy.newaxis]) & up_field
    plume_field = (tr_field > numpy.max(numpy.array([tr_mean + tr_stdev, tr_min]), 0)[:, numpy.newaxis, numpy.newaxis])

    save_file = Dataset('%s/tracking/cloudtracker_input_%08g.nc' % (mc.data_directory, time_step), 'w')
    
    save_file.createDimension('x', len(x))
    save_file.createDimension('y', len(y))
    save_file.createDimension('z', len(z))

    xvar = save_file.createVariable('x', 'f', ('x',))
    yvar = save_file.createVariable('y', 'f', ('y',))
    zvar = save_file.createVariable('z', 'f', ('z',))

    corevar = save_file.createVariable('core', 'i', ('z', 'y', 'x'))
    condvar = save_file.createVariable('condensed', 'i', ('z', 'y', 'x'))
    plumevar = save_file.createVariable('plume', 'i', ('z', 'y', 'x'))
    uvar = save_file.createVariable('u', 'f', ('z', 'y', 'x'))
    vvar = save_file.createVariable('v', 'f', ('z', 'y', 'x'))
    wvar = save_file.createVariable('w', 'f', ('z', 'y', 'x'))

    xvar[:] = x[:]
    yvar[:] = y[:]
    zvar[:] = z[:]

    corevar[:] = core_field[:]
    condvar[:] = cloud_field[:]
    plumevar[:] = plume_field[:]
    uvar[:] = u_field[:]
    vvar[:] = v_field[:]
    wvar[:] = w_field[:]
    
    save_file.close()
 
if __name__ == "__main__":
#    t0 = 0
#    dt = 7
    filelist = glob.glob('%s/variables/*.nc' % mc.data_directory)
    
    filelist.sort()
    nt = len(filelist)
    
    for time_step, filename in enumerate(filelist):
        print "time_step: " + str(time_step)
        main(filename)
        
#    if len(sys.argv) == 3:
#        t0 = int(sys.argv[1])
#        dt = int(sys.argv[2])
#    for time_step in range(t0, nt, dt):
#        print "-----------------"
#        print "time_step: " + str(time_step)
#        main(time_step)

