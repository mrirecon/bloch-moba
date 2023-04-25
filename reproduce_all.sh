#!/bin/bash

set -euo pipefail
set -B

# Find figure folders
folders=($(find . -mindepth 2 -maxdepth 2 -type f -name run_figs.sh -exec dirname {} \+ | sort))

for f in "${folders[@]}";
do
	(
		cd  "$f"
		echo "$f"
		./run_figs.sh
	)
done
