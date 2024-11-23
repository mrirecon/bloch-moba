#!/bin/bash

set -e

export BART_COMPAT_VERSION=v0.9.00

# Run reconstructions
[ ! -d results/LL_1 ] && ./run_reco.sh LL 1

[ ! -d results/M0A_1 ] && ./run_reco.sh M0A 1


WAV=(1 0.5 0.25 0.1 0.01 0.001 0.0001)

for (( i=0; i<${#WAV[@]}; i++ ));
do
	echo "${WAV[$i]}"

	[ ! -d results/Bloch_${WAV[$i]} ] && ./run_reco.sh Bloch "${WAV[$i]}"
done

# Sort datasets

bart join 7 $(find results/Bloch_*/t1map.cfl | sed -e 's/\.cfl//') results/joined_t1


# Order
echo "Ordering of files!"

FILE=results/order.txt
[ -f ${FILE} ] && rm ${FILE}
touch ${FILE}

# Init R1
echo $(find results/Bloch_*/t1map.cfl | sed -e 's/results\/Bloch_//' | sed -e 's/\/t1map.cfl//' ) >> ${FILE}


# Improve testing

# Join ROIs
bart join 6 $(ls vertices/*.cfl | sed -e 's/\.cfl//') results/rois

for (( i=0; i<${#WAV[@]}; i++ ));
do
	echo "${WAV[$i]}"

	bart fmac results/Bloch_${WAV[$i]}/t1map results/rois results/Bloch_${WAV[$i]}/t1_test
done

rm results/rois.{cfl,hdr}