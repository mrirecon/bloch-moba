#!/bin/bash

set -euo pipefail
set -x

# Estimate relative paths

FULL_PATH=$(realpath ${0})
REL_PATH=$(dirname ${FULL_PATH})


# Save results

RESULTS=results/${1}

[ ! -d $RESULTS ] && mkdir -p $RESULTS

cp t1map.{cfl,hdr} $RESULTS || true
cp t2map.{cfl,hdr} $RESULTS || true


# Save additional information

OUTDIR="out/out_$1"

echo $OUTDIR

[ ! -d $OUTDIR ] && mkdir -p $OUTDIR

# Save additional files (not reqired for paper)
if true;
then
        ALL_FILES=${OUTDIR}/all
        
        [ ! -d $ALL_FILES ] && mkdir $ALL_FILES

        mv *.{cfl,hdr} $ALL_FILES || :
        mv *.log $ALL_FILES || :
fi
