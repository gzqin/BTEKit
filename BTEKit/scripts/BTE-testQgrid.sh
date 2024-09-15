#!/bin/bash
#
# 测试 Q 空间格子取点收敛
#
# 2014-09-12

# 命令行附带任何参数则不计算，仅收集结果
[ x"$@" != x ] && FLAG=1

#GRID='1 1 20'      # seq
GRID='1 1 20'      # seq
#GRID='51 50 201'      # seq
DATAFILE=Qgrids.dat # 收集的数据文件
rm -f $DATAFILE

_testQgrid()
{
# 取不同格子进行收敛性测试
for grid in $(seq $GRID)
do
    DIR=grid-$grid
    [ -d $DIR ] && continue

    (
     mkdir $DIR
     cp CONTROL $DIR
     ln -s ../FORCE_CONSTANTS_2ND $DIR/FORCE_CONSTANTS_2ND
     ln -s ../FORCE_CONSTANTS_3RD $DIR/FORCE_CONSTANTS_3RD
     cd $DIR
#     sed -i -e "s/ngrid(:)=.*/ngrid(:)=1 1 $grid/g" CONTROL     # 1D
     sed -i -e "s/ngrid(:)=.*/ngrid(:)=$grid $grid 1/g" CONTROL     # 2D
#     sed -i -e "s/ngrid(:)=.*/ngrid(:)=$grid $grid $grid/g" CONTROL     # 3D
     pwd
#     mpirun -npernode 12 ShengBTE 2>|BTE.err | tee BTE.out 
#     mpirun -np 72 ShengBTE 2>|BTE.err | tee BTE.out 
     qsub $(pwd)/../shengbte.pbs
    )
done
}

[ x"$FLAG" != x1 ] && _testQgrid

# 收集数据
#for grid in $(seq $GRID)
#do
#    echo -n "$grid " >>$DATAFILE
#    cat grid-$grid/BTE.kappa_tensor | tail -1 | tr -s " " | cut -d " " -f 3,7 >>$DATAFILE
#done

rm -f $DATAFILE
for grid in $(seq 1 1 1000)
do
    dir=grid-$grid
    [ ! -s $dir/BTE.kappa_tensor ] && continue
    echo -n "${grid} " >>$DATAFILE
    cat $dir/BTE.kappa_tensor | tail -1 | tr -s " " | cut -d " " -f 3,7,11 >>$DATAFILE
done
