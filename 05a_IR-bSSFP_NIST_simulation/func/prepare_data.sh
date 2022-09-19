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

SAMPLES=$(echo $BR 2 | awk '{printf "%3.0f\n",$1*$2}')
TIME_STEPS=$((REP/AV))   # Integer division!

#-----------------------------------------------
#------------------ Trajectory -----------------
#----------------------------------------------- 
SPOKES=1

bart traj -x $SAMPLES -y $SPOKES -s${GA} -c -G -t ${REP} -D -r _traj

# two-fold oversampling
bart scale -- 0.5 _traj{,2}

# reshape traj to create artificial spoke averaging
## speeds up the reconstruction for better testing
bart extract 10 0 $((TIME_STEPS*AV)) _traj{2,3}
bart reshape $(bart bitmask 2 10) ${AV} ${TIME_STEPS} _traj{3,4}

rm _traj{,2,3}.{cfl,hdr}


# Move time dimension: (5) -> (10) as required by moba
bart transpose 5 10 _traj4 traj

rm _traj4.{cfl,hdr} || :


echo "Generated output files: traj.{cfl,hdr}" >&2
