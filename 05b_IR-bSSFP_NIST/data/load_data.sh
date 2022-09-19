#!/bin/bash

# Download dataset from zenodo

ZENODO="https://zenodo.org/record/6992763/files"

FILE=data_05b_kspace

if [[ ! -f "ksp.cfl" ]];
then
	wget "${ZENODO}/${FILE}.cfl"
	wget "${ZENODO}/${FILE}.hdr"

	bart copy ${FILE} ksp

	rm ${FILE}.{cfl,hdr}

	echo "Generated output file: ksp.{cfl,hdr}" >&2
fi
