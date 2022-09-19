#!/bin/bash

set -eux

# Perfect Inversion Model

# without slice-profile model
./run_reco.sh BLOCH_ie func/opts_ie.sh

# with slice-profile model
./run_reco.sh BLOCH_ie_sp func/opts_ie_sp.sh


# HyperSec Inversion Model

# without slice-profile model
./run_reco.sh BLOCH func/opts.sh

# with slice-profile model
./run_reco.sh BLOCH_sp func/opts_sp.sh


# Concentrate data
bart join 7 results/BLOCH{,_sp,_ie,_ie_sp}/t1map results/join_t1map
bart join 7 results/BLOCH{,_sp,_ie,_ie_sp}/t2map results/join_t2map


# Improve testing

# Join ROIs
bart join 6 $(ls vertices/*.cfl | sed -e 's/\.cfl//') results/rois

# Extract ROIs
bart fmac results/{join_t1map,rois,t1_test}
bart fmac results/{join_t2map,rois,t2_test}

# Seperate T1 maps
bart slice 7 0 results/t1_test{,1}	# Hyp.Sec. inversion, single-spin
bart slice 7 1 results/t1_test{,2}	# Hyp.Sec. inversion, Slice Profile
bart slice 7 2 results/t1_test{,3}	# Perfect inversion, single-spin
bart slice 7 3 results/t1_test{,4}	# Perfect inversion, Slice Profile

# Seperate T2 maps
bart slice 7 0 results/t2_test{,1}
bart slice 7 1 results/t2_test{,2}
bart slice 7 2 results/t2_test{,3}
bart slice 7 3 results/t2_test{,4}

rm results/rois.{cfl,hdr}