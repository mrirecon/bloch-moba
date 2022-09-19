#!/bin/bash

set -euo pipefail
set -b
# set -x

function component_analysis()
{
        POS=$1
        M=$2

        bart slice 5 ${POS} ${M} tmp
        bart slice 0 0 tmp x
        bart slice 0 1 tmp y
        bart slice 0 2 tmp z

        rm tmp.{cfl,hdr}

        echo $(bart show x) $(bart show y) $(bart show z)
}

FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})

[ -d tmp ] && rm -r tmp
mkdir tmp

# Simulation
DIM=1
SPOKES=1
REP=1

FA=8
RF_DUR=0.001
TR=0.0031
TE=0.0017
DINV=0
DPREP=0
BWTP=1

#WM
T1=0.832
T2=0.08
M0=1
NSPINS=101

# Create file for storing results of simulation

FILE=${REL_PATH}/trtime.txt
[ -f $FILE ] && rm $FILE
touch $FILE

# Loop over repetition numbers

REPMAX=1000
STEP=50


for i in $(seq 1 $STEP $((REPMAX+1)))
do
        echo $i

        # STM
        t=$(nice -n 5 bart sim --STM --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=0.001,Nspins=${NSPINS} --other ode-tol=10E-7 --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/modev)
        echo "0" $i $t $(component_analysis $((i-1)) tmp/modev) >> $FILE

        # ODE
        t=$(nice -n 5 bart sim --ODE --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=0.001,Nspins=${NSPINS} --other ode-tol=10E-7 --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/odev)
        echo "1" $i $t $(component_analysis $((i-1)) tmp/odev) >> $FILE

        # ROT rate 10^4
        t=$(nice -n 5 bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=0.001,Nspins=${NSPINS} --other ode-tol=10E-7 --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 --other sampling-rate=10E4 tmp/oder)
        echo "2" $i $t $(component_analysis $((i-1)) tmp/oder) >> $FILE

        # ROT rate 10^5
        t=$(nice -n 5 bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=0.001,Nspins=${NSPINS} --other ode-tol=10E-7 --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 --other sampling-rate=10E5 tmp/oder2)
        echo "3" $i $t $(component_analysis $((i-1)) tmp/oder2) >> $FILE

        # ROT rate 10^6
        t=$(nice -n 5 bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=0.001,Nspins=${NSPINS} --other ode-tol=10E-7 --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 --other sampling-rate=10E6 tmp/oder3)
        echo "4" $i $t $(component_analysis $((i-1)) tmp/oder3) >> $FILE        
done

sed -i 's/i/j/g' $FILE #required for input to python script

[ -d tmp ] && rm -r tmp
