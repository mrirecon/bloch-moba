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
SLICE_THICKNESS=0.01
G_SS=0.012

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

	# ODE

	ODE_TOL=1E-6
        t=$(nice -n 5 bart sim --ODE --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${SLICE_THICKNESS},sl-grad=${G_SS},Nspins=${NSPINS} --other ode-tol=${ODE_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/ode)
        echo "0" $i $t $(component_analysis $((i-1)) tmp/ode) >> $FILE

	ODE_TOL=1E-5
        t=$(nice -n 5 bart sim --ODE --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${SLICE_THICKNESS},sl-grad=${G_SS},Nspins=${NSPINS} --other ode-tol=${ODE_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/ode1)
        echo "1" $i $t $(component_analysis $((i-1)) tmp/ode1) >> $FILE

	ODE_TOL=1E-4
        t=$(nice -n 5 bart sim --ODE --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${SLICE_THICKNESS},sl-grad=${G_SS},Nspins=${NSPINS} --other ode-tol=${ODE_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/ode2)
        echo "2" $i $t $(component_analysis $((i-1)) tmp/ode2) >> $FILE


        # STM

	STM_TOL=1E-6
        t=$(nice -n 5 bart sim --STM --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${SLICE_THICKNESS},sl-grad=${G_SS},Nspins=${NSPINS} --other stm-tol=${STM_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/stm)
        echo "3" $i $t $(component_analysis $((i-1)) tmp/stm) >> $FILE

	STM_TOL=1E-5
        t=$(nice -n 5 bart sim --STM --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${SLICE_THICKNESS},sl-grad=${G_SS},Nspins=${NSPINS} --other stm-tol=${STM_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/stm1)
        echo "4" $i $t $(component_analysis $((i-1)) tmp/stm1) >> $FILE

	STM_TOL=1E-4
        t=$(nice -n 5 bart sim --STM --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${SLICE_THICKNESS},sl-grad=${G_SS},Nspins=${NSPINS} --other stm-tol=${STM_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/stm2)
        echo "5" $i $t $(component_analysis $((i-1)) tmp/stm2) >> $FILE


        # ROT

	SR=1E7
        t=$(nice -n 5 bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${SLICE_THICKNESS},sl-grad=${G_SS},Nspins=${NSPINS} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 --other sampling-rate=${SR} tmp/rot)
        echo "6" $i $t $(component_analysis $((i-1)) tmp/rot) >> $FILE

        SR=1E6
        t=$(nice -n 5 bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${SLICE_THICKNESS},sl-grad=${G_SS},Nspins=${NSPINS} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 --other sampling-rate=${SR} tmp/rot1)
        echo "7" $i $t $(component_analysis $((i-1)) tmp/rot1) >> $FILE

        SR=1E5
        t=$(nice -n 5 bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${i},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${SLICE_THICKNESS},sl-grad=${G_SS},Nspins=${NSPINS} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 --other sampling-rate=${SR} tmp/rot2)
        echo "8" $i $t $(component_analysis $((i-1)) tmp/rot2) >> $FILE        
done

sed -i 's/i/j/g' $FILE #required for input to python script

[ -d tmp ] && rm -r tmp
