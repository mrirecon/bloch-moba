#!/bin/bash

export BART_COMPAT_VERSION=v0.9.00

# Simulation

## Run slice-profile simulation
./slice_profile.sh

## Run speed simulation
./speed_comparison.sh

# For Testing
./txt2cfl.py slice.txt slice
