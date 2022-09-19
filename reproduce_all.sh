#!/bin/bash

set -euo pipefail
set -B

# Find figure folders (exclude meta and .git)
folders=($(find . -mindepth 1 -maxdepth 1 -type d -not \( -path "./meta" -o -path "./.git" \) -print | sort))

for f in "${folders[@]}";
do
	( cd $f; echo $f; ./run_figs.sh )
done