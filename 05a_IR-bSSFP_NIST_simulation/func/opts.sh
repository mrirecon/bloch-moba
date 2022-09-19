#!/bin/bash

GA=7
AV_COILS=3
SIM_COILS=8
AV=1

# Optimization Parameter
OS=1
REDU_FAC=3
INNER_ITER=250
STEP_SIZE=0.95
MIN_R1=0.001

ITER=15
LAMBDA=0.0005

BR=192

# Model specifics
BWTP=4
TR=0.00488
TE=0.00244
REP=1000
FA=45
PREP_LEN=${TE}
RF_DUR=0.001
INV_LEN=0.01
INV_SPOILER=0.005

SLICE_THICKNESS=0.02


case ${MODEL} in


SP_PI)  # Slice-Profile AND Perfect Inversion

        SLICEPROFILE=1
        PERFECT_INVERSION=1

        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.012
        NOM_SLICE_THICKNESS=0.005
        ;;

NSP_PI)  # No Slice-Profile AND Perfect Inversion

        SLICEPROFILE=0
        PERFECT_INVERSION=1

        SLICE_PROFILE_SPINS=1
        SS_GRAD_STRENGTH=0
        ;;

SP_NPI)  # Slice-Profile AND No Perfect Inversion

        SLICEPROFILE=1
        PERFECT_INVERSION=0

        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.012
        NOM_SLICE_THICKNESS=0.005
        ;;

NSP_NPI)  # No Slice-Profile AND No Perfect Inversion

        SLICEPROFILE=0
        PERFECT_INVERSION=0

        SLICE_PROFILE_SPINS=1
        SS_GRAD_STRENGTH=0
        ;;
esac



