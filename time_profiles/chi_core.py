#!/usr/bin/env python

from netCDF4 import Dataset
import numpy
from thermo import SAM
import glob

import bomex as mc

def makechi(filename):
    key = int(filename.split('/')[-1].split('_')[-1].split('.')[0])
    print key

    corefile = Dataset('cdf/core_profile_%08d.nc' % key)
    envfile = Dataset('cdf/core_env_profile_%08d.nc' % key)
    #shellfile = Dataset('cdf/core_shell_profile_%08d.nc' % key)
    statfile = Dataset('%s/stat_1min.nc' % mc.data_dir)
 
    t = numpy.atleast_1d(corefile.variables['ids'][:])

    cloud_duration = len(t)
    n = len(t)

    z = envfile.variables['z'][:]
    p = statfile.variables['PRES'][0,:]*100.
    thetav_mean = statfile.variables['THETAV'][int(key), :]

    area_core = numpy.atleast_2d(corefile.variables['AREA'][:])

    thetal_core = numpy.atleast_2d(corefile.variables['THETAL'][:])
    thetav_core = numpy.atleast_2d(corefile.variables['THETAV'][:])
    qt_core = numpy.atleast_2d(corefile.variables['QT'][:])
    ql_core = numpy.atleast_2d(corefile.variables['QN'][:])
    T_core = numpy.atleast_2d(corefile.variables['TABS'][:])
#    p = numpy.atleast_2d(corefile.variables['PRES'][:])

    thetal_env = numpy.atleast_2d(envfile.variables['THETAL'][:])
    qt_env = numpy.atleast_2d(envfile.variables['QT'][:])
     
#    thetal_shell = numpy.atleast_2d(shellfile.variables['THETAL'][:])
#    qt_shell = numpy.atleast_2d(shellfile.variables['QT'][:])
    
    mask = ~(area_core > 0.)
    
    thetal_core_mask = numpy.ma.array(thetal_core, mask=mask)
    thetav_core_mask = numpy.ma.array(thetav_core, mask=mask)
    qt_core_mask = numpy.ma.array(qt_core, mask=mask)
    ql_core_mask = numpy.ma.array(ql_core, mask=mask)
    T_core_mask = numpy.ma.array(T_core, mask=mask)

    thetal_env_mask = numpy.ma.array(thetal_env, mask=mask)
    qt_env_mask = numpy.ma.array(qt_env, mask=mask)
 
#    thetal_shell_mask = numpy.ma.array(thetal_shell, mask=mask)
#    qt_shell_mask = numpy.ma.array(qt_shell, mask=mask)

    chi_theta = SAM.find_chi_theta(thetal_core, thetal_env, 
                                   thetav_core, thetav_mean, 
                                   qt_core, qt_env, 
                                   T_core, p)
    
    chi_theta_mean = SAM.find_chi_theta(thetal_core_mask.mean(0), thetal_env_mask.mean(0), 
                                  thetav_core_mask.mean(0), thetav_mean, 
                                  qt_core_mask.mean(0), qt_env_mask.mean(0), 
                                  T_core_mask.mean(0), p)
    chi_theta_mean_core = SAM.find_chi_theta(thetal_core_mask.mean(0), thetal_env, 
                                  thetav_core_mask.mean(0), thetav_mean, 
                                  qt_core_mask.mean(0), qt_env, 
                                  T_core_mask.mean(0), p)
    chi_theta_mean_env = SAM.find_chi_theta(thetal_core, thetal_env_mask.mean(0), 
                                  thetav_core, thetav_mean, 
                                  qt_core, qt_env_mask.mean(0), 
                                  T_core, p)

    chi_ql = SAM.find_chi_ql(ql_core,
                             thetal_core, thetal_env, 
                             qt_core, qt_env, 
                             T_core, p)
    chi_ql_mean = SAM.find_chi_ql(ql_core_mask.mean(0),
                                  thetal_core_mask.mean(0), thetal_env_mask.mean(0), 
                                  qt_core_mask.mean(0), qt_env_mask.mean(0), 
                                  T_core_mask.mean(0), p)
    chi_ql_mean_core = SAM.find_chi_ql(ql_core_mask.mean(0), 
                                  thetal_core_mask.mean(0), thetal_env, 
                                  qt_core_mask.mean(0), qt_env, 
                                  T_core_mask.mean(0), p)
    chi_ql_mean_env = SAM.find_chi_ql(ql_core,
                                  thetal_core, thetal_env_mask.mean(0), 
                                  qt_core, qt_env_mask.mean(0), 
                                  T_core, p)

#    chi[isnan(chi)] = 0.

    savefile = Dataset('cdf/core_chi_profile_%08d.nc' % key, 'w', format='NETCDF3_64BIT')
    savefile.createDimension('id', cloud_duration)
    savefile.createDimension('z', len(z))
    var_t = savefile.createVariable('id', 'd', ('id',))
    var_z = savefile.createVariable('z', 'd', ('z',))
    var_chi_theta = savefile.createVariable('chi_theta', 'd', ('id', 'z'))
    var_chi_theta_mean = savefile.createVariable('chi_theta_mean', 'd', ('id', 'z'))
    var_chi_theta_mean_env = savefile.createVariable('chi_theta_mean_env', 'd', ('id', 'z'))
    var_chi_theta_mean_core = savefile.createVariable('chi_theta_mean_core', 'd', ('id', 'z'))
    var_chi_ql = savefile.createVariable('chi_ql', 'd', ('id', 'z'))
    var_chi_ql_mean = savefile.createVariable('chi_ql_mean', 'd', ('id', 'z'))
    var_chi_ql_mean_env = savefile.createVariable('chi_ql_mean_env', 'd', ('id', 'z'))
    var_chi_ql_mean_core = savefile.createVariable('chi_ql_mean_core', 'd', ('id', 'z'))


    var_t[:] = t
    var_z[:] = z
    var_chi_theta[:] = chi_theta
    var_chi_theta_mean[:] = chi_theta_mean*(~mask)
    var_chi_theta_mean_core[:] = chi_theta_mean_core*(~mask)
    var_chi_theta_mean_env[:] = chi_theta_mean_env*(~mask)
    var_chi_ql[:] = chi_ql
    var_chi_ql_mean[:] = chi_ql_mean*(~mask)
    var_chi_ql_mean_core[:] = chi_ql_mean_core*(~mask)
    var_chi_ql_mean_env[:] = chi_ql_mean_env*(~mask)


    corefile.close()
    envfile.close()
    #shellfile.close()
    statfile.close()

    savefile.close()


if __name__ == '__main__':
    filelist = glob.glob('cdf/core_env*.nc')
    filelist.sort()

    for filename in filelist:
        makechi(filename)

