#!/bin/bash

# Download dataset from zenodo

ZENODO="https://zenodo.org/record/7654462/files"

FILES=(data_06_b1map data_06_irflash data_06_irbssfp_short data_06_irbssfp_long)
OUT=(ksp_b1map ksp_flash ksp_short ksp_long)

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
