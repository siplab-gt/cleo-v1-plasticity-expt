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
To replicate results in the paper:
1. Run the original Wilmes-Clopath model for comparison
    ```bash
    python run_code.py
    ```
2. Run the simulation for all target firing rates
    ```bash
    python run_cleo_sweep.py
    ```