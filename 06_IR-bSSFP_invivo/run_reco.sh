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
	;;

Bloch_long)
	RAW=ksp_long
	;;
esac


# Load required parameters
source func/opts.sh

# Load SS IR FLASH data
./data/load_data.sh

# Load B1 map
if [[ "$MODEL" == "Bloch_short" ]] || [[ "$MODEL" == "Bloch_long" ]];
then
	./b1map/load_b1map.sh mask/mask
fi

# Prepare kspace data for reconstruction
./func/prepare_data.sh ${RAW}

# Run reconstrution
./func/reco.sh ${RAW} traj data

# Postprocess data
./func/post_process.sh mask/mask

# Move data to model folder
./func/move_results.sh