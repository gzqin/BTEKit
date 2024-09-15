#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# BTE.omega  BTE.w_final
# 散射率 - 频率
#
# Written BY QIN GuangZhao <gyty@163.com>
# 2014-08-09
#
# ====================================================
#
# ZA-frequency RelaxationTime TA-frequency RelaxationTime LA-frequency RelaxationTime ...
#
# ====================================================

import os
import sys
import math

omega_file = 'BTE.omega_full'            # 频率
#omega_file = 'BTE.omega'            # 频率

w_file = 'BTE.w_final_full'              # 散射率
#w_file = 'BTE.w_final'              # 散射率

# ========
# 读入数据
# ========
omega = open(omega_file)
w = open(w_file)
omega_data = omega.read().split('\n')
w_data = w.read().split('\n')
omega.close()
w.close()

# ========
# 输出数据
# ========

for i in range(1, len(omega_data)-1):
    for j in range(0, len(omega_data[0].split())):
        print('%20.15f %20.15f' %(float(omega_data[i].split()[j]) / 2 / math.pi, 1 / float(w_data[i].split()[j]))),
        print
#    print
