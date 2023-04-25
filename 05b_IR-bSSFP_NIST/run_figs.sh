#!/bin/bash

set -eux

./run.sh

# Final paper figure
./func/create_figure.py ref_values_nist results/join_{t1,t2}map results/figure_05b $(ls vertices/*.cfl | sed -e 's/\.cfl//')

./func/create_figure2.py ref_values_nist results/join_{t1,t2}map results/figure_05b_bland $(ls vertices/*.cfl | sed -e 's/\.cfl//')

# No data points are removed for better visualization
./func/create_figure_all.py ref_values_nist results/join_{t1,t2}map results/figure_05b_bland_all $(ls vertices/*.cfl | sed -e 's/\.cfl//')

# Comment for debugging:
# ./clean_up.sh