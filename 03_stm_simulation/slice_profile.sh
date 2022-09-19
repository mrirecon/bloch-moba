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

FA=180
RF_DUR=0.001
TR=$RF_DUR
TE=$RF_DUR
DINV=0
DPREP=0
BWTP=1

ODE_TOL=1E-6

#WM
T1=0.832
T2=0.08
M0=1

# Create file for storing results of simulation

FILE=${REL_PATH}/slice.txt
[ -f $FILE ] && rm $FILE
touch $FILE

# Loop over Slice Profile Spins

G_SS=0.012              # [T/m]
DISTANCE=0.010          # [m]

SPIN=0
NSPIN=100

for SPIN in $(seq 0 1 $NSPIN)
do
        Z=$(echo $DISTANCE $SPIN $NSPIN | awk '{printf "%f\n",$1/$3*($2-$3/2)}')

        echo $SPIN  $Z

        bart sim --STM --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/modev
        echo "0" $Z $(component_analysis $((REP-1)) tmp/modev) >> $FILE

        bart sim --ODE --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/odev
        echo "1" $Z $(component_analysis $((REP-1)) tmp/odev) >> $FILE

        bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim --other sampling-rate=10E4 -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/oder
        echo "2" $Z $(component_analysis $((REP-1)) tmp/oder) >> $FILE

        bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim --other sampling-rate=10E5 -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/oder2
        echo "3" $Z $(component_analysis $((REP-1)) tmp/oder2) >> $FILE

        bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim --other sampling-rate=10E6 -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/oder3
        echo "4" $Z $(component_analysis $((REP-1)) tmp/oder3) >> $FILE

        bart join 6 tmp/modev tmp/odev tmp/oder tmp/oder2 tmp/oder3 tmp/join_$(printf ${SPIN})
done

bart join 7 $(ls tmp/join_*.cfl | sed -e 's/\.cfl//') joined_results

sed -i 's/i/j/g' $FILE

[ -d tmp ] && rm -r tmp
