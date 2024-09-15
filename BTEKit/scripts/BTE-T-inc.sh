#!/bin/bash
#PBS -q core12
#PBS -N ShengBTE
#PBS -l nodes=1:ppn=12
#
# ====================================================
#
# Increase the temperature and do ShengBTE calculation
#
# OUTPUT: ThermalConductivity-T.txt
# 
# 温度 K(x) K(y) K(z) x-ZA x-TA x-LA ... y-ZA y-TA y-LA ... z-ZA z-TA z-LA ...
#
# ====================================================

# Temperature
TEMP_INC='50 25 800'

#export LD_LIBRARY_PATH=/share/apps/Intel.Fortran.Compiler.2013.1.117/mkl/lib/intel64/netcdf:/share/apps/Intel.Fortran.Compiler.2013.1.117/mkl/lib/intel64/:/share/apps/intel/ictce311/impi/3.1/lib64:/share/apps/intel/ictce311/impi/3.1/lib64:/share/apps/intel/ictce311/mkl/10.0.3.020/lib/em64t:/share/apps/intel/ictce311/itac/7.1/itac/slib_impi3:/share/apps/intel/ictce311//fce/10.1.015/lib:/share/apps/intel/ictce311//cce/10.1.015/lib:$LD_LIBRARY_PATH
#export PATH=~/bin/ScriptsForVASP:~/bin:/share/apps/Intel.Fortran.Compiler.2013.1.117/bin:/share/apps/intel/ictce311/impi/3.1/bin64:/usr/kerberos/bin:/usr/java/latest/bin:/share/apps/intel/ictce311/impi/3.1/bin64:/share/apps/intel/ictce311/itac/7.1/bin:/share/apps/intel/ictce311//fce/10.1.015/bin:/share/apps/intel/ictce311//cce/10.1.015/bin:/share/apps/intel/ictce311//idbe/10.1.015/bin:/usr/local/bin:/bin:/usr/bin:/opt/eclipse:/opt/ganglia/bin:/opt/ganglia/sbin:/opt/maui/bin:/opt/torque/bin:/opt/torque/sbin:/opt/pdsh/bin:/opt/rocks/bin:/opt/rocks/sbin:/sbin:/usr/sbin:$PATH

if [ -d "$PBS_O_WORKDIR" ];then
    cd "$PBS_O_WORKDIR"
fi

mkdir -p T-inc
cp CONTROL FORCE_CONSTANTS_2ND FORCE_CONSTANTS_3RD T-inc/
cd T-inc

NATOMS="$(cat CONTROL | grep 'natoms=')"
NATOMS="${NATOMS##*=}"

# 计算
for T in $(seq $TEMP_INC)
do
    [ -d T-$T ] && continue
    (
     mkdir T-$T
     cp CONTROL FORCE_CONSTANTS_2ND FORCE_CONSTANTS_3RD T-$T
     cd T-$T
     pwd
     sed -i -e "s/T=.*/T=$T/g" CONTROL
     mpirun -np 72 ShengBTE >|BTE.out 2>|BTE.err
    )
done

# 收集数据
for T in $(seq $TEMP_INC)
do
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
