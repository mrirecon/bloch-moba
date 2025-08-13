**The main repository has moved to: https://gitlab.tugraz.at/ibi/mrirecon/papers/bloch-moba.git**

**Please check there for updates.**


# Quantitative Magnetic Resonance Imaging by Nonlinear Inversion of the Bloch Equations

This repository includes the scripts to create the Figures for the study

> #### Quantitative MRI by nonlinear inversion of the Bloch equations
> Scholand, N, Wang, X, Roeloffs, V, Rosenzweig, S, Uecker, M. Magn Reson Med. 2023; 1- 19.
> [doi: 10.1002/mrm.29664](https://doi.org/10.1002/mrm.29664)

## Requirements
This repository has been tested on Debian 11, but is assumed to work on other Linux-based operating systems, too.

### Reconstruction
Pre-processing, reconstruction and post-processing is performed with the [BART toolbox](https://github.com/mrirecon/bart).
The provided scripts are compatible with commit `0c847a2` or later.
If you experience any compatibility problems with later BART versions please contact us!

[//]: <> (FIXME: Add DOI for BART version including the Bloch model-based reconstruction)

For running the reconstructions access to a GPU is recommended.
If the CPU should be used, please remove `-g` flags from `bart moba ...`, `bart pics ...` and `bart rtnlinv ...` calls.

### Visualization
The visualizations have been tested with Python on version 3.9.2 and require numpy, copy, matplotlib, mpl_toolkits, sys, os, math, time, and scipy. Ensure to have a your DISPLAY variable set, when the results should be visualized.

## Data
The data is hosted on [ZENODO](https://zenodo.org/) and must be downloaded first.

* Manual download: https://zenodo.org/record/7654462
* Download via script: Run the download script in the `./data` folder.
  * **All** files: `bash load_all.sh`
  * **Individual** files: `bash load.sh 7654462 <FILENAME> . `

Note: The data must be stored in the `./data` folder!


## Folders
The folder names represent the corresponding figure numbers in the manuscript.
Folder `00_...` only reproduces the gold-standard mapping reference results used in figure 05b.
The reference figures from the manuscript can be found under `<folder>/results/`.

Each folder contains a README file explaining how the figure can be reproduced.

If you want to reproduce **all** figures, run

	bash reproduce_all.sh

[//]: <> (FIXME: Add Runtime!)

## Feedback
Please feel free to send us feedback about this scripts!
We would be happy to learn how to improve this and future script publications.


## License
This work is licensed under a **Creative Commons Attribution 4.0 International License**.
You should have received a copy of the license along with this
work. If not, see <https://creativecommons.org/licenses/by/4.0/>.
