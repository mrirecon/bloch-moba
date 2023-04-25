#!/bin/bash

GA=13
AV_COILS=5
AV=15


# Optimization Parameter
OS=1
REDU_FAC=3
INNER_ITER=250
STEP_SIZE=0.95
MIN_R1=0.001


# Model specifics
case ${MODEL} in

LL)

        TR=0.00375
        TE=0.00226
        FA=8
        RF_DUR=0.001
	BWTP=4
        INV_LEN=0
        PREP_LEN=0
        INV_SPOILER=0
        DELAY=0.0153
        ;;

Bloch_flash)

	TR=0.00375
        TE=0.00226
        FA=8
        RF_DUR=0.001
	BWTP=4
        INV_LEN=0.01
        PREP_LEN=0
        INV_SPOILER=0.005
        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.01879
        ;;

Bloch_2_5)

        TR=0.00614
        TE=0.00307
        FA=35
        RF_DUR=0.0025
	BWTP=1
        INV_LEN=0.01
        PREP_LEN=${TE}
        INV_SPOILER=0.005
        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.00188
        ;;

Bloch_2_1)

        TR=0.0055
        TE=0.00275
        FA=35
        RF_DUR=0.0021
	BWTP=1
        INV_LEN=0.01
        PREP_LEN=${TE}
        INV_SPOILER=0.005
        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.00224
        ;;

Bloch_1_6)

        TR=0.005
        TE=0.0025
        FA=35
        RF_DUR=0.0016
	BWTP=1
        INV_LEN=0.01
        PREP_LEN=${TE}
        INV_SPOILER=0.005
        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.00294
        ;;

Bloch_1_2)

        TR=0.0046
        TE=0.0023
        FA=35
        RF_DUR=0.0012
	BWTP=1
        INV_LEN=0.01
        PREP_LEN=${TE}
        INV_SPOILER=0.005
        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.00391
        ;;

Bloch_0_6)

        TR=0.004
        TE=0.002
        FA=35
        RF_DUR=0.0006
	BWTP=1
        INV_LEN=0.01
        PREP_LEN=${TE}
        INV_SPOILER=0.005
        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.00783
        ;;

Bloch_0_4)

        TR=0.0038
        TE=0.0019
        FA=35
        RF_DUR=0.0004
	BWTP=1
        INV_LEN=0.01
        PREP_LEN=${TE}
        INV_SPOILER=0.005
        SLICE_PROFILE_SPINS=21
        SS_GRAD_STRENGTH=0.01174
        ;;
esac
