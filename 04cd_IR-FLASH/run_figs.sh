#!/bin/bash

# Run reconstructions

./run.sh


# Create figure

# Without slice-profile model

./func/create_figure.py results/M0A/t1map results/Bloch/t1map results/figure_04c  $(ls vertices/*.cfl | sed -e 's/\.cfl//')

./func/create_figure_allmaps.py results/Bloch/{t1,m0,b1}map results/Bloch/sensc results/figure_04d

# ./func/create_figure_allmaps_horiz.py results/Bloch/{t1,m0,b1}map results/Bloch/sensc results/figure_04d_horiz


# With slice-profile model

# ./func/create_figure.py results/M0A/t1map results/Bloch_SP/t1map results/figure_04c_SP  $(ls vertices/*.cfl | sed -e 's/\.cfl//')

# ./func/create_figure_allmaps.py results/Bloch_SP/{t1,m0,b1}map results/Bloch_SP/sensc results/figure_04d_SP

# Comment for debugging:
# ./clean_up.sh