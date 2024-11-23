#!/bin/bash

set -e

export BART_COMPAT_VERSION=v0.9.00

# Run reconstructions

./run_reco.sh LL
./run_reco.sh M0A
./run_reco.sh Bloch
