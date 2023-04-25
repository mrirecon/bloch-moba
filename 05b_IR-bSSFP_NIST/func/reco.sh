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

if [ -z ${OPTS+x} ];
then
        echo "${REL_PATH}/opts.sh is not actively set." >&2
        exit 1
fi

source $OPTS


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


B1MAP=b1map

ex=1

if [ ! -f ${B1MAP}".cfl" ];
then
        echo "B1 map $B1MAP does not exist!"
        echo "Please run LL model and b1 script first."
        exit 1
fi

SLICE_THICKNESS=0.02
NOM_SLICE_THICKNESS=0.005

if [[ "$PERFECT_INVERSION" == "1" ]];
then

         # Constant Inversion Efficiency

        if [[ "$SLICEPROFILE" == "1" ]];
        then

                echo "Constant Inversion Efficiency + Slice Profile Simulation"

                nice -5 bart moba --bloch --sim STM \
                --img_dims $BR:$BR:1 \
                --seq IR-BSSFP,TR=${TR},TE=${TE},FA=${FA},Trf=${RF_DUR},BWTP=${BWTP},pinv,ipl=0,ppl=${PREP_LEN},sl-grad=${SS_GRAD_STRENGTH},isp=$(echo $INV_LEN $INV_SPOILER | awk '{print $1+$2}'),av-spokes=${AV},slice-thickness=${SLICE_THICKNESS},nom-slice-thickness=${NOM_SLICE_THICKNESS},Nspins=${SLICE_PROFILE_SPINS} \
                --other pinit=1:1:1:0,pscale=1:1:30:0,b1map=${B1MAP},b1-sobolev-a=440,b1-sobolev-b=22 --scale_data=5000. --scale_psf=1000. --normalize_scaling \
                -i$ITER -C$INNER_ITER -s$STEP_SIZE -B$MIN_R1 -d4 -o$OS -R$REDU_FAC -j$LAMBDA -g -N \
		--pusteps 4 --ratio 0.5 \
                -t ${TRAJ} ${DATA} TI reco sens \
                2>&1 | tee reco.log

                ex=$?
        else
                echo "Constant Inversion Efficiency"

                nice -5 bart moba --bloch --sim STM \
                --img_dims $BR:$BR:1 \
                --seq IR-BSSFP,TR=${TR},TE=${TE},FA=${FA},Trf=${RF_DUR},BWTP=${BWTP},pinv,ipl=0,ppl=${PREP_LEN},sl-grad=${SS_GRAD_STRENGTH},isp=$(echo $INV_LEN $INV_SPOILER | awk '{print $1+$2}'),av-spokes=${AV},Nspins=${SLICE_PROFILE_SPINS} \
                --other pinit=1:1:1:0,pscale=1:1:30:0,b1map=${B1MAP},b1-sobolev-a=440,b1-sobolev-b=22 --scale_data=5000. --scale_psf=1000. --normalize_scaling \
                -i$ITER -C$INNER_ITER -s$STEP_SIZE -B$MIN_R1 -d4 -o$OS -R$REDU_FAC -j$LAMBDA -g -N \
		--pusteps 4 --ratio 0.5 \
                -t ${TRAJ} ${DATA} TI reco sens \
                2>&1 | tee reco.log

                ex=$?

        fi

else
       # Hyper Secant Inversion Model

        if [[ "$SLICEPROFILE" == "1" ]];
        then
                echo "Hyper Secant Inversion Model + Slice Profile Simulation"

                nice -5 bart moba --bloch --sim STM \
                --img_dims $BR:$BR:1 \
                --seq IR-BSSFP,TR=${TR},TE=${TE},FA=${FA},Trf=${RF_DUR},BWTP=${BWTP},ipl=${INV_LEN},ppl=${PREP_LEN},sl-grad=${SS_GRAD_STRENGTH},isp=${INV_SPOILER},av-spokes=${AV},slice-thickness=${SLICE_THICKNESS},nom-slice-thickness=${NOM_SLICE_THICKNESS},Nspins=${SLICE_PROFILE_SPINS} \
		--other pinit=1:1:1:0,pscale=1:1:30:0,b1map=${B1MAP},b1-sobolev-a=440,b1-sobolev-b=22 --scale_data=5000. --scale_psf=1000. --normalize_scaling \
                -i$ITER -C$INNER_ITER -s$STEP_SIZE -B$MIN_R1 -d4 -o$OS -R$REDU_FAC -j$LAMBDA -g -N \
		--pusteps 4 --ratio 0.5 \
                -t ${TRAJ} ${DATA} TI reco sens \
                2>&1 | tee reco.log

                ex=$?
        else
                echo "Hyper Secant Inversion Model"

                nice -5 bart moba --bloch --sim STM \
                --img_dims $BR:$BR:1 \
                --seq IR-BSSFP,TR=${TR},TE=${TE},FA=${FA},Trf=${RF_DUR},BWTP=${BWTP},ipl=${INV_LEN},ppl=${PREP_LEN},sl-grad=${SS_GRAD_STRENGTH},isp=${INV_SPOILER},av-spokes=${AV},Nspins=${SLICE_PROFILE_SPINS} \
                --other pinit=1:1:1:0,pscale=1:1:30:0,b1map=${B1MAP},b1-sobolev-a=440,b1-sobolev-b=22 --scale_data=5000. --scale_psf=1000. --normalize_scaling \
                -i$ITER -C$INNER_ITER -s$STEP_SIZE -B$MIN_R1 -d4 -o$OS -R$REDU_FAC -j$LAMBDA -g -N \
		--pusteps 4 --ratio 0.5 \
                -t ${TRAJ} ${DATA} TI reco sens \
                2>&1 | tee reco.log

                ex=$?
        fi
fi

exit $ex