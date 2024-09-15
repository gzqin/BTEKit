#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# BTE.kappa_mode
# BTE.w_final_full
# BTE.v_full
#
# bte.*
#
# Written BY GuangZhao QIN <qin.phys@gmail.com>
# 2014-12-22
# 2016-03-05 各向异性的处理

# =================================================
# w = v/L * (1-p)/(1+p)
# -------------------------------------------------
# v 为输运方向的群速度
# -------------------------------------------------
# 边界散射中尺寸的大小 单位为 nm （w 单位为 ps-1）
L = 1
# -------------------------------------------------
# rough -> smooth
# 0     -> 1
p = 0
# =================================================

import os
import sys
import math

if len(sys.argv) == 2:
    L = float(sys.argv[1])
if len(sys.argv) == 3:
    L = float(sys.argv[1])
    p = float(sys.argv[2])

infile_kappa_mode = 'BTE.kappa_mode'            # 各个 mode 的热导率
infile_w_final = 'BTE.w_final_full'             # 散射率： 非简谐+同位素
infile_velocity = 'BTE.v_full'       # 散射率： 边界散射

outfile_w_total_x = 'BTE.w_total_x_full'            # 总散射率
outfile_w_total_y = 'BTE.w_total_y_full'            # 总散射率
outfile_w_total_z = 'BTE.w_total_z_full'            # 总散射率
outfile_kappa_mode = 'BTE.kappa_mode'           # 各个 mode 的热导率
outfile_kappa = 'BTE.kappa'                     # 各个 band 的热导率 tensor
outfile_kappa_tensor = 'BTE.kappa_tensor'       # 总的热导率 tensor

# ========
# 读入数据
# ========
print('Reading data ...')
kappa_mode = open(infile_kappa_mode)            # kappa_mode
data_kappa_mode = kappa_mode.read().split('\n')
kappa_mode.close()
w_final = open(infile_w_final)                  # w_final
data_w_final = w_final.read().split('\n')
w_final.close()
velocity = open(infile_velocity)            # velocity
data_velocity = velocity.read().split('\n')
velocity.close()

