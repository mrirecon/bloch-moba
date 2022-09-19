#!/bin/bash

set -eux

# Check if BART is set up correctly

if [ ! -e $TOOLBOX_PATH/bart ] ;
then
	echo "\${TOOLBOX_PATH} is not set correctly!" >&2
	exit 1
fi

export PATH=${TOOLBOX_PATH}:${PATH}


# Estimate relative paths

FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})


# Download datasets for single-shot inversion recovery
# following https://github.com/mrirecon/sms-t1-mapping

if [[ ! -f "phantom/pha-ss.cfl" ]];
then
        wget https://zenodo.org/record/3969809/files/phantom-ss.tgz
        tar -xzvf phantom-ss.tgz
        rm phantom-ss.tgz
fi

bart copy phantom/pha-ss ksp


echo "Generated output file: ksp.{cfl,hdr}" >&2
