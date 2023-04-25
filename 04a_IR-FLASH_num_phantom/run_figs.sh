#!/bin/bash

# Run reconstructions

./run.sh

# Create figure

./func/create_figure.py results/M0A/t1map results/Bloch/t1map results/rois results/figure_04a

# Comment for debugging:
# ./clean_up.sh