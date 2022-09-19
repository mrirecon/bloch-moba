#!/bin/bash

set -eux

# Check if BART is set up correctly

if [ ! -e $TOOLBOX_PATH/bart ] ;
then
	echo "\$TOOLBOX_PATH is not set correctly!" >&2
	exit 1
fi

export PATH=$TOOLBOX_PATH:$PATH

# Load B1 map
./b1map/load_b1map.sh

# Load required parameters
if [ $# -le 1 ]
then
	export OPTS=func/opts.sh
else
	export OPTS=$2
fi

source $OPTS


# Load SS IR bSSFP data
./data/load_data.sh

# Prepare kspace data for reconstruction
./func/prepare_data.sh ksp

# Run reconstrution
./func/reco.sh ksp traj data

# Postprocess data
./func/post_process.sh

# Move data to model folder
./func/move_results.sh $1