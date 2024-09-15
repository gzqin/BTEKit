#!/bin/bash
#
# 2nd force calculations
#
# Written BY QIN, Guangzhao <qin.phys@gmail.com>
# 2019-12-01

JOBSUB='qsub /public/example/vasp.pbs'
[ x"$1" != x ] && JOBSUB="qsub $1"

touch WAVECAR CHGCAR

for POSCAR in POSCAR-*
do
    NUM=${POSCAR#POSCAR-}
    DIR="run-$NUM"
    [ -d "$DIR" ] && continue

    mkdir "$DIR"
    cp $POSCAR "$DIR/POSCAR"

    (
     cd "$DIR"
     pwd
     ln -s ../WAVECAR WAVECAR
     ln -s ../CHGCAR CHGCAR
     if [ "$DIR" == run-001 ];then
         # write the CHGCAR for accelerating other calculations
         cp ../INCAR ./
         sed -i -e 's/^LWAVE=.*/LWAVE=.FALSE./g' INCAR
         sed -i -e 's/^LCHARG=.*/LCHARG=.TRUE./g' INCAR
     else
         ln -s ../INCAR INCAR
     fi
     ln -s ../KPOINTS KPOINTS
     ln -s ../POTCAR POTCAR
     ln -s ../vdw_kernel.bindat vdw_kernel.bindat
     eval $JOBSUB
    )
done