print('Initializing array ... ')
# 初始化二维数组 row x col: outdata_kappa_mode outdata_w_total
# 输出的每个 mode 的 rescaled 热导率和每个 band 的总散射率
num_kappa_mode_row = len(data_kappa_mode) - 1           # -1 是因为最后会有一个空元素
num_kappa_mode_col = len(data_kappa_mode[0].split())
outdata_kappa_mode = [[0 for col in range(num_kappa_mode_col)] for row in range(num_kappa_mode_row)]
num_w_row = len(data_w_final) - 1
num_w_col = len(data_w_final[0].split())
outdata_w_total_x = [[0 for col in range(num_w_col)] for row in range(num_w_row)]
outdata_w_total_y = [[0 for col in range(num_w_col)] for row in range(num_w_row)]
outdata_w_total_z = [[0 for col in range(num_w_col)] for row in range(num_w_row)]
# 初始化一维数组: outdata_kappa outdata_kappa_tensor
# 输出的每个 band 的热导率和最终的热导率 9x9 tensor
outdata_kappa = [0 for col in range(num_kappa_mode_col)]
outdata_kappa_tensor = [0 for col in range(num_kappa_mode_col//num_w_col)]

print('Calculating scattering rate ...')
print('  p=%f    L=%f nm' %(p, L))
# 总散射率 = “非简谐+同位素” + 边界散射
for i in range(1, num_w_row):
    for j in range(num_w_col):
        print(f"Row {i}, Velocity data: {len(data_velocity[i].split())}, num_w_col: {num_w_col}, j: {j}")
        # i=3204 data_velocity[i].split()=['-0.8713188838E+01', '0.4617880269E+00', '0.0000000000E+00']
        # num_w_col=6, j=3
        # if len(data_velocity[i].split()) < (j + 2 * num_w_col):
        #     print(f"Error: Row {i} has insufficient data.")
        #     continue  # 跳过该行，避免报错
        if data_w_final[i].split()[j] == 'NaN':     # discard the NaN
            outdata_w_total_x[i][j] = 0
            outdata_w_total_y[i][j] = 0
            outdata_w_total_z[i][j] = 0
        else:
            outdata_w_total_x[i][j] = float(data_w_final[i].split()[j]) + \
                                    abs(float(data_velocity[i].split()[int(j+0*num_w_col)])) / float(L) * (1-p)/(1+p)
            outdata_w_total_y[i][j] = float(data_w_final[i].split()[j]) + \
                                    abs(float(data_velocity[i].split()[int(j+1*num_w_col)])) / float(L) * (1-p)/(1+p)
            outdata_w_total_z[i][j] = float(data_w_final[i].split()[j]) + \
                                    abs(float(data_velocity[i].split()[j+2*num_w_col])) / float(L) * (1-p)/(1+p)
# 最终的每个 mode 的热导率 = mode 初始热导率 * w_final / w_total （每个小 tensor 一个散射率）
# data_kappa_mode 每一行的数据结构
# 1 2    3
#   编号 xx xy xz yx yy yz zx zy zz
#   其中 xx 等矩阵元有 3*atoms 个数值，分别对应 ZA, TA, LA ...
#   每个 ZA, TA, LA ... 对应一个散射率
print('Rescaling thermal conductivity of each mode ...')
for i in range(1, num_kappa_mode_row):
    for j in range(num_kappa_mode_col):
        if float(data_kappa_mode[i].split()[j]) <= 0:   # Only count the positive value
            outdata_kappa_mode[i][j] = 0
            continue

        k=j%num_w_col       # k 为j对应的band编号（num_w_col为总band个数）
        l=int(j/num_w_col)  # l 为j对应的方向编号（num_w_col为总band个数）
                        # 0:xx  1:xy    2:xz    3:yx    4:yy    5:yz    6:zx    7:zy    8:zz
        if l == 0:      # xx
            outdata_w_total=outdata_w_total_x[i][k]
        if l == 4:      # yy
            outdata_w_total=outdata_w_total_y[i][k]
        if l == 8:      # zz
            outdata_w_total=outdata_w_total_z[i][k]
        if l == 1 or l == 3:      # xy yx
            outdata_w_total=(outdata_w_total_x[i][k]+outdata_w_total_y[i][k])/2
        if l == 2 or l == 6:      # xz zx
            outdata_w_total=(outdata_w_total_x[i][k]+outdata_w_total_z[i][k])/2
        if l == 5 or l == 7:      # yz zy
            outdata_w_total=(outdata_w_total_y[i][k]+outdata_w_total_z[i][k])/2
        if outdata_w_total == 0:        # NaN
            outdata_kappa_mode[i][j] = 0
            continue

        outdata_kappa_mode[i][j] = float(data_kappa_mode[i].split()[j]) * \
                                   float(data_w_final[i].split()[k]) / outdata_w_total

# 将 outdata_kappa_mode 中的每一行累加 到 outdata_kappa
print('Getting thermal conductivity by summing up ...')
for i in range(1, num_kappa_mode_row):
    for j in range(num_kappa_mode_col):
        outdata_kappa[j] = outdata_kappa[j] + outdata_kappa_mode[i][j]
#        outdata_kappa[j] = float(outdata_kappa[j]) + data_kappa_mode[i][j]
# 将 outdata_kappa 中的每一行中的 band 合并变成 9x9 tensor
for k in range(num_kappa_mode_col):
    outdata_kappa_tensor[k // num_w_col] = outdata_kappa_tensor[k // num_w_col] + outdata_kappa[k]

# ========
# 输出数据
# ========
print('Outputing ...')

w_total = open(outfile_w_total_x, 'w')            # 总散射率 x
for i in range(num_w_row):
    for j in range(num_w_col):
        print >>w_total, "%20.15f" %(outdata_w_total_x[i][j]),
    print >>w_total
w_total.close()
w_total = open(outfile_w_total_y, 'w')            # 总散射率 y
for i in range(num_w_row):
    for j in range(num_w_col):
        print >>w_total, "%20.15f" %(outdata_w_total_y[i][j]),
    print >>w_total
w_total.close()
w_total = open(outfile_w_total_z, 'w')            # 总散射率 z
for i in range(num_w_row):
    for j in range(num_w_col):
        print >>w_total, "%20.15f" %(outdata_w_total_z[i][j]),
    print >>w_total
w_total.close()

kappa_mode = open(outfile_kappa_mode, 'w')      # 各个 mode 的热导率
for i in range(num_kappa_mode_row):
    for j in range(num_kappa_mode_col):
        print >>kappa_mode, "%20.15f" %(outdata_kappa_mode[i][j]),
    print >>kappa_mode
kappa_mode.close()

kappa = open(outfile_kappa, 'w')                # 各个 band 的热导率 tensor
print >>kappa, ' 0',
for j in range(num_kappa_mode_col):
    print >>kappa, "%20.15f" %(outdata_kappa[j]),
print >>kappa
kappa.close()

kappa_tensor = open(outfile_kappa_tensor, 'w')  # 总的热导率 tensor
print >>kappa_tensor, ' 0',
for j in range(num_kappa_mode_col//num_w_col):
    print >>kappa_tensor, "%20.15f" %(outdata_kappa_tensor[j]),
print >>kappa_tensor
kappa_tensor.close()
print('  %s\n  %s\n  %s\n  %s\n  %s\n  %s' %(outfile_w_total_x, outfile_w_total_y, outfile_w_total_z, outfile_kappa_mode, outfile_kappa, outfile_kappa_tensor))
