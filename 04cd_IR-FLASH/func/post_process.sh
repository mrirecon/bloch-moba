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

if [ ! -f ${REL_PATH}/opts.sh ];
then
	echo "${REL_PATH}/opts.sh does not exist." >&2
	exit 1
fi

source ${REL_PATH}/opts.sh

# Load required data

SAMPLES=$(bart show -d 0 reco)

MASK=$1


# Estimate correct parameter maps

case $MODEL in

LL)
        M0_THRESH=0.2

        bart looklocker -t $M0_THRESH -D $DELAY reco{,2}

        # Print maps
        bart slice 6 0 {reco2,_t1map}
        bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) _t1map t1map
        # ${REL_PATH}/plot_map.py 2 0.4 t1map{,} '$T_1$ [s]'
        rm _t1map.{cfl,hdr}

        # Create a mask
        bart threshold -B 0.1 {t1map,_mask}
        bart morphop -c 9 {_,}mask
        # ${REL_PATH}/plot_map.py 4 0 mask{,} 'mask'
        rm _mask.{cfl,hdr}

        # create a mask
        if [ ! -f $MASK".cfl" ];
        then
                mkdir mask || :
                bart copy mask ${MASK}
        fi
        rm mask.{cfl,hdr}
        ;;
M0A)
        if [ ! -f $MASK".cfl" ]; then

                echo "Mask $MASK does not exist!"
                echo "Please run LL model first."
                exit 1
        fi

        bart slice 6 1 reco _r1map2
        bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) _r1map{2,}
        bart spow -- -1 _r1map _t1map
        # ${REL_PATH}/plot_map.py 2 0 _t1map2 t1map '$R_1$ [Hz]'
        rm _r1map{,2}.{cfl,hdr}

        # correct t1 map for initial relaxation effects
        bart ones 2 $((SAMPLES/2)) $((SAMPLES/2)) _ones
        bart saxpy -- $(echo 2 ${DELAY} | awk '{printf "%f\n",$1*$2}') _ones _t1map{,2}
        bart fmac $MASK _t1map2 t1map
        # ${REL_PATH}/plot_map.py 2 0.4 t1map{,} '$T_1$ [s]'
        rm _ones.{cfl,hdr} _t1map{,2}.{cfl,hdr}

        bart slice 6 2 {reco,_famap}
        bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) _famap{,2}
        bart fmac $MASK _famap2 famap
        bart scale -- $(echo ${FA} | awk '{printf "%f\n",1/$1}') famap{,_rel}
        # ${REL_PATH}/plot_map.py 1.5 0.5 famap{_rel,} 'rel. FA'
        rm _famap.{cfl,hdr}
        ;;

Bloch)

        if [ ! -f $MASK".cfl" ]; then

                echo "Mask $MASK does not exist!"
                echo "Please run LL model first."
                exit 1
        fi

        bart slice 6 0 reco _r1map2
        bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) _r1map{2,}
        bart spow -- -1 _r1map _t1map
        # ${REL_PATH}/plot_map.py 2 0 _t1map2 t1map '$R_1$ [Hz]'
        rm _r1map{,2}.{cfl,hdr}

        # correct t1 map for initial relaxation effects
        bart ones 2 $((SAMPLES/2)) $((SAMPLES/2)) _ones
        bart saxpy -- $(echo 2 ${DELAY} | awk '{printf "%f\n",$1*$2}') _ones _t1map _t1map2
        bart fmac $MASK _t1map2 t1map
        # ${REL_PATH}/plot_map.py 2 0.4 t1map{,} '$T_1$ [s]'
        rm _ones.{cfl,hdr} _t1map{,2}.{cfl,hdr}

        bart slice 6 1 {reco,_m0map}
        bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) _m0map{,2}
        bart fmac $MASK _m0map2 m0map
        # ${REL_PATH}/plot_map.py 2 0 m0map{,} '$M_0$ [Hz]'
        rm _m0map.{cfl,hdr}

        bart slice 6 3 {reco,_b1map}
        bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) _b1map{,2}
        bart fmac $MASK _b1map2 b1map
        # ${REL_PATH}/plot_map.py 1.5 0.5 b1map{,} '$B_1$'
        rm _b1map.{cfl,hdr}

        bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) sens{,c}
        ;;

Bloch_SP)

        if [ ! -f $MASK".cfl" ]; then

                echo "Mask $MASK does not exist!"
                echo "Please run LL model first."
                exit 1
        fi

        bart slice 6 0 reco _r1map
        bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) _r1map r1map
        # ${REL_PATH}/plot_map.py 2 0 r1map{,} '$R_1$ [Hz]'
        bart spow -- -1 r1map _t1map
        bart fmac $MASK _t1map t1map
        # ${REL_PATH}/plot_map.py 2 0.4 t1map{,} '$T_1$ [s]'
        rm _{r,t}1map.{cfl,hdr}

        bart slice 6 2 reco _r2map
        bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) _r2map r2map
        # ${REL_PATH}/plot_map.py 1.5 0.5 r2map{,} '$R_2$'
        bart spow -- -1 r2map _t2map
        bart fmac $MASK _t2map t2map
        # ${REL_PATH}/plot_map.py 2 0.4 t2map{,} '$T_2$ [s]'
        rm _{r,t}2map.{cfl,hdr}

        bart slice 6 1 reco _m0map
        bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) _m0map{,2}
        bart fmac $MASK _m0map2 m0map
        # ${REL_PATH}/plot_map.py 2 0 m0map{,} '$M_0$ [Hz]'
        rm _m0map.{cfl,hdr}

        bart slice 6 3 {reco,_b1map}
        bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) _b1map{,2}
        bart fmac $MASK _b1map2 b1map
        # ${REL_PATH}/plot_map.py 1.5 0.5 b1map{,} '$B_1$'
        rm _b1map.{cfl,hdr}

        bart resize -c 0 $((SAMPLES/2)) 1 $((SAMPLES/2)) sens{,c}
        ;;
esac