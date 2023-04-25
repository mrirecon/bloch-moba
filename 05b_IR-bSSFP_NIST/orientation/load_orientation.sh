#!/bin/bash

set -eux

# Find correct B1 and B0 map orientation
# Stack all radial spokes of inversion curve into single slice and reconstruct them

# Estimate relative paths
FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})

# Load data
bash ${REL_PATH}/../data/load_data.sh

SAMPLES=$(bart show -d 0 ksp)
SPOKES=$(bart show -d 1 ksp)
COILS=$(bart show -d 3 ksp)
FRAMES=$(bart show -d 10 ksp)

bart transpose 1 3 ksp{,1}
bart reshape $(bart bitmask 3 10) $((FRAMES*SPOKES)) 1 ksp{1,2}
bart transpose 1 3 ksp2 raw
rm ksp{,1,2}.{cfl,hdr}

bart transpose 1 2 raw tmp
bart transpose 0 1 tmp raw2
rm {raw,tmp}.{cfl,hdr}

# Estimate Coil sensitivities
bart traj -x $SAMPLES -R 27 -y $((FRAMES*SPOKES)) -s7 -G -D -r _traj
bart scale -- 0.5 _traj traj
rm _traj.{cfl,hdr}

# Phase preserving PI reconstruction
bart nufft -g -i traj raw2 _pro

# Grid non-Cartesian data to Cartesian grid
bart fft $(bart bitmask 0 1 2) _pro ksp
rm _pro.{cfl,hdr}

# Estimate Coil sensitivities
bart ecalib -c 0 -m 1 ksp sens
rm ksp.{cfl,hdr}

# Phase preserving PI reconstruction
bart pics -g -e -S -d 5 -l1 -r0.001 -t traj raw2 sens ref

rm {traj,raw2,sens}.{cfl,hdr}
