#!/bin/bash

set -ex

[ -d tmp ] &&  rm -rf tmp
mkdir tmp

# Download datasets

ZENODO="https://zenodo.org/record/7654462/files"

FILES=(data_GSM_t1 data_GSM_t2)
OUT=(tmp/dataTI tmp/dataTE)

for (( i=0; i<${#FILES[@]}; i++ ));
do
	if [[ ! -f "${OUT[$i]}.cfl" ]];
	then
		wget "${ZENODO}/${FILES[$i]}.cfl"
		wget "${ZENODO}/${FILES[$i]}.hdr"

		bart copy ${FILES[$i]} ${OUT[$i]}

		rm ${FILES[$i]}.{cfl,hdr}

		echo "Generated output file: ${OUT[$i]}.{cfl,hdr}" >&2
	fi
done

# Reconstruct multi inversion dataset
bart fft -i 7 tmp/dataTI tmp/tmp
bart resize -c 0 256 1 256 tmp/tmp tmp/reco
bart rss 8 tmp/reco recoTI

# Reconstruct multi echo dataset
bart fft -i 7 tmp/dataTE tmp/tmp
bart resize -c 0 256 1 256 tmp/tmp tmp/reco
bart rss 8 tmp/reco recoTE


# Pixel-wise fitting of reconstructed intermediate images
python3 mapping.py recoTI T1 0.030 0.250 mapT1

# Pixel-wise fitting of reconstructed intermediate images
python3 mapping.py recoTE T2 0.015 0.040 mapT2


rm -rf tmp
rm recoTI.{cfl,hdr}
rm recoTE.{cfl,hdr}
