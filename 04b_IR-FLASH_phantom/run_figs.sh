#!/bin/bash

# Run reconstructions

./run.sh

# Create figure

./func/create_figure.py results/M0A/t1map results/Bloch/t1map  results/figure_04b  $(ls vertices/*.cfl | sed -e 's/\.cfl//')

# ./func/create_figure2ref.py ref_values results/Bloch/t1map  results/figure_not_used  $(ls vertices/*.cfl | sed -e 's/\.cfl//')

# Comment for debugging:
# ./clean_up.sh