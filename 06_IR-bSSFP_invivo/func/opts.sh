#!/bin/bash

GA=7
AV_COILS=5
AV=15

# Sequence Parameter
BWTP=4

# Optimization Parameter
OS=1
REDU_FAC=3
INNER_ITER=250
STEP_SIZE=0.95
MIN_R1=0.001


# Model specifics
case ${MODEL} in

LL)

        TR=0.0041
        TE=0.00258
        FA=6
        RF_DUR=0.001
        INV_LEN=0
        PREP_LEN=0
        INV_SPOILER=0
        DELAY=0.0153
        ;;

Bloch_flash)

        TR=0.0041
        TE=0.00258
        FA=6
        RF_DUR=0.001
        INV_LEN=0.01
        PREP_LEN=0
        INV_SPOILER=0.005
        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.012
        ;;

Bloch_short)

        TR=0.00488
        TE=0.00244
        FA=45
        PREP_LEN=${TE}
        RF_DUR=0.001
        INV_LEN=0.01
        INV_SPOILER=0.005
        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.012
        ;;

Bloch_long)

        TR=0.0108
        TE=0.0054
        FA=45
        PREP_LEN=${TE}
        RF_DUR=0.0025
        INV_LEN=0.01
        INV_SPOILER=0.005
        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.012
        ;;
esac
