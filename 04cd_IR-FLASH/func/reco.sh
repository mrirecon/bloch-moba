#!/bin/bash

set -eux
set -o pipefail

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

KSP=$1
TRAJ=$2
DATA=$3

# Load and Extract Reconstruction information

if [ ! -f ${REL_PATH}/opts.sh ];
then
	echo "${REL_PATH}/opts.sh does not exist." >&2
	exit 1
fi

source ${REL_PATH}/opts.sh


SPOKES=$(bart show -d 1 ${KSP})
COILS=$(bart show -d 3 ${KSP})
FRAMES=$(bart show -d 10 ${KSP})
BR=$(($(bart show -d 0 ${KSP})/2))
SAMPLES=$(echo $BR 2 | awk '{printf "%3.0f\n",$1*$2}')


TIME_STEPS=$((FRAMES/AV))   # Integer division!


# Create log file

[ -f reco.log ] && rm reco.log
touch reco.log


# Create inversion time (required for Look-Locker model)

bart index 5 ${TIME_STEPS} _TI

bart scale $(echo ${TR} ${AV} | awk '{printf "%1.5f\n",$1*$2}') _TI{,s}

bart ones 6 1 1 1 1 1 ${TIME_STEPS} _one

bart saxpy $(echo ${TR} $((AV/2)) | awk '{printf "%1.5f\n",$1*$2}') _one _TIs TI

rm _TI{,s}.{cfl,hdr} _one.{cfl,hdr}

ex=1

case $MODEL in

LL)
        ITER=10
        LAMBDA=0.007

        nice -5 bart moba -L \
        --img_dims $BR:$BR:1 \
        -i$ITER -C$INNER_ITER -s$STEP_SIZE -B$MIN_R1 -d4 -o$OS -R$REDU_FAC -j$LAMBDA -g -N \
        --other pinit=1:1:2:1 --scale_data=5000. --scale_psf=1000. --normalize_scaling \
        -t ${TRAJ} ${DATA} TI reco sens \
        2>&1 | tee reco.log

        ex=$?
        ;;

M0A)
        ITER=15
        LAMBDA=0.0008

        nice -5 bart moba -P --seq TR=${TR} \
        --img_dims $BR:$BR:1 \
        -i$ITER -C$INNER_ITER -s$STEP_SIZE -B$MIN_R1 -d4 -o$OS -R$REDU_FAC -j$LAMBDA -g -N \
        --other pinit=1:1:2:1 --scale_data=5000. --scale_psf=1000. --normalize_scaling \
        -t ${TRAJ} ${DATA} TI reco sens \
        2>&1 | tee reco.log

        ex=$?
        ;;

Bloch)
        RF_DUR=0.001
        INV_LEN=0
        PREP_LEN=0
        INV_SPOILER=0

        ITER=13
        LAMBDA=0.0008

        nice -5 bart moba --bloch --sim STM \
        --img_dims $BR:$BR:1 \
	--seq IR-FLASH,TR=${TR},TE=${TE},FA=${FA},Trf=${RF_DUR},BWTP=${BWTP},pinv,ipl=${INV_LEN},ppl=${PREP_LEN},isp=${INV_SPOILER},av-spokes=${AV} \
        --other pinit=3:1:1:1,pscale=1:1:1:0.1 --scale_data=5000. --scale_psf=1000. --normalize_scaling \
        -i$ITER -C$INNER_ITER -s$STEP_SIZE -B$MIN_R1 -d4 -o$OS -R$REDU_FAC -j$LAMBDA -g -N \
        -t ${TRAJ} ${DATA} TI reco sens \
        2>&1 | tee reco.log

        ex=$?
        ;;

Bloch_SP)
        RF_DUR=0.001
        INV_LEN=0.01
        PREP_LEN=0
        INV_SPOILER=0.005
        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.012
        SLICE_THICKNESS=0.02
	NOM_SLICE_THICKNESS=0.005

        ITER=13 #15
        LAMBDA=0.0005 #2

        nice -5 bart moba --bloch --sim STM \
        --img_dims $BR:$BR:1 \
        --seq IR-FLASH,TR=${TR},TE=${TE},FA=${FA},Trf=${RF_DUR},BWTP=${BWTP},ipl=${INV_LEN},ppl=${PREP_LEN},isp=${INV_SPOILER},av-spokes=${AV},sl-grad=${SS_GRAD_STRENGTH},slice-thickness=${SLICE_THICKNESS},nom-slice-thickness=${NOM_SLICE_THICKNESS},Nspins=${SLICE_PROFILE_SPINS} \
        --other pinit=3:1:1:1,pscale=1:1:1:0.1 --scale_data=5000. --scale_psf=1000. --normalize_scaling \
        -i$ITER -C$INNER_ITER -s$STEP_SIZE -B$MIN_R1 -d4 -o$OS -R$REDU_FAC -j$LAMBDA -g -N \
        -t ${TRAJ} ${DATA} TI reco sens \
        2>&1 | tee reco.log

        ex=$?
        ;;
esac

exit $ex