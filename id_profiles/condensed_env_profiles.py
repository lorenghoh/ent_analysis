#!/usr/bin/env python
#Runtime (690, 130, 128, 128): 3 hours 40 minutes


import sys
from pylab import *
import numpy
#import pcontour
import cPickle
import glob
from netCDF3 import Dataset
import networkx

from thermo import SAM

import os
model_name = os.getcwd().split('/ANALYSIS/')[-1].split('/')[0]
MC = __import__(model_name)

def main(item):

    created_file_ids = []
    for t in range(MC.nt):
        ncfile = Dataset('../TIME_PROFILES/cdf/%s_profile_%08d.nc' % (item, t))

        ids = ncfile.variables['ids'][:]
        z = ncfile.variables['z'][:]
        
        
        for n, id in enumerate(ids):
            id = int(id)
            print "time: ", t, " id: ", id
            if id not in created_file_ids:
                savefile = Dataset('cdf/%s_profile_%08d.nc' % (item, id), 'w')
                
                # Create savefile
                savefile.createDimension('t', None)
                savefile.createDimension('z', len(z))

                tsavevar = savefile.createVariable('t', 'd', ('t',))
                tsavevar[0] = t
                zsavevar = savefile.createVariable('z', 'd', ('z',))
                zsavevar[:] = z[:]

                for name in ncfile.variables:
                    if name not in ('ids', 'z'):
                        new_variable = savefile.createVariable(name, 'd', ('t', 'z'))
                        new_variable[0, :] = ncfile.variables[name][n, :]
                savefile.close()
                created_file_ids.append(id)
            else:
                savefile = Dataset('cdf/%s_profile_%08d.nc' % (item, id), 'a')
                tvar = savefile.variables['t']
                l = len(tvar)
                tvar[l] = t
                for name in ncfile.variables:
                    if name not in ('ids', 'z'):
                        savefile.variables[name][l, :] = ncfile.variables[name][n, :]
                savefile.close()
                                
        ncfile.close()
   
if __name__ == "__main__":
    for item in ('cloud_env',):
        main(item)
