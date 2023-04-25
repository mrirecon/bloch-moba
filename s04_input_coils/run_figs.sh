#!/bin/bash

set -eux

# Run reconstructions
./run.sh

# Create figure
./func/create_figure.py results/Bloch_cr/t{1,2}map results/Bloch_c/t{1,2}map results/figure_s04

# ./clean_up.sh
