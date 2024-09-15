#!/bin/bash
#
# similar bandplot, for gruneisen
#
# Written BY QIN, GuangZhao <qin.phys@gmail.com>
# 2016-06-10

FILE=gruneisen.yaml
DAT=gruneisen.dat               # band seperated

pwd
echo "  $FILE --> $DAT"

NQPOINT=$(cat $FILE | grep nqpoint | cut -d : -f 2 | head -1)

# Accumulating distance
PLUS1=$(cat $FILE | grep distance | head -n ${NQPOINT} | tail -n 1 | cut -d : -f 2)
PLUS2=$(cat $FILE | grep distance | head -n $(($NQPOINT*2)) | tail -n 1 | cut -d : -f 2)

COUNT=0
#cat $FILE | grep -E 'distance|frequency' | cut -d : -f 2 |\
cat $FILE | grep -E 'distance|gruneisen' | cut -d : -f 2 |\
while read LINE
do
    COUNT=$(($COUNT + 1))

    if [ $(($COUNT / 7)) -ge $(($NQPOINT*2)) ]\
            && [ $(($COUNT % 7)) == 1 ];then
        echo "$LINE + $PLUS1 + $PLUS2" | bc -l | tr '\n' ' '            # 3
    elif [ $(($COUNT / 7)) -ge $NQPOINT ]\
            && [ $(($COUNT % 7)) == 1 ];then
        echo "$LINE + $PLUS1" | bc -l | tr '\n' ' '                     # 2
    else
        echo -n "$LINE "                                                # 1
    fi

    [ $(($COUNT % 7)) == 0 ] && echo
done >|$DAT


# merge band into one column
echo "  $DAT --> ${DAT}2"

TMP_DIR=tmp.$(date +%s)
mkdir $TMP_DIR
cd $TMP_DIR
for i in $(seq 1 1 7)
do
    cat ../$DAT | tail -n +2 | \
        tac | tail -n +2 | tac | \
        cut -d ' ' -f $i >$i
done

rm -f ../${DAT}2

for i in $(seq 2 1 7)
do
    paste -d ' ' 1 $i >>../${DAT}2
    echo >>../${DAT}2
done

cd ..
rm -r $TMP_DIR
