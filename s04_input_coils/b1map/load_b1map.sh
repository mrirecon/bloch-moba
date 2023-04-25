#!/bin/bash

# B1+ Mapping with Siemens Sequence "tfl_b1map" based on
# Chung, S., Kim, D., Breton, E. and Axel, L. (2010),
# Rapid B1+ mapping using a preconditioning RF pulse with TurboFLASH readout.
# Magn. Reson. Med., 64: 439-446.
# https://doi.org/10.1002/mrm.22423

set -eux

# Estimate relative paths
FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})

KSP_B1MAP="$1"

# Load b1 raw data
bart copy "${KSP_B1MAP}" raw_asym

# Compensate for asymetric echo
## Mirror kspace to fill missing lines
FREQ_ASYM=$(bart show -d 0 raw_asym)
PHASE=$(bart show -d 1 raw_asym)
DIFF=$(($((PHASE*2))-FREQ_ASYM))

bart extract 0 $((FREQ_ASYM-DIFF)) $FREQ_ASYM raw_asym miss
bart flip $(bart bitmask 0) raw_asym tmp
bart join -a 0 tmp miss _raw
bart flip $(bart bitmask 0) _raw raw

rm {raw_asym,miss,tmp,_raw}.{cfl,hdr}


# Estimate Coil sensitivities
bart ecalib -c 0 -m 1 raw sens

# Phase preserving PI reconstruction
bart pics -g -e -S -d 5 raw sens _reco

SAMPLES=$(bart show -d 0 _reco)

bart resize -c 0 $PHASE _reco reco

rm {raw,sens,_reco}.{cfl,hdr}

bart slice 11 0 reco pd
bart slice 11 1 reco pre

rm reco.{cfl,hdr}

# Calculate: SSPre / PD
bart invert pd pdi
bart fmac pre pdi tmp

# Calculate: arccos(SSPre / PD)
python3 ${REL_PATH}/arccos.py tmp acos

FA_NOM=80 # [deg] Just from raw data..., IDEA internal... -> vim *.dat and /PrepFlipAngle

# Calculate: kappa = arccos(SSPre / PD) / FA_NOM = b1map
bart scale -- $(echo $FA_NOM | awk '{printf "%f\n", 1/(3.141592653589793 * $1 / 180)}') acos _b1map

rm {pd,pdi,pre,tmp,acos}.{cfl,hdr}


# Resize for input in moba
bart resize -c 0 $SAMPLES 1 $SAMPLES _b1map __b1map
bart transpose 0 1 __b1map b1map

rm _{,_}b1map.{cfl,hdr}
