# Quantitative Magnetic Resonance Imaging by Nonlinear Inversion of the Bloch Equations

This repository includes the scripts to create the Figures for the study

	Quantitative Magnetic Resonance Imaging by Nonlinear Inversion of the Bloch Equations

by Nick Scholand, Xiaoqing Wang, Volkert Roeloffs, Sebastian Rosenzweig, and Martin Uecker.

## Requirements
This repository has been tested on Debian 11, but is assumed to work on other Linux-based operating systems, too.

### Reconstruction
Pre-processing, reconstruction and post-processing is perfomed with the [BART toolbox](https://github.com/mrirecon/bart). The provided scripts are compatible with commit `e641e74` or later. If you experience any compatibility problems with later BART versions please contact us!

[//]: <> (FIXME: Add DOI for BART version including the Bloch model-based reconstruction)

For running the reconstructions access to a GPU is recommended. If the CPU should be used, please remove `-g` flags from `bart moba ...` and `bart pics ...` calls.

### Visualization
The visualisations are testet with Python version 3.9.2 and require numpy, copy, matplotlib, mpl_toolkits, sys, os, math, time, and scipy. Figure 6 requires [Latex](https://matplotlib.org/stable/tutorials/text/usetex.html) to be installed.
Ensure to have a your DISPLAY variable set, when the results should be visualized.

## Data
The data for the reconstructions is automatically downloaded from [Zenodo](https://zenodo.org/record/6992763). Please ensure internet access, when running the scripts.

## Folders
The folder names represent their corresponding figure numbers in the manuscript.
Folder `00_...` only reproduces the gold-standard mapping reference results used in figure 05b.
The reference figures from the manuscript can be found under `<folder>/results/`.

Each folder contains a README file explaining how the figure can be reproduced.

If you want to reproduce **all** figures, run

	bash reproduce_all.sh

## Feedback
Please feel free to send us feedback about this scripts!
We would be happy to learn how to improve this and future script publications.