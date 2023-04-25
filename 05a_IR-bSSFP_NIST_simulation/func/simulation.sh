#!/bin/bash

set -euo pipefail
set -x


# Check if BART is set up correctly

if [ ! -e $TOOLBOX_PATH/bart ] ;
then
	echo "\${TOOLBOX_PATH} is not set correctly!" >&2
	exit 1
fi

export PATH=${TOOLBOX_PATH}:${PATH}


# Estimate relative paths

FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})


# Load and Extract Reconstruction information

echo $OPTS

if [ -z ${OPTS+x} ];
then
        echo "${REL_PATH}/opts.sh is not actively set." >&2

	OPTS=${REL_PATH}/opts.sh
fi

source $OPTS

# Always most complex model for this simulation!

SLICE_PROFILE_SPINS_SIM=31
SS_GRAD_STRENGTH_SIM=0.012
SLICE_THICKNESS=0.02


# Create temporary folder

[ -d tmp ] && rm -rf tmp
mkdir tmp


# Load traj files

TRAJ=$1


# Simulated Signal

SAMPLES=$(bart show -d 1 ${TRAJ})
BR=$(($(bart show -d 1 ${TRAJ})/2))
SPOKES=$(bart show -d 2 ${TRAJ})
REP=$(bart show -d 5 ${TRAJ})

echo "SAMPLES: ${SAMPLES}"
echo "BR: ${BR}"
echo "SPOKES: ${SPOKES}"
echo "REP: ${REP}"

## Relaxation parameters for NIST phantom
## Estimated from single-echo spin-echo measurements
## Last value in T2 was measured wrong: 735 ms. Thus it is replace
## by the literature value of 6 ms
T1=(3 2.965 2.224 1.934 1.582 1.529 1.047 0.839 0.630 0.455 0.310 0.327 0.196 0.139 0.116)
T2=(1 1.450 0.388 0.271 0.183 0.175 0.098 0.071 0.049 0.033 0.023 0.018 0.018 0.026 0.006)

FILE=ref_nist.txt
[ -f $FILE ] && rm $FILE
touch $FILE

for i in `seq 0 $((${#T1[@]}-1))`;
do
        echo -e "Tube $i\t T1: ${T1[$i]} s,\tT2[$i]: ${T2[$i]} s"

        bart sim --ODE \
        --seq IR-BSSFP,TR=${TR},TE=${TE},FA=${FA},Nrep=$((REP*AV)),Trf=${RF_DUR},BWTP=${BWTP},ipl=${INV_LEN},ppl=${PREP_LEN},sl-grad=${SS_GRAD_STRENGTH_SIM},isp=${INV_SPOILER},slice-thickness=${SLICE_THICKNESS},Nspins=${SLICE_PROFILE_SPINS_SIM} \
         -1 ${T1[$i]}:${T1[$i]}:1 -2 ${T2[$i]}:${T2[$i]}:1 \
         tmp/simu$(printf "%02d" $i)

        echo -e "${T1[$i]}\t${T2[$i]}" >> $FILE
done

## Join all individually simulated signals
bart join 7 $(ls tmp/simu*.cfl | sed -e 's/\.cfl//') tmp/sim_c
rm tmp/simu*.{cfl,hdr}

## join them in a single dimension (6)
bart reshape $(bart bitmask 6 7) ${#T1[@]} 1 tmp/sim_c tmp/sim
rm tmp/sim_c.{cfl,hdr}


# Simulate spatial components of T2 sphere of NIST phantom

GEOM_COMP=${#T1[@]} # Should be 15 for NIST geoemtry!

## Create phantom based on trajectory
bart phantom --NIST -s${SIM_COILS} -b -k -t ${TRAJ} tmp/_geom

### Remove spoke averaging here
bart reshape $(bart bitmask 2 5) 1 $((REP*AV)) tmp/{_,}geom


# Combine simulated signal and spatial components

bart fmac -s $(bart bitmask 6) tmp/geom tmp/sim tmp/ksp


# Format ksp to fit moba required data format data
### Add spoke averaging again
bart reshape $(bart bitmask 2 5) ${AV} ${REP} tmp/ksp{,2}


# Add noise

bart noise -n 1 -s 42 tmp/ksp{2,3}


# Apply coil compression as for measured data

bart cc -p $AV_COILS -A  tmp/ksp3 ksp

[ -d tmp ] && rm -rf tmp

echo "Created simulated kspace file: ksp.{cfl,hdr}."