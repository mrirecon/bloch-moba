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

# Load ksp files
KSP=$1
TRAJ=$2


# Load and Extract Reconstruction information

if [ ! -f ${REL_PATH}/opts.sh ];
then
	echo "${REL_PATH}/opts.sh does not exist." >&2
	exit 1
fi

source ${REL_PATH}/opts.sh


SPOKES=$(bart show -d 2 ${KSP})
FRAMES=$(bart show -d 5 ${KSP})


# Take last $COMBINED_SPOKES spokes close to steady-state and join all

COMBINED_SPOKES=$FRAMES

bart extract 5 $((FRAMES-COMBINED_SPOKES)) $FRAMES $KSP dtmp
bart reshape $(bart bitmask 2 5) $((COMBINED_SPOKES*SPOKES)) 1 dtmp{,2}

bart extract 5 $((FRAMES-COMBINED_SPOKES)) $FRAMES $TRAJ ttmp
bart reshape $(bart bitmask 2 5) $((COMBINED_SPOKES*SPOKES)) 1 ttmp{,2}


# Grid k-space

## NuFFT to image space
bart nufft -i ttmp2 dtmp2 tmp

## Project back to k-space
bart fft -u $(bart bitmask 0 1) tmp{,2}

# Calculate sensitivity maps, just 1 (-m) map!
bart ecalib -c 0 -m 1 tmp2 sens_ref


rm {,t,d}tmp{,2}.{cfl,hdr}

echo "Estimated reference coil-profiles sens_ref.{cfl,hdr}." >&2
