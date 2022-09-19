#!/bin/bash

# Perform gold-standard T1-T2 mapping
./run.sh

# Visualize T1 and T2 maps and perform a ROI analysis
export DARK_LAYOUT=0
python3 analysis.py mapT1 mapT2 ref_values_nist $(ls vertices/*.cfl | sed -e 's/\.cfl//')
