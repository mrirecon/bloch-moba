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

# Choose Dataset
case ${MODEL} in

LL)
	SUFF=irflash
	;;
Bloch_flash)
	SUFF=irflash
	;;
Bloch_2_5)
	SUFF=irbssfp_2_5ms
	;;
Bloch_2_1)
	SUFF=irbssfp_2_1ms
	;;
Bloch_1_6)
	SUFF=irbssfp_1_6ms
	;;
Bloch_1_2)
	SUFF=irbssfp_1_2ms
	;;
Bloch_0_6)
	SUFF=irbssfp_0_6ms
	;;
Bloch_0_4)
	SUFF=irbssfp_0_4ms
	;;
esac


# Load required parameters
source func/opts.sh

# Load data path
source ../utils/data_loc.sh
B1_PATH="${DATA_LOC}"/data_s03_b1map
RAW_KSP_PATH="${DATA_LOC}"/data_s03_"${SUFF}"
KSP_PATH=data_s03_"${SUFF}"_first1200

if [ "${MODEL}" != "LL" ]
then
	echo "Load B1 map"
	
	# Load B1 map
	./b1map/load_b1map.sh "${B1_PATH}"
fi

# Prepare kspace data for reconstruction
./func/prepare_data.sh "${RAW_KSP_PATH}" "${KSP_PATH}"

# Run reconstrution
./func/reco.sh "${KSP_PATH}" traj data

# Postprocess data
./func/post_process.sh mask/mask

# Move data to model folder
./func/move_results.sh
