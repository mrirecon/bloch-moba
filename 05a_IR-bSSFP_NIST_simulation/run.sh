#!/bin/bash

set -eux

export BART_COMPAT_VERSION=v0.9.00

./run_reco.sh SP_PI

./run_reco.sh NSP_PI

./run_reco.sh SP_NPI

# ./run_reco.sh NSP_NPI

bart join 7 results/{NSP_PI,SP_PI,SP_NPI}/t1map results/t1_join
bart join 7 results/{NSP_PI,SP_PI,SP_NPI}/t2map results/t2_join


# Improve testing

# Extract ROIs
bart fmac results/{t1_join,rois,_t1_test}
bart fmac results/{t2_join,rois,_t2_test}

# Water background not relevant here
bart extract 6 1 15 results/{_,}t1_test
bart extract 6 1 15 results/{_,}t2_test

# Seperate T1 maps
bart slice 7 0 results/t1_test{,1}
bart slice 7 1 results/t1_test{,2}
bart slice 7 2 results/t1_test{,3}

# Seperate T2 maps
bart slice 7 0 results/t2_test{,1}
bart slice 7 1 results/t2_test{,2}
bart slice 7 2 results/t2_test{,3}

rm results/_t{1,2}_test.{cfl,hdr}
