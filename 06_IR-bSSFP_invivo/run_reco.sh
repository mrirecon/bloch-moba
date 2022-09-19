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

LL | Bloch_flash)
	RAW=ksp_flash
	;;

Bloch_short)

	RAW=ksp_short

	# Load B1 map
	./b1map/load_b1map.sh mask/mask
	;;

Bloch_long)

	RAW=ksp_long

	# Load B1 map
	./b1map/load_b1map.sh mask/mask
	;;
esac


# Load required parameters
source func/opts.sh

# Load SS IR FLASH data
./data/load_data.sh

# Prepare kspace data for reconstruction
./func/prepare_data.sh ${RAW}

# Run reconstrution
./func/reco.sh ${RAW} traj data

# Postprocess data
./func/post_process.sh mask/mask

# Move data to model folder
./func/move_results.sh