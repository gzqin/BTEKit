#!/bin/bash
#
# Construct the 3rd files based on the finished calculations
#
# Written BY QIN, GuangZhao <qin.phys@gmail.com>
# 2016-11-22

DIR="../3rd"  # original dir 

if [ ! -d "$DIR" ];then
    echo Please specify the source directory.
    exit
fi

for NAME in 3RD.POSCAR.*
do
    NUM="${NAME#3RD.POSCAR.}"   # the number of the 3nd POSCAR file
    CODE=$(head -1 $NAME)       # the code of the POSCAR file
# find the source POSCAR file in the source directory
    INFO=$(grep $CODE $DIR/3RD.POSCAR.* | head -1)
    [ x"$INFO" == x ] && echo "NOT FOUND for run-$NUM" && continue
    SOURCE_NUM="${INFO%:*}"     # the number of the source POSCAR file
    SOURCE_NUM="${SOURCE_NUM##*.}"

    echo "$DIR/run-$SOURCE_NUM/ --> run-$NUM/"
#    diff 3RD.POSCAR.$NUM $DIR/3RD.POSCAR.$SOURCE_NUM
    rsync -a $DIR/run-$SOURCE_NUM/vasprun.xml ./run-$NUM/
done
