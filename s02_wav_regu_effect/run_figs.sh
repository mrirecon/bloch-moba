#!/bin/bash

# Run reconstructions

./run.sh

# Create figure

# Create figure
./func/create_figure.py results/M0A_1/t1map results/joined_t1 results/figure_s02 results/order.txt

# Comment for debugging:
# ./clean_up.sh