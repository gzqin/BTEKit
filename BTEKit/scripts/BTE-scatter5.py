#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# BTE.scatter
#
# Calculate the scatter rate of each mode by each mode, such as:
#   ZA+ZA->ZA, ZA+TA->O, LA->O+TA
#   1  1   1   1  2   0  3   0 2
#
# Written BY QIN, GuangZhao <qin.phys@gmail.com>
# 2015-11-05

import os
import sys
import math

scatter_file = 'BTE.scatter'
omega_file = 'BTE.omega'
qpoints_file = 'BTE.qpoints'

#name={0: 'O', 1: 'ZA', 2: 'TA/LA'}
#name={0: 'O', 1: 'ZA', 2: 'TA', 3: 'LA', 4: 'TOz', 5: 'TOx', 6: 'LOy'}
name={0: 'O', 1: 'FA', 2: 'TA', 3: 'LA', 4: 'FO', 5: 'TO', 6: 'LO'}

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

NK = len(omega_data)-1              # number of qpoints
nband = len(omega_data[0].split())  # nband = 3 x N_atoms

class DATA:
    def __init__(self):
        self.pol = 0                # polization
        self.omega = 0              # frequency (THz)
        self.q = [ 0 for i in range(3) ]    # qx qy qz
        # absorption scattering rate
        self.plus = [ [ 0.0 for j in range(len(name)) ] for i in range(len(name)) ]
        # emission scattering rate
        self.minus = [ [ 0.0 for j in range(len(name)) ] for i in range(len(name)) ]
  
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
    # +/-: Gamma_plus(absorption)/Gamma_minus(emission)
    # w + w1 = w2  / w - w1 = w2
    # 'band' and 'k' of w/w1/w2
    line = scatter_data[i].split()
    pol1 = int(line[3])
    pol2 = int(line[5])
    # translate to the position in name space: name[pol1] name[pol2]
    # name={0: 'O', 1: 'FA', 2: 'TA', 3: 'LA', 4: 'FO', 5: 'TO', 6: 'LO'}
    if pol1 >= 7:
        pol1 = 0
    #
    if pol2 >= 7:
        pol2 = 0

    if line[0] == '+':
        scatter[int(line[2])-1][int(line[1])-1].plus[pol1][pol2] = \
            scatter[int(line[2])-1][int(line[1])-1].plus[pol1][pol2] + float(line[7])
    elif line[0] == '-':
        scatter[int(line[2])-1][int(line[1])-1].minus[pol1][pol2] = \
            scatter[int(line[2])-1][int(line[1])-1].minus[pol1][pol2] + float(line[7])

# ===========
# OUTPUT DATA
# ===========

# Output the anharmonic scattering rate that is same as BTE.w_anharmonic
#for i in range(NK):
#    for j in range(nband):
#        scatt = 0
#        for l in range(len(name)):
#            for m in range(len(name)):
#                scatt = scatt + scatter[i][j].plus[l][m]
#        for l in range(len(name)):
#            for m in range(len(name)):
#                scatt = scatt + scatter[i][j].minus[l][m]
#        print scatt,
#    print

print( '#pol omega qx qy qz scatt absorption emission', )  # COMMENT LINE
for l in range(len(name)):
    for m in range(len(name)):
        print( 'X+'+name[l]+'->'+name[m],)
for l in range(len(name)):
    for m in range(len(name)):
        print( 'X->'+name[l]+'+'+name[m],)
print

# output data
for i in range(NK):
    for j in range(nband):
        print( scatter[i][j].pol,)
        print( scatter[i][j].omega,)

        for k in range(3):              # qx qy qz
            print( scatter[i][j].q[k],)

        scatt_plus = 0
        for l in range(len(name)):
            for m in range(len(name)):
                scatt_plus = scatt_plus + scatter[i][j].plus[l][m]
        scatt_minus = 0
        for l in range(len(name)):
            for m in range(len(name)):
                scatt_minus = scatt_minus + scatter[i][j].minus[l][m]
                if l != m:              # X->ZA+TA, X->TA+ZA equals to each other
                    scatter[i][j].minus[l][m] = 2*scatter[i][j].minus[l][m]
        print (scatt_plus+scatt_minus,)   # scatt
        print (scatt_plus,)               # absorption
        print (scatt_minus,)              # emission

        # corresponding to: name[l] name[m]
        for l in range(len(name)):      # absorption O->O O->1 O->2 O->3 1->O 1->1 ...
            for m in range(len(name)):
                print (scatter[i][j].plus[l][m],)
        for l in range(len(name)):      # emission ->O+O ->O+1 ->O+2 ->O+3 ->1+O ->1+1 ...
            for m in range(len(name)):
                print (scatter[i][j].minus[l][m],)
        print
