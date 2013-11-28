#!/usr/bin/env python

from netCDF4 import Dataset
import numpy
from thermo import SAM
import glob

import gcssarm as mc

def makechi(filename):
    key = int(filename.split('/')[-1].split('_')[-1].split('.')[0])
    print key

    condensedfile = Dataset('cdf/condensed_profile_%08d.nc' % key)
    envfile = Dataset('cdf/condensed_env_profile_%08d.nc' % key)
    shellfile = Dataset('cdf/condensed_shell_profile_%08d.nc' % key)
    statfile = Dataset('%s/stat_1min.nc' % mc.data_dir)
 
    t = numpy.atleast_1d(condensedfile.variables['ids'][:])

    cloud_duration = len(t)
    n = len(t)

    z = envfile.variables['z'][:]
    p = statfile.variables['PRES'][0,:]*100.

    area_condensed = numpy.atleast_2d(condensedfile.variables['AREA'][:])

    thetal_condensed = numpy.atleast_2d(condensedfile.variables['THETAL'][:])
    qt_condensed = numpy.atleast_2d(condensedfile.variables['QT'][:])
    ql_condensed = numpy.atleast_2d(condensedfile.variables['QN'][:])
    T_condensed = numpy.atleast_2d(condensedfile.variables['TABS'][:])

    thetal_env = numpy.atleast_2d(envfile.variables['THETAL'][:]) 
    qt_env = numpy.atleast_2d(envfile.variables['QT'][:]) 
    thetal_shell = numpy.atleast_2d(shellfile.variables['THETAL'][:])
    qt_shell = numpy.atleast_2d(shellfile.variables['QT'][:])
    
    mask = ~(area_condensed > 0.)
    
    thetal_condensed_mask = numpy.ma.array(thetal_condensed, mask=mask)
    qt_condensed_mask = numpy.ma.array(qt_condensed, mask=mask)
    ql_condensed_mask = numpy.ma.array(ql_condensed, mask=mask)
    T_condensed_mask = numpy.ma.array(T_condensed, mask=mask)

    thetal_env_mask = numpy.ma.array(thetal_env, mask=mask) 
    qt_env_mask = numpy.ma.array(qt_env, mask=mask) 
    thetal_shell_mask = numpy.ma.array(thetal_shell, mask=mask)
    qt_shell_mask = numpy.ma.array(qt_shell, mask=mask)

    chi = SAM.find_chi_ql(ql_condensed, 
                          thetal_condensed, thetal_env, 
                          qt_condensed, qt_env, 
                          T_condensed, p)
                          
    chi_mean = SAM.find_chi_ql(ql_condensed_mask.mean(0),
                               thetal_condensed_mask.mean(0), 
                               thetal_env_mask.mean(0), 
                               qt_condensed_mask.mean(0), 
                               qt_env_mask.mean(0), 
                               T_condensed_mask.mean(0), 
                               p)

    chi_mean_condensed = SAM.find_chi_ql(ql_condensed_mask.mean(0),
                                  thetal_condensed_mask.mean(0), 
                                  thetal_env, 
                                  qt_condensed_mask.mean(0), qt_env, 
                                  T_condensed_mask.mean(0), p)

    chi_mean_env = SAM.find_chi_ql(ql_condensed,
                                  thetal_condensed, thetal_env_mask.mean(0), 
                                  qt_condensed, qt_env_mask.mean(0), 
                                  T_condensed, p)

#    chi[isnan(chi)] = 0.

    savefile = Dataset('cdf/condensed_chi_profile_%08d.nc' % key, 'w', format='NETCDF3_64BIT')
    savefile.createDimension('id', cloud_duration)
    savefile.createDimension('z', len(z))
    var_t = savefile.createVariable('id', 'd', ('id',))
    var_z = savefile.createVariable('z', 'd', ('z',))
    var_chi = savefile.createVariable('chi', 'd', ('id', 'z'))
    var_chi_mean = savefile.createVariable('chi_mean', 'd', ('id', 'z'))
    var_chi_mean_env = savefile.createVariable('chi_mean_env', 'd', ('id', 'z'))
    var_chi_mean_condensed = savefile.createVariable('chi_mean_condensed', 'd', ('id', 'z'))

    var_t[:] = t
    var_z[:] = z
    var_chi[:] = chi
    var_chi_mean[:] = chi_mean*(~mask)
    var_chi_mean_condensed[:] = chi_mean_condensed*(~mask)
    var_chi_mean_env[:] = chi_mean_env*(~mask)


    condensedfile.close()
    envfile.close()
    shellfile.close()
    statfile.close()

    savefile.close()


if __name__ == '__main__':
    filelist = glob.glob('cdf/condensed_env*.nc')
    filelist.sort()

    for filename in filelist:
        makechi(filename)

