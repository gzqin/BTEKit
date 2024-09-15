#!/bin/bash
#
# Get the data of IFC-distance
#
# Written BY QIN, GuangZhao <qin.phys@gmail.com>
# 2016-11-25
# updated on 2022-01-25 for new format of SPOSCAR and FORCE_CONSTANTS

CENTER_NU=7
TOTAL_ATOMS=144


LATTICE_X=$(cat SPOSCAR | head -3 | tail -1)
LATTICE_X1=$(echo $LATTICE_X | cut -d ' ' -f 1)
LATTICE_X2=$(echo $LATTICE_X | cut -d ' ' -f 2)
LATTICE_X3=$(echo $LATTICE_X | cut -d ' ' -f 3)
LATTICE_Y=$(cat SPOSCAR | head -4 | tail -1)
LATTICE_Y1=$(echo $LATTICE_Y | cut -d ' ' -f 1)
LATTICE_Y2=$(echo $LATTICE_Y | cut -d ' ' -f 2)
LATTICE_Y3=$(echo $LATTICE_Y | cut -d ' ' -f 3)
LATTICE_Z=$(cat SPOSCAR | head -5 | tail -1)
LATTICE_Z1=$(echo $LATTICE_Z | cut -d ' ' -f 1)
LATTICE_Z2=$(echo $LATTICE_Z | cut -d ' ' -f 2)
LATTICE_Z3=$(echo $LATTICE_Z | cut -d ' ' -f 3)

_distance()
{
    XYZ1="${1# }"
    XYZ2="${2# }"
    XYZ1=${XYZ1% }
    XYZ2=${XYZ2% }

    XYZ1_x=${XYZ1% *}
    XYZ1_y=${XYZ1_x#* }
    XYZ1_x=${XYZ1_x% *}
    XYZ1_z=${XYZ1##* }

    XYZ2_x=${XYZ2% *}
    XYZ2_y=${XYZ2_x#* }
    XYZ2_x=${XYZ2_x% *}
    XYZ2_z=${XYZ2##* }

    DIS_X=$(echo "$XYZ2_x - $XYZ1_x" | bc -l)
    DIS_Y=$(echo "$XYZ2_y - $XYZ1_y" | bc -l)
    DIS_Z=$(echo "$XYZ2_z - $XYZ1_z" | bc -l)

#   X
    DIFF=$(echo "$DIS_X - 0.5" | bc -l)
    if [ x"${DIFF:0:1}" == x"0" ];then
        DIS_X=$(echo "$DIS_X - 1" | bc -l)
    fi
    DIFF=$(echo "$DIS_X + 0.5" | bc -l)
    if [ x"${DIFF:0:1}" == x"-" ];then
        DIS_X=$(echo "$DIS_X + 1" | bc -l)
    fi
#   Y
    DIFF=$(echo "$DIS_Y - 0.5" | bc -l)
    if [ x"${DIFF:0:1}" == x"0" ];then
        DIS_Y=$(echo "$DIS_Y - 1" | bc -l)
    fi
    DIFF=$(echo "$DIS_Y + 0.5" | bc -l)
    if [ x"${DIFF:0:1}" == x"-" ];then
        DIS_Y=$(echo "$DIS_Y + 1" | bc -l)
    fi
#   Z
    DIFF=$(echo "$DIS_Z - 0.5" | bc -l)
    if [ x"${DIFF:0:1}" == x"0" ];then
        DIS_Z=$(echo "$DIS_Z - 1" | bc -l)
    fi
    DIFF=$(echo "$DIS_Z + 0.5" | bc -l)
    if [ x"${DIFF:0:1}" == x"-" ];then
        DIS_Z=$(echo "$DIS_Z + 1" | bc -l)
    fi

    D_DIS_X=$(echo "$LATTICE_X1*$DIS_X + $LATTICE_Y1*$DIS_Y + $LATTICE_Z1*$DIS_Z" | bc -l)
    D_DIS_Y=$(echo "$LATTICE_X2*$DIS_X + $LATTICE_Y2*$DIS_Y + $LATTICE_Z2*$DIS_Z" | bc -l)
    D_DIS_Z=$(echo "$LATTICE_X3*$DIS_X + $LATTICE_Y3*$DIS_Y + $LATTICE_Z3*$DIS_Z" | bc -l)
    
    echo "sqrt(($D_DIS_X)^2 + ($D_DIS_Y)^2 + ($D_DIS_Z)^2)" | bc -l
}

for CENTER_NU in $(seq 1 1 $TOTAL_ATOMS)
do
    XYZ_center=$(tail -n +9 SPOSCAR | head -n $CENTER_NU | tail -n 1 | tr -s ' ')

    for NU in $(seq 1 1 $TOTAL_ATOMS)
    do
        XYZ=$(tail -n +9 SPOSCAR | head -n $NU | tail -n 1 | tr -s ' ')
        DISTANCE=$(_distance "$XYZ_center" "$XYZ")

#        if [ $NU -lt 10 ];then
#            NU="  $NU"
#        elif [ $NU -lt 100 ];then
#            NU=" $NU"
#        fi

#        IFC=$(cat FORCE_CONSTANTS | grep -A 3 " $CENTER_NU $NU" | tail -3)
        IFC=$(cat FORCE_CONSTANTS | grep -A 3 -E "^$CENTER_NU $NU$" | tail -3)
#        traceIFC=$(echo $IFC | cut -d ' ' -f 1,5,9 | tr " " "+")
        traceIFC=$(echo $IFC | tr -d '-' | sed -e 's/ /^2+/g')
#        traceIFC=$(echo "sqrt((${traceIFC})^2)" | bc -l)
        traceIFC=$(echo "sqrt(${traceIFC})" | bc -l)

        echo $DISTANCE $traceIFC
    done
done
