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


# Load required parameters
source func/opts.sh

# Load SS IR FLASH data
./data/load_data.sh

# Prepare kspace data for reconstruction
./func/prepare_data.sh ksp

# Estimate reference coil-profiles
./func/coil_reference.sh data traj

# Run reconstrution
./func/reco.sh ksp traj data

# Postprocess data
./func/post_process.sh mask/mask

# Move data to model folder
./func/move_results.sh