#!/usr/bin/bash
#
# use the BTE.boundaryRescale.py to get the kappa-size curve.
#
# Written BY QIN, GuangZhao <qin.phys@gmail.com>
# 2015-11-12

p=0

_log_inc_num()
{
#    for i in {-1..4}
#    for i in {-3..7}
    for i in {-1..6}
    do
#        for j in {1..1}
        for j in {1..9}
        do
            echo "$j*10^$i" | bc -l
        done
    done
}

#_log_inc_num
#exit

DIR="p-$p-$(date +%s)"
mkdir $DIR
#cp BTE.kappa_mode BTE.w_final_full BTE.w_boundary_full $DIR
if [ -s BTE.kappa_mode_new ];then
    cp BTE.kappa_mode_new $DIR/BTE.kappa_mode
else
    cp BTE.kappa_mode $DIR/BTE.kappa_mode
fi
cp BTE.w_final_full BTE.v_full $DIR
cp BTE-boundaryRescale2.py $DIR

cd $DIR
#for i in 0.1 1 10 100 1000 10000
for i in $(_log_inc_num)
do
#    BTE-boundaryRescale.py $i $p >&2
    python BTE-boundaryRescale2.py $i $p >&2
    echo -n "== $i "
    tail bte.kappa_tensor | tr -s " " | cut -d " " -f 3,7,11
done
