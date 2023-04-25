#!/bin/bash

set -eux

# Check if BART is set up correctly

if [ ! -e $TOOLBOX_PATH/bart ] ;
then
	echo "\$TOOLBOX_PATH is not set correctly!" >&2
	exit 1
fi

export PATH=$TOOLBOX_PATH:$PATH

# Load required parameters
if [ $# -le 1 ]
then
	export OPTS=func/opts.sh
else
	export OPTS=$2
fi

source $OPTS


# Load data path
source ../utils/data_loc.sh
B1_PATH="${DATA_LOC}"/data_05b_b1map
KSP_PATH="${DATA_LOC}"/data_05b_kspace

# Load B1 map
./b1map/load_b1map.sh "${B1_PATH}"

# Prepare kspace data for reconstruction
./func/prepare_data.sh "${KSP_PATH}"

# Run reconstrution
./func/reco.sh "${KSP_PATH}" traj data

# Postprocess data
./func/post_process.sh

# Move data to model folder
./func/move_results.sh $1
