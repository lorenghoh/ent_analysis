#!/usr/bin/env python
import numpy

from thermo import SAM
import model_param as mc

def area(data, k, j, i):
    return float(len(i))*mc.dx*mc.dy

def qn(data, k, j, i):
    return data['QN'][k, j, i].mean()/1000.

def qv(data, k, j, i):
    return data['QV'][k, j, i].mean()/1000.

def tabs(data, k, j, i):
    return data['TABS'][k, j, i].mean()

def qt(data, k, j, i):
    return (data['QN'][k, j, i] + data['QV'][k, j, i]).mean()/1000.

def u(data, k, j, i):
    return data['U'][k, j, i].mean()

def v(data, k, j, i):
    return data['V'][k, j, i].mean()

def tke(data, k, j, i):
    return data['TKE'][k, j, i].mean()

def tr01(data, k, j, i):
    return data['TR01'][k, j, i].mean()

def w(data, k, j, i):
    kk = min(k+1, (mc.nz-1))
    return (data['W'][k, j, i] + data['W'][kk, j, i]).mean()/2.

def dw_dz(data, k, j, i):
    kk = min(k+1, (mc.nz-1))
    return (data['W'][kk, j, i].mean() - data['W'][k, j, i].mean())/mc.dz

def wqreyn(data, k, j, i):
    kk = min(k+1, (mc.nz-1))
    w = (data['W'][k, j, i] + data['W'][kk, j, i])/2.
    q = (data['QV'][k, j, i] + data['QN'][k, j ,i])
    wq_reyn = (w*q - w.mean()*q.mean())
    return wq_reyn.mean()

def wwreyn(data, k, j, i):
    kk = min(k+1, (mc.nz-1))
    w = (data['W'][k, j, i] + data['W'][kk, j, i])/2.
    ww_reyn = (w*w - w.mean()**2)
    return ww_reyn.mean()

def dp_dz(data, k, j, i):
    kplus = min(k+1, (mc.nz-1))
    kminus = max(k-1, 0)
    return (data['PP'][kplus, j, i] - data['PP'][kminus, j, i]).mean()/2/mc.dz
     
def thetav(data, k, j, i):
    return SAM.theta_v(data['p'][k, numpy.newaxis, numpy.newaxis]*100., 
                       data['TABS'][k, j, i], 
                       data['QV'][k, j, i]/1000., 
                       data['QN'][k, j, i]/1000., 0.).mean()
    
def thetav_lapse(data, k, j, i):
    dp_dz = (data['p'][k+1]-data['p'][k-1])*100./mc.dz/2.
    return SAM.density_theta_lapse_rate(
                       data['TABS'][k, j, i].mean(), 
                       data['p'][k]*100., 
                       data['QV'][k, j, i].mean()/1000., 
                       data['QN'][k, j, i].mean()/1000., 
                       0.,
                       dp_dz)
    
def thetal(data, k, j, i):
    return SAM.theta_l(data['p'][k, numpy.newaxis, numpy.newaxis]*100., 
                       data['TABS'][k, j, i], 
                       data['QN'][k, j, i]/1000., 0.).mean()
    
def mse(data, k, j, i):
    return SAM.h(data['TABS'][k, j, i],
                 data['z'][k, numpy.newaxis, numpy.newaxis],
                 data['QN'][k, j, i]/1000., 0.).mean()

def rho(data, k, j, i):
    return data['RHO'][k]

def press(data, k, j, i):
    return data['p'][k]*100.

def dwdt(data, k, j, i):
    return data['DWDT'][k, j, i].mean()

def etetcor(data, k, j, i):
    return data['ETETCOR'][k, j, i].sum()*mc.dx*mc.dy

def dtetcor(data, k, j, i):
    return data['DTETCOR'][k, j, i].sum()*mc.dx*mc.dy

def eqtetcor(data, k, j, i):
    return data['EQTETCOR'][k, j, i].sum()*mc.dx*mc.dy

def dqtetcor(data, k, j, i):
    return data['DQTETCOR'][k, j, i].sum()*mc.dx*mc.dy

def ettetcor(data, k, j, i):
    return data['ETTETCOR'][k, j, i].sum()*mc.dx*mc.dy

def dttetcor(data, k, j, i):
    return data['DTTETCOR'][k, j, i].sum()*mc.dx*mc.dy

def ewtetcor(data, k, j, i):
    return data['EWTETCOR'][k, j, i].sum()*mc.dx*mc.dy

def dwtetcor(data, k, j, i):
    return data['DWTETCOR'][k, j, i].sum()*mc.dx*mc.dy

def vtetcor(data, k, j, i):
    return data['VTETCOR'][k, j, i].sum()*mc.dx*mc.dy

def mftetcor(data, k, j, i):
    return data['MFTETCOR'][k, j, i].sum()*mc.dx*mc.dy

def etetcld(data, k, j, i):
    return data['ETETCLD'][k, j, i].sum()*mc.dx*mc.dy

def dtetcld(data, k, j, i):
    return data['DTETCLD'][k, j, i].sum()*mc.dx*mc.dy

def eqtetcld(data, k, j, i):
    return data['EQTETCLD'][k, j, i].sum()*mc.dx*mc.dy

def dqtetcld(data, k, j, i):
    return data['DQTETCLD'][k, j, i].sum()*mc.dx*mc.dy

def ettetcld(data, k, j, i):
    return data['ETTETCLD'][k, j, i].sum()*mc.dx*mc.dy

def dttetcld(data, k, j, i):
    return data['DTTETCLD'][k, j, i].sum()*mc.dx*mc.dy

def ewtetcld(data, k, j, i):
    return data['EWTETCLD'][k, j, i].sum()*mc.dx*mc.dy

def dwtetcld(data, k, j, i):
    return data['DWTETCLD'][k, j, i].sum()*mc.dx*mc.dy

def vtetcld(data, k, j, i):
    return data['VTETCLD'][k, j, i].sum()*mc.dx*mc.dy*mc.dz

def mftetcld(data, k, j, i):
    return data['MFTETCLD'][k, j, i].sum()*mc.dx*mc.dy*mc.dz

