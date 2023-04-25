#!/bin/bash

set -eux

./run.sh

# Final paper figure
./func/create_figure.py ref_nist.txt results/{t1_join,t2_join,rois,figure_05a}

./func/create_figure2.py ref_nist.txt results/{t1_join,t2_join,rois,figure_05a_bland}

# No data points are removed for better visualization
./func/create_figure_all.py ref_nist.txt results/{t1_join,t2_join,rois,figure_05a_bland_all}


# Comment for debugging:
# ./clean_up.sh