#!/bin/bash

set -eux

# Check if BART is set up correctly

if [ ! -e $TOOLBOX_PATH/bart ] ;
then
	echo "\$TOOLBOX_PATH is not set correctly!" >&2
	exit 1
fi

export PATH=$TOOLBOX_PATH:$PATH


export MODEL=$1

# Load Model dependencies

case ${MODEL} in

LL)
	SUFF=irflash
	;;

Bloch | Bloch_c | Bloch_cr)

	SUFF=irbssfp_short
	;;

esac


# Load required parameters
source func/opts.sh

# Load data path
source ../utils/data_loc.sh
B1_PATH="${DATA_LOC}"/data_06_b1map
KSP_PATH="${DATA_LOC}"/data_06_"${SUFF}"

# Load B1 map
if [[ "$MODEL" == "Bloch" ]] || [[ "$MODEL" == "Bloch_c" ]] || [[ "$MODEL" == "Bloch_cr" ]];
then
	./b1map/load_b1map.sh "${B1_PATH}"
fi

# Prepare kspace data for reconstruction
./func/prepare_data.sh ${KSP_PATH}

# Run reconstrution
./func/reco.sh ${KSP_PATH} traj data

# Postprocess data
./func/post_process.sh mask/mask

# Move data to model folder
./func/move_results.sh
