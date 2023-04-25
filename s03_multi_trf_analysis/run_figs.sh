#!/bin/bash

set -eux

# Run reconstructions
./run.sh


# Create figure

[ -f trf.txt ] && rm trf.txt
touch trf.txt

echo {2_5,2_1,1_6,1_2,0_6,0_4} >> trf.txt

bart join 2 $(ls vertices/v*.cfl | sed -e 's/\.cfl//') vertices/rois

./func/create_figure.py trf vertices/rois results/figure_s03 results/Bloch_{2_5,2_1,1_6,1_2,0_6,0_4}/t1map

# ./clean_up.sh
