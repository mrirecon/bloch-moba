#!/bin/bash

# Run reconstructions

./run.sh

# Create figures

./func/create_figure.py "A" "" tol results/rois results/joined_t1{,_SP} results/figure_s01_A

# Comment for debugging:
# ./clean_up.sh