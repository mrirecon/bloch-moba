#!/bin/bash

# Download dataset from zenodo

ZENODO="https://zenodo.org/record/6992763/files"

FILE=data_06_b1map

if [[ ! -f "b1map_smooth.cfl" ]];
then
	wget "${ZENODO}/${FILE}.cfl"
	wget "${ZENODO}/${FILE}.hdr"

	bart copy ${FILE} b1map_smooth

	rm ${FILE}.{cfl,hdr}

	echo "Generated output file: b1map_smooth.{cfl,hdr}" >&2
fi
