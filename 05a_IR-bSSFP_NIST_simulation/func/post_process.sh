#!/bin/bash

set -eux

# Check if BART is set up correctly

if [ ! -e $TOOLBOX_PATH/bart ] ;
then
	echo "\$TOOLBOX_PATH is not set correctly!" >&2
	exit 1
fi

export PATH=$TOOLBOX_PATH:$PATH


# Estimate relative paths

FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})

# Load and Extract Reconstruction information

if [ -z ${OPTS+x} ];
then
        echo "opts.sh is not actively set." >&2

	OPTS=${REL_PATH}/opts.sh
fi

source $OPTS

SAMPLES=$(bart show -d 0 reco)

# Create Mask based on M0 map
bart slice 6 1 {reco,_m0map}

bart threshold -B 0.8 _m0map{,2}

bart morphop -c 15 _m0map2 _mask

bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) {_,}mask

rm _mask.{cfl,hdr} _m0map{,2}.{cfl,hdr}

# Estimate correct parameter maps

bart slice 6 0 reco _r1map
bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) _r1map r1map
# ${REL_PATH}/plot_map.py 2 0 r1map{,} '$R_1$ [Hz]'
bart spow -- -1 r1map _t1map
bart fmac mask _t1map t1map
# ${REL_PATH}/plot_map.py 2 0.4 t1map{,} '$T_1$ [s]'
rm _{r,t}1map.{cfl,hdr}

bart slice 6 2 reco _r2map
bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) _r2map r2map
# ${REL_PATH}/plot_map.py 1.5 0.5 r2map{,} '$R_2$'
bart spow -- -1 r2map _t2map
bart fmac mask _t2map t2map
# ${REL_PATH}/plot_map.py 2 0.4 t2map{,} '$T_2$ [s]'
rm _{r,t}2map.{cfl,hdr}



[ -d tmp ] && rm -rf tmp
mkdir tmp

# Create initial masks
bart phantom --NIST -x $((SAMPLES/2)) -b tmp/tubes

# Shrink masks to rois
bart morphop -e 3 tmp/tubes rois

rm -rf tmp || :
