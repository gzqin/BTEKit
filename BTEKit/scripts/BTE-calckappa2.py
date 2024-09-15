#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# BTE.omega BTE.v BTE.w_final
#
# Modified from KMC-fromShengBTE.py
#
# Written BY QIN, GuangZhao <qin.phys@gmail.com>
# 2016-03-05

import os
import sys
import math

omega_file = 'BTE.omega'   # radial frequency
vel_file = 'BTE.v'         # group velocity
w_file = 'BTE.w_final'     # scattering rate (relaxation time)
q_file = 'BTE.qpoints'     # qpoints

# =========
# READ DATA
# =========

# ========
# 读入数据
# ========
omega = open(omega_file)        # omega
omega_data = omega.read().split('\n')
omega.close()
vel = open(vel_file)            # velocity
vel_data = vel.read().split('\n')
vel.close()
w = open(w_file)
w_data = w.read().split('\n')   # scattering
w.close()
q = open(q_file)
q_data = q.read().split('\n')   # qpoints
q.close()

# ===========
# OUTPUT DATA
# ===========

NK = len(omega_data)-1
nband = len(omega_data[0].split())
N = NK*nband

def dot(x,y):
  return x[0]*y[0] + x[1]*y[1] + x[2]*y[2]

def cross(x,y):
  z = [0.0 for i in range(3)]
  z[0] = x[1]*y[2] - x[2]*y[1];
  z[1] = x[2]*y[0] - x[0]*y[2];
  z[2] = x[0]*y[1] - x[1]*y[0];
  return z

class DATA:
    def __init__(self, pol, omega, tau, factor, vel_x, vel_y, vel_z):
        self.pol = int(pol)
        self.omega = float(omega) * 1e12        # rad/ps --> rad/s
        #self.omega = float(omega) / 2 / math.pi # rad/ps --> THz
        self.tau = 1 / float(tau) * 1e-12       # ps^{-1} --> s
        self.factor = int(factor)
        self.vel_x = abs(float(vel_x)) * 1e3    # km/s --> m/s
        self.vel_y = abs(float(vel_y)) * 1e3    # km/s --> m/s
        self.vel_z = abs(float(vel_z)) * 1e3    # km/s --> m/s
  
data = []

for i in range(1, NK):
    omega = omega_data[i].split()
    vel = vel_data[i].split()
    w = w_data[i].split()
    q = q_data[i].split()
    for j in range(0, nband):
#        if float(w[j]) <= 0:
#            continue        # Only count the positive value
        data.append(DATA(
                    j+1,                        # pol
                    omega[j],                   # omega
                    w[j],                       # tau
                    q[1],
                    vel[j+0*nband],             # vx
                    vel[j+1*nband],             # vy
                    vel[j+2*nband]              # vz
                    ))

# sort by omega
#data.sort(key=lambda data: data.omega)

#############################################################
# calculate V
a1 = [0.0 for i in range(3)]
a2 = [0.0 for i in range(3)]
a3 = [0.0 for i in range(3)]
fi_nb = open('CONTROL','r')
while True:
  line = fi_nb.readline()
  if len(line)==0:
    break
  if line.find('lfactor')!=-1:
    lfactor = float(line.split('=')[1].split()[0])
    continue
  if line.find('lattvec(:,1)')!=-1:
    a1[0] =  float(line.split('=')[1].split()[0])
    a1[1] =  float(line.split('=')[1].split()[1])
    a1[2] =  float(line.split('=')[1].split()[2].split(',')[0])
    continue
  if line.find('lattvec(:,2)')!=-1:
    a2[0] =  float(line.split('=')[1].split()[0])
    a2[1] =  float(line.split('=')[1].split()[1])
    a2[2] =  float(line.split('=')[1].split()[2].split(',')[0])
    continue
  if line.find('lattvec(:,3)')!=-1:
    a3[0] =  float(line.split('=')[1].split()[0])
    a3[1] =  float(line.split('=')[1].split()[1])
    a3[2] =  float(line.split('=')[1].split()[2].split(',')[0])
    continue
fi_nb.close()

n=0
fi_nq = open('BTE.qpoints_full','r')
while True:
  line = fi_nq.readline()
  if len(line)==0:
    break
  n+=1
fi_nq.close()
nq = n

nm    = 1.0e-9          # m
V = dot(cross(a1, a2), a3)*(lfactor*nm)**3
#
#V = V*float(nq)         # All the Q points as base
V = V*len(data)/nband   # Q points except the data with negative tau as base
#print len(data), nband, float(nq)


#############################################################
# calculate kappa
hBar = 1.05457173e-34
BOLTZ = 1.3806488e-23
PI = 3.1415926535897932384626433832795028841971693993751
Teq = 300
de_dT = 0.0
Cv = 0.0
kappa_x = 0.0
kappa_y = 0.0
kappa_z = 0.0
for i in range(len(data)):
    de_dT = hBar*data[i].omega/(2*BOLTZ*Teq)
    if (de_dT == 0):
        de_dT = 1
    else:
        de_dT = de_dT/math.sinh(de_dT)
        de_dT = BOLTZ*de_dT*de_dT
    C_mode = de_dT/V
    Cv = Cv + C_mode
#    kappa_x = kappa_x + C_mode*data[i].vel_x**2*data[i].tau
#    kappa_y = kappa_y + C_mode*data[i].vel_y**2*data[i].tau
#    kappa_z = kappa_z + C_mode*data[i].vel_z**2*data[i].tau
    kappa_x = kappa_x + C_mode*data[i].vel_x**2*data[i].tau*data[i].factor
    kappa_y = kappa_y + C_mode*data[i].vel_y**2*data[i].tau*data[i].factor
    kappa_z = kappa_z + C_mode*data[i].vel_z**2*data[i].tau*data[i].factor
print(kappa_x,)
print(kappa_y,)
print(kappa_z)
