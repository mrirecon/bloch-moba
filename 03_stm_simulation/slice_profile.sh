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

	# ODE

	ODE_TOL=1E-6
        bart sim --ODE --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/ode
        echo "0" $Z $(component_analysis $((REP-1)) tmp/ode) >> $FILE

	# ODE_TOL=1E-5
	# bart sim --ODE --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/ode1
        # echo "1" $Z $(component_analysis $((REP-1)) tmp/ode1) >> $FILE

	ODE_TOL=1E-4
	bart sim --ODE --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/ode2
        echo "2" $Z $(component_analysis $((REP-1)) tmp/ode2) >> $FILE

	ODE_TOL=1E-3
	bart sim --ODE --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/ode3
        echo "3" $Z $(component_analysis $((REP-1)) tmp/ode3) >> $FILE

	ODE_TOL=1E-2
	bart sim --ODE --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/ode4
        echo "4" $Z $(component_analysis $((REP-1)) tmp/ode4) >> $FILE

	# STM

	STM_TOL=1E-6
        bart sim --STM --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other stm-tol=${STM_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/stm
        echo "5" $Z $(component_analysis $((REP-1)) tmp/stm) >> $FILE

	# STM_TOL=1E-5
        # bart sim --STM --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other stm-tol=${STM_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/stm1
        # echo "6" $Z $(component_analysis $((REP-1)) tmp/stm1) >> $FILE

	STM_TOL=1E-4
        bart sim --STM --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other stm-tol=${STM_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/stm2
        echo "7" $Z $(component_analysis $((REP-1)) tmp/stm2) >> $FILE

	STM_TOL=1E-3
        bart sim --STM --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other stm-tol=${STM_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/stm3
        echo "8" $Z $(component_analysis $((REP-1)) tmp/stm3) >> $FILE

	STM_TOL=1E-2
        bart sim --STM --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other stm-tol=${STM_TOL} --split-dim -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/stm4
        echo "9" $Z $(component_analysis $((REP-1)) tmp/stm4) >> $FILE

	# ROT

	SR=1E8
        bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim --other sampling-rate=${SR} -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/rot
        echo "10" $Z $(component_analysis $((REP-1)) tmp/rot) >> $FILE

	SR=1E7
        bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim --other sampling-rate=${SR} -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/rot1
        echo "11" $Z $(component_analysis $((REP-1)) tmp/rot1) >> $FILE

	SR=1E6
        bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim --other sampling-rate=${SR} -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/rot2
        echo "12" $Z $(component_analysis $((REP-1)) tmp/rot2) >> $FILE

	SR=1E5
        bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim --other sampling-rate=${SR} -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/rot3
        echo "13" $Z $(component_analysis $((REP-1)) tmp/rot3) >> $FILE

	# SR=1E4
        # bart sim --ROT --seq FLASH,TR=${TR},TE=${TE},Nrep=${REP},pinv,ipl=${DINV},ppl=${DPREP},Trf=${RF_DUR},FA=${FA},BWTP=${BWTP},isp=${DINV},slice-thickness=${Z},sl-grad=${G_SS},Nspins=1 --other ode-tol=${ODE_TOL} --split-dim --other sampling-rate=${SR} -1 ${T1}:${T1}:1 -2 ${T2}:${T2}:1 tmp/rot4
        # echo "14" $Z $(component_analysis $((REP-1)) tmp/rot4) >> $FILE
done

sed -i 's/i/j/g' $FILE

[ -d tmp ] && rm -r tmp
