#!/bin/bash

set -e

export BART_COMPAT_VERSION=v0.9.00

# Run reconstructions

./run_reco.sh LL

# Reference with coils
./run_reco.sh Bloch

# Input coils and no regularization
./run_reco.sh Bloch_c

# Input coils and regularization
./run_reco.sh Bloch_cr


# Improve testing

# Join ROIs
bart join 6 $(ls vertices/*.cfl | sed -e 's/\.cfl//') results/rois

# Extract ROIs

bart fmac results/{LL/t1map,rois,LL/t1_test}

bart fmac results/{Bloch/t1map,rois,Bloch/t1_test}
bart fmac results/{Bloch/t2map,rois,Bloch/t2_test}

bart fmac results/{Bloch_c/t1map,rois,Bloch_c/t1_test}
bart fmac results/{Bloch_c/t2map,rois,Bloch_c/t2_test}

bart fmac results/{Bloch_cr/t1map,rois,Bloch_cr/t1_test}
bart fmac results/{Bloch_cr/t2map,rois,Bloch_cr/t2_test}

rm results/rois.{cfl,hdr}
