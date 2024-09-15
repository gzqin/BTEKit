#!/bin/bash
# 完成对多个目录中第三阶力常数计算和ShengBTE（第一性原理材料热导计算）任务的准备和提交
# dir and files that should be prepared:
#   3nd-XXX/ 3nd/ shengbte/
#   BTE.bsub
#
# Written BY QIN, GuangZhao <qin.phys@gmail.com> 
# 2016-11-25
# 2020-03-30

NUMBER=10
SC="5 5 1"

THIRDORDER='thirdorder_vasp.py'
BTECOPY='BTE-copy3rd.sh'
JOBSUB='qsub /public/example/ShengBTE.pbs'  # path of ShengBTE qusb file

for i in $(seq 1 1 $NUMBER)
do
    [ -d 3nd-$i ] && continue
    rsync -av 3nd/ 3nd-$i
    cd 3nd-$i               # ----------------
    $THIRDORDER sow $SC -$i
    $BTECOPY ../3nd-$NUMBER
    find run-* -name vasprun.xml | $THIRDORDER reap $SC -$i
    cd ..                   # ----------------

    rsync -av shengbte/ shengbte-$i
    cd shengbte-$i          # ----------------
    rm FORCE_CONSTANTS_3RD
    ln -s ../3nd-$i/FORCE_CONSTANTS_3RD
    $JOBSUB
    cd ..                   # ----------------
done
