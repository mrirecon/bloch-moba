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

export OPTS=func/opts.sh

source func/opts.sh

# Prepare kspace data for reconstruction
./func/prepare_data.sh

# Simulate kspace
./func/simulation.sh traj

# Run reconstrution
./func/reco.sh ksp traj

# Postprocess data
./func/post_process.sh

# Move data to model folder
./func/move_results.sh $MODEL