#!/bin/bash

./run.sh

# Visualize slice-profile simulation

# Main Figure
python3 plot_simulation.py figure_03 slice.txt trtime.txt


# Supporting Material: in depth analysis
python3 plot_simulation_sup.py figure_s01 slice.txt trtime.txt

# Clean up
./clean_up.sh