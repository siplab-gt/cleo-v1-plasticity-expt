# cleo-v1-plasticity-expt

Code for the V1 plasticity disruption experiment (prospective experiment 2) in the [Cleo publication](https://www.biorxiv.org/content/10.1101/2023.01.27.525963).
Original [model](https://modeldb.science/259546) from [Wilmes and Clopath 2019](https://doi.org/10.1038/s41467-019-12972-2).
Adapted here by [Nathan Cruzado](https://www.linkedin.com/in/nathanael-cruzado-5a7541199/) to add closed-loop optogenetic control with [Cleo](https://cleosim.rtfd.io/).

*Research was conducted in the [SIPLab](https://siplab.gatech.edu), led by Chris Rozell and Sankar Alagapan at Georgia Tech.*

## Setup
Install the conda environment:
```bash
mamba env create -f environment.yml
mamba activate wcm
```

*(wcm refers to Wilmes-Clopath Model)*

## Usage
To replicate results in the paper, simply run [Task](https://taskfile.dev):

```
task
```

While Task will orchestrate needed runs to form plots, it unfortunately does not detect when a *repeated* task needs to be rerun when they share a source (in this case the source code `Spiking_model_cleo.py`).
So if you change that file and need to rerun everything, you'll need to delete the previous results for Task to handle it intelligently.
[Snakemake](https://snakemake.github.io/) would be the better choice in the future.

*This code has not been thoroughly tested, so please report any issues you encounter.*