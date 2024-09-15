#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# BTE.scatter
#
# Calculate the scatter rate of absorption, emission, N and U process 
#
# Written BY QIN, GuangZhao <qin.phys@gmail.com>
# 2016-11-01

import os
import sys
import math

scatter_file = 'BTE.scatter'
omega_file = 'BTE.omega'
qpoints_file = 'BTE.qpoints'                # for the scattered phonon mode: k0
qpoints_file_full = 'BTE.qpoints_full'      # for the other two phonon modes involved in the scattering process: k1 k2

# =========
# READ DATA
# =========

scatter = open(scatter_file)    # scatter
scatter_data = scatter.read().split('\n')
scatter.close()
omega = open(omega_file)        # omega
omega_data = omega.read().split('\n')
omega.close()
qpoints = open(qpoints_file)    # qpoints
qpoints_data = qpoints.read().split('\n')
qpoints.close()
qpoints_full = open(qpoints_file_full)    # qpoints
qpoints_data_full = qpoints_full.read().split('\n')
qpoints_full.close()

NK = len(omega_data)-1              # number of qpoints
nband = len(omega_data[0].split())  # nband = 3 x N_atoms

class DATA:
    def __init__(self):
        self.pol = 0                # polization
        self.omega = 0              # frequency (THz)
        self.q = [ 0 for i in range(3) ]    # qx qy qz
        # absorption scattering rate
        self.plus = 0
        # emission scattering rate
        self.minus = 0
        # N process
        self.N = 0
        # U process
        self.U = 0


scatter = [ [ DATA() for j in range(nband) ] for i in range(NK) ]

# Set the pol, omega and q[xyz] of each mode
for i in range(NK):
    omega = omega_data[i].split()
    qpoints = qpoints_data[i].split()
    for j in range(nband):
        pol = j+1
        scatter[i][j].pol = pol              # pol
        scatter[i][j].omega = float(omega[j]) / 2 / math.pi
        scatter[i][j].q[0] = qpoints[2]       # qx
        scatter[i][j].q[1] = qpoints[3]       # qy
        scatter[i][j].q[2] = qpoints[4]       # qz

# Summarize the scattering rate of each process
for i in range(len(scatter_data)-1):
    # 0    1    2 3     4  5     6  7
    # +/-  band k band1 k1 band2 k2 scattering_rate
    #   +/-: Gamma_plus(absorption)/Gamma_minus(emission)
    #   w + w1 = w2  / w - w1 = w2
    #   'band' and 'k' of w/w1/w2
    line = scatter_data[i].split()
    b0=int(line[1])-1
    k0=int(line[2])-1
    b1=int(line[3])-1
    k1=int(line[4])-1
    b2=int(line[5])-1
    k2=int(line[6])-1

    coor0=qpoints_data[k0].split()
    coor1=qpoints_data_full[k1].split()
    coor2=qpoints_data_full[k2].split()

    if line[0] == '+':
        x=float(coor2[2])-float(coor1[2])-float(coor0[2])
        y=float(coor2[3])-float(coor1[3])-float(coor0[3])
        z=float(coor2[4])-float(coor1[4])-float(coor0[4])
        scatter[k0][b0].plus = scatter[k0][b0].plus + float(line[7])
    elif line[0] == '-':
        x= float(coor2[2])+float(coor1[2])-float(coor0[2])
        y= float(coor2[3])+float(coor1[3])-float(coor0[3])
        z= float(coor2[4])+float(coor1[4])-float(coor0[4])
        scatter[k0][b0].minus = scatter[k0][b0].minus + float(line[7])
    q_dis=math.sqrt(x*x+y*y+z*z)
    if abs(q_dis) < 1e-5:
        scatter[k0][b0].N = scatter[k0][b0].N + float(line[7])
    else:
        scatter[k0][b0].U = scatter[k0][b0].U + float(line[7])
#    print line
#    print coor0
#    print coor1
#    print coor2
#    print x,y,z,q_dis
#    print

# ===========
# OUTPUT DATA
# ===========

print( '#pol omega qx qy qz scatt absorption emission N U')   # COMMENT LINE

# output data
for i in range(NK):
    for j in range(nband):
        print (scatter[i][j].pol,)
        print (scatter[i][j].omega,)

        for k in range(3):              # qx qy qz
            print (scatter[i][j].q[k],)

        print (scatter[i][j].plus+scatter[i][j].minus,)   # scatt
        print (scatter[i][j].plus, )                      # absorption
        print (scatter[i][j].minus, )                     # emission
        print (scatter[i][j].N, )                         # N process
        print( scatter[i][j].U, )                         # U process
        print
