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


# Load and Extract Reconstruction information

if [ ! -f ${REL_PATH}/opts.sh ];
then
	echo "${REL_PATH}/opts.sh does not exist." >&2
	exit 1
fi

source ${REL_PATH}/opts.sh


SPOKES=$(bart show -d 1 ${KSP})
COILS=$(bart show -d 3 ${KSP})
FRAMES=$(bart show -d 10 ${KSP})
BR=$(($(bart show -d 0 ${KSP})/2))
SAMPLES=$(echo $BR 2 | awk '{printf "%3.0f\n",$1*$2}')

TIME_STEPS=$((FRAMES/AV))   # Integer division!

#-----------------------------------------------
#-------------- Data Compression ---------------
#----------------------------------------------- 

bart cc -p $AV_COILS -A  $KSP _kspcc

# Switch dimensions (0,1) -> (1,2) to work with nufft tools
bart transpose 1 2 _kspcc _tmp
bart transpose 0 1 _tmp data

rm _tmp.{cfl,hdr} _kspcc.{cfl,hdr}


#-----------------------------------------------
#------------------ Trajectory -----------------
#----------------------------------------------- 

bart traj -x $SAMPLES -y $SPOKES -s${GA} -G -t $FRAMES -D -r _traj

# Perform Gradient delay correction on timesteps in steady-state
## 1. Extract 150 spokes from steady state to estimate graident delays
## 2. transpose time to spoke dimension
## 3. flip spoke order to allow for first iterations in steady state
bart extract 10 $((FRAMES-150)) $FRAMES data{,2}
bart transpose 2 10 data{2,3}
bart flip $(bart bitmask 2) data{3,4}

bart extract 10 $((FRAMES-150)) $FRAMES _traj{,2}
bart transpose 2 10 _traj{2,3}
bart flip $(bart bitmask 2) _traj{3,4}

bart traj -x $SAMPLES -y $SPOKES -s${GA} -G -t $FRAMES -D -r -O -q $(bart estdelay -R _traj4 data4) _traj5

bart scale -- 0.5 _traj5 traj


rm _traj{,2,3,4,5}.{cfl,hdr} data{2,3,4}.{cfl,hdr}


#-----------------------------------------------
#---------------- Data Reshape -----------------
#----------------------------------------------- 
# reshape traj and data to create artificial spoke averaging
## speeds up the reconstruction for better testing

bart extract 10 0 $((TIME_STEPS*AV)) traj _tmp
bart reshape $(bart bitmask 2 10) ${AV} ${TIME_STEPS} _{tmp,traj}

bart extract 10 0 $((TIME_STEPS*AV)) data _tmp1
bart transpose 2 3 _tmp{1,2}
bart reshape $(bart bitmask 3 10) ${AV} ${TIME_STEPS} _tmp{2,3}
bart transpose 2 3 _tmp3 _data

rm {traj,data}.{cfl,hdr}

# Move time dimension for (5) -> (10) as required by moba
bart transpose 5 10 {_,}data
bart transpose 5 10 {_,}traj

rm _traj.{cfl,hdr} _data.{cfl,hdr} _tmp{,1,2,3}.{cfl,hdr}



echo "Generated output files: {traj,data}.{cfl,hdr}" >&2
