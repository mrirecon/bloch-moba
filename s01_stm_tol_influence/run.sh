#!/bin/bash

set -e

export BART_COMPAT_VERSION=v0.9.00

# Run reconstructions

[ ! -d results/LL ] && ./run_reco.sh LL ""
[ ! -d results/M0A ] && ./run_reco.sh M0A ""



TOL=(1E-6 1E-3 5E-3 7E-3 1E-2)

for i in "${TOL[@]}"
do
	[ ! -d results/Bloch$i ] &&  ./run_reco.sh Bloch $i

	[ ! -d results/Bloch_SP$i ] &&  ./run_reco.sh Bloch_SP $i
done

[ -f tol.txt ] && rm tol.txt
touch tol.txt

echo "${TOL[@]}" >> tol.txt

bart join 8 $(for i in "${TOL[@]}"; do echo "results/Bloch$i/t1map"; done) results/joined_t1
bart join 8 $(for i in "${TOL[@]}"; do echo "results/Bloch_SP$i/t1map"; done) results/joined_t1_SP
bart join 8 $(ls vertices/v*.cfl | sed -e 's/\.cfl//') results/rois


# Improve testing
## Remove backgroudn to avoid strong noise influence

bart fmac results/M0A/t1map results/rois results/M0A/t1_test

for i in "${TOL[@]}";
do
	echo "$i"

	bart fmac results/Bloch$i/t1map results/rois results/Bloch$i/t1_test

	bart fmac results/Bloch_SP$i/t1map results/rois results/Bloch_SP$i/t1_test
done