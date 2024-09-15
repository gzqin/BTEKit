#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# BTE.omega  
#               BTE.w_final
#               BTE.P3
# 频率          散射率
#               相空间
#
# Written BY QIN GuangZhao <gyty@163.com>
# 2015-04-30
#
# ====================================================
#
# ZA-frequency RelaxationTime TA-frequency RelaxationTime LA-frequency RelaxationTime ...
#
# ====================================================

import os
import sys
import math

omega_file = 'BTE.omega'                 # 频率
quantity_file = 'BTE.gruneisen'                   # Gruneisen parameter

# ========
# 读入数据
# ========
omega = open(omega_file)
quantity = open(quantity_file)
omega_data = omega.read().split('\n')
quantity_data = quantity.read().split('\n')
omega.close()
quantity.close()

# ========
# 输出数据
# ========
NK=len(omega_data)-1
nband=len(omega_data[0].split())

gruneisen=[ 0 for i in range(nband) ]
for i in range(1, NK):
    for j in range(0, nband):
        print('%20.15f %20.15f' %(float(omega_data[i].split()[j]) / 2 / math.pi, float(quantity_data[i].split()[j]))),
        print

#        gruneisen[j]=gruneisen[j]+float(quantity_data[i].split()[j])
#for j in range(0, nband):
#    print gruneisen[j]/NK,
#print

