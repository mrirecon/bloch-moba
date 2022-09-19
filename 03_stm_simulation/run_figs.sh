#!/bin/bash

./run.sh

# Visualize slice-profile simulation

python3 plot_simulation.py figure_03 slice.txt trtime.txt

# Clean up
./clean_up.sh