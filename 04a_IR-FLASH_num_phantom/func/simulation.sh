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

SLICE_PROFILE_SPINS_SIM=41
SS_GRAD_STRENGTH_SIM=0.012 # Set to 0 for Fourier Approximation
SLICE_THICKNESS=0.03

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

## Relaxation parameters for Diagnostic Sonar phantom
## Eurospin II, gel nos 3, 4, 7, 10, 14, and 16)
## T1 from reference measurements in
##      Wang, X., Roeloffs, V., Klosowski, J., Tan, Z., Voit, D., Uecker, M. and Frahm, J. (2018),
##      Model-based T1 mapping with sparsity constraints using single-shot inversion-recovery radial FLASH.
##      Magn. Reson. Med, 79: 730-740. https://doi.org/10.1002/mrm.26726
## T2 from
##      T. J. Sumpf, A. Petrovic, M. Uecker, F. Knoll and J. Frahm,
##      Fast T2 Mapping With Improved Accuracy Using Undersampled Spin-Echo MRI and Model-Based Reconstructions With a Generating Function
##      IEEE Transactions on Medical Imaging, vol. 33, no. 12, pp. 2213-2222, Dec. 2014, doi: 10.1109/TMI.2014.2333370.

T1=(3 0.311 0.458 0.633 0.805 1.1158 1.441 3)
T2=(1 0.046 0.081 0.101 0.132 0.138 0.166 1)

FILE=ref_sonar.txt
[ -f $FILE ] && rm $FILE
touch $FILE

for i in `seq 0 $((${#T1[@]}-1))`;
do
        echo -e "Tube $i\t T1: ${T1[$i]} s,\tT2[$i]: ${T2[$i]} s"

        bart sim --ODE \
        --seq IR-FLASH,TR=${TR},TE=${TE},FA=${FA},Nrep=$((REP*AV)),Trf=${RF_DUR},BWTP=${BWTP},ipl=${INV_LEN},ppl=${PREP_LEN},sl-grad=${SS_GRAD_STRENGTH_SIM},isp=${INV_SPOILER},slice-thickness=${SLICE_THICKNESS},Nspins=${SLICE_PROFILE_SPINS_SIM} \
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

## Create phantom based on trajectory
bart phantom --SONAR -s${SIM_COILS} -b -k -t ${TRAJ} tmp/_geom

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