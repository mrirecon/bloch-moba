#!/bin/bash

set -e

# Run reconstructions
MODELS=(LL Bloch_flash Bloch_2_5 Bloch_2_1 Bloch_1_6 Bloch_1_2 Bloch_0_6 Bloch_0_4)

# Join ROIs
bart join 2 $(ls vertices/v*.cfl | sed -e 's/\.cfl//') results/rois

# Run Reconstructions
for (( i=0; i<${#MODELS[@]}; i++ ));
do
	echo ${MODELS[$i]}

	[ ! -d results/${MODELS[$i]} ] && ./run_reco.sh "${MODELS[$i]}"

	# Improve testing: Extract ROIs

	CURRENT_MODEL="${MODELS[$i]}"

	echo ${CURRENT_MODEL}

	bart fmac results/${CURRENT_MODEL}/t1map results/rois results/${CURRENT_MODEL}/t1_test

	if [ "$CURRENT_MODEL" = "LL" ] || [ "$CURRENT_MODEL" = "Bloch_flash" ];
        then
                echo "No T2 map for this case."
        else
		bart fmac results/${CURRENT_MODEL}/t2map results/rois results/${CURRENT_MODEL}/t2_test
	fi
done

rm results/rois.{cfl,hdr}