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

# Load data path
source ../utils/data_loc.sh
KSP_PATH="${DATA_LOC}"/data_06_irflash

# Prepare kspace data for reconstruction
./func/prepare_data.sh ${KSP_PATH}

# Estimate reference coil-profiles
#./func/coil_reference.sh data traj

# Run reconstrution
./func/reco.sh ${KSP_PATH} traj data

# Postprocess data
./func/post_process.sh mask/mask

# Move data to model folder
./func/move_results.sh
