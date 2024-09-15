#!/bin/bash
#
# 3nd force calculations
#
# Written BY QIN, Guangzhao <qin.phys@gmail.com>
# 2015-09-17 

JOBSUB='qsub /public/example/vasp.pbs'
[ x"$1" != x ] && JOBSUB="qsub $1"

touch WAVECAR CHGCAR

# SCF -> FORCE_CONSTANTS_3D
for POSCAR in 3RD.POSCAR.*
do
    NUM=${POSCAR##*.}
    DIR=run-$NUM
    [ -d "$DIR" ] && continue

    /public/bin/checkpend.sh
#    ~/bin/checkpend.sh 'jara|low' 200
#    ~/bin/checktotalpend.sh

    echo; echo -n '== '; date
    mkdir $DIR
    cp $POSCAR $DIR/POSCAR

    (
     cd $DIR
     pwd
     ln -s ../WAVECAR WAVECAR
     ln -s ../CHGCAR CHGCAR
     ln -s ../INCAR INCAR
     ln -s ../KPOINTS KPOINTS
     ln -s ../POTCAR POTCAR
     ln -s ../vdw_kernel.bindat vdw_kernel.bindat
     eval $JOBSUB
    )
done
