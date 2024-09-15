#!/bin/bash
#
# ====================================================
#
# Increase the temperature and do ShengBTE calculation
#
# OUTPUT: ThermalConductivity-T.txt
# 
# 温度 K(x) K(y) K(z) RTAx RTAy RTAz x-ZA x-TA x-LA ... y-ZA y-TA y-LA ... z-ZA z-TA z-LA ...
#
# ====================================================

# Temperature
#TEMP_INC='1 1 1000'
TEMP_INC='50 25 1000'

mkdir -p T-inc
cp CONTROL FORCE_CONSTANTS_2ND FORCE_CONSTANTS_3RD T-inc/
cd T-inc

NATOMS="$(cat CONTROL | grep 'natoms=')"
NATOMS="${NATOMS##*=}"

# 收集数据
for T in $(seq $TEMP_INC)
do
    [ ! -d T-$T ] && continue
    echo -n "$T "
#   x y z
#   BTE.kappa_tensor 数据结构：
# 1 2    3  4  5  6  7  8  9  10 11
#   编号 xx xy xz yx yy yz zx zy zz
    cat T-$T/BTE.kappa_tensor | tail -1 | tr -s " " | cut -d " " -f 3,7,11 | tr "\n" " "    # Iterative
    cat T-$T/BTE.kappa_tensor | head -1 | tr -s " " | cut -d " " -f 3,7,11 | tr "\n" " "    # RTA

#   Contribution from each branch
# BTE.kappa 数据结构
# 1 2    3
#   编号 xx xy xz yx yy yz zx zy zz
#   其中 xx 等矩阵元有 3*atoms 个数值，分别对应 ZA, TA, LA ...
    Nbands=$(($NATOMS * 3))
    cat T-$T/BTE.kappa | tail -1 | tr -s " " | cut -d ' ' -f 3- | \
        cut -d ' ' -f 1-${Nbands},$(($Nbands * 4 + 1))-$(($Nbands * 5)),$(($Nbands * 8 + 1))-$(($Nbands * 9))
done >|ThermalConductivity-T.txt
