#!/bin/bash

set -e

# Run reconstructions

./run_reco.sh LL
./run_reco.sh Bloch_flash
./run_reco.sh Bloch_short
./run_reco.sh Bloch_long


# Improve testing

# Join ROIs
bart join 6 $(ls vertices/*.cfl | sed -e 's/\.cfl//') results/rois

# Extract ROIs

bart fmac results/{LL/t1map,rois,LL/t1_test}

bart fmac results/{Bloch_flash/t1map,rois,Bloch_flash/t1_test}

bart fmac results/{Bloch_short/t1map,rois,Bloch_short/t1_test}
bart fmac results/{Bloch_short/t2map,rois,Bloch_short/t2_test}

bart fmac results/{Bloch_long/t1map,rois,Bloch_long/t1_test}
bart fmac results/{Bloch_long/t2map,rois,Bloch_long/t2_test}

rm results/rois.{cfl,hdr}