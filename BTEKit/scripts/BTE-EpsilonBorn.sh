#!/bin/bash
#
# 获取介电常数以及玻恩有效电荷
#
# Written BY QIN, GuangZhao <qin.phys@gmail.com>
# 2014-04-13

# 数据从 OUTCAR 中读取
DATAFILE=OUTCAR
[ x"$1" != x ] && DATAFILE="$1"
if [ ! -s "$DATAFILE" ];then
    echo "File NOT exists: $DATAFILE"
    exit
fi

# 介电常数
DIELECTRIC="$(cat "$DATAFILE" | grep -A 4 'MACROSCOPIC STATIC DIELECTRIC TENSOR (including local field effects in DFT)' | tail -n +3 | head -3 | tr -s "\t" " " | sed -e 's/^ //g')"

# 输出介电常数
for i in 1 2 3
do
    echo "epsilon(:,$i)=$(echo "$DIELECTRIC" | tail -n +$i | head -1)"
done

# 玻恩有效电荷
COUNT=0
cat "$DATAFILE" | grep -A 999999 'BORN EFFECTIVE CHARGES (in e, cummulative output)' |
tail -n +3 | tr -s "\t" " " | sed -e 's/^ //g' |
while read LINE
do
    if [ x"$LINE" = x ];then
        break
    fi
    if [ x"${LINE% *}" = xion ];then
        ION="${LINE#ion }"
        for i in 1 2 3
        do
            read LINE
            echo "born(:,${i},$ION)=${LINE#* }"
        done
    fi
done
