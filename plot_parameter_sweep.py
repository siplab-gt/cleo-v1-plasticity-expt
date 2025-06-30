import os
import sys
import time

import brian2.only as b2
import cleo
import cleo.utilities
import matplotlib.cm as cmaps
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec, rcParams
from scipy import stats

import analyse_experiment
from firing_rate_sd_to_hz import fr_sd_to_hz

SAVEPATH = "results"
FIGSIZE = (1.7, 2.7)


def plot_ctrl_vs_baseline(ax, base_mean, base_sd, ctrl_means, ctrl_sds, ctrl_targets):
    ax.plot(ctrl_targets, ctrl_means, c="#8000b4", label="opto feedback control")
    ax.fill_between(
        ctrl_targets,
        ctrl_means - 2 * ctrl_sds,
        ctrl_means + 2 * ctrl_sds,
        color="#8000b4",
        alpha=0.2,
    )
    ax.axhline(
        base_mean, linestyle="-", color="k", label="no-opto baseline"
    )
    ax.fill_between(
        ctrl_targets,
        base_mean - 2 * base_sd,
        base_mean + 2 * base_sd,
        color="k",
        alpha=0.2,
    )



def plot_weights(baseline_data, ctrl_datas):
    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=FIGSIZE)

    def plot_weight_panel(conn_type, ax):
        means = np.array([ctrl_data[f"{conn_type}_mean"] for ctrl_data in ctrl_datas])
        sds = np.array([ctrl_data[f"{conn_type}_sd"] for ctrl_data in ctrl_datas])
        fr_targets = np.array(
            [ctrl_data["target_firing_rate"] for ctrl_data in ctrl_datas]
        )

        plot_ctrl_vs_baseline(ax, baseline_data[f"{conn_type}_mean"], baseline_data[f"{conn_type}_sd"], means, sds, fr_targets)

    plot_weight_panel("pc_pc", ax1)
    plot_weight_panel("sst_pv", ax2)

    ax1.set(ylabel="PC-PC weights (nS)")
    ax2.set(xlabel="Target multi-unit\nfiring rate (Hz)", ylabel="SST-PV weights (nS)")
    fig.savefig(f"{SAVEPATH}/weights.png", transparent=False)
    fig.savefig(f"{SAVEPATH}/weights.svg")


def plot_firing(baseline_data, ctrl_datas):
    fig, ax = plt.subplots(figsize=FIGSIZE)

    fr_means = np.array([ctrl_data["fr_mean"] for ctrl_data in ctrl_datas])
    fr_sds = np.array([ctrl_data["fr_sd"] for ctrl_data in ctrl_datas])
    fr_targets = np.array(
        [ctrl_data["target_firing_rate"] for ctrl_data in ctrl_datas]
    )

    plot_ctrl_vs_baseline(
        ax,
        baseline_data["fr_mean"],
        baseline_data["fr_sd"],
        fr_means,
        fr_sds,
        fr_targets,
    )
    ax.plot(fr_targets, fr_targets, linestyle=":", color="gray", label="achieved = target")

    ax.set_xlabel("Target multi-unit\nfiring rate (Hz)")
    ax.set_ylabel("Achieved multi-unit firing rate (Hz)")
    ax.legend()
    fig.savefig(f"{SAVEPATH}/firing.png", transparent=False)
    fig.savefig(f"{SAVEPATH}/firing.svg")


def plot_trajectories(baseline_data, ctrl_datas):
    all_datas = [baseline_data] + ctrl_datas
    n_cols = len(all_datas)
    fig, axs = plt.subplots(
        2, n_cols, figsize=(n_cols * 1.3, 4), sharex=True, sharey="row"
    )
    for i, data in enumerate(all_datas):
        axs[0, i].plot(
            data["spike_times_s"],
            data["firing_rates"],
        )
        axs[1, i].plot(
            data["spike_times_s"],
            data["opto_values"],
            color="xkcd:sky blue",
        )
        axs[0, i].set(title=data["target_firing_rate"])
        axs[1, i].set(xlabel="time (s)")
    axs[0, 0].set(ylabel="firing rate (Hz)")
    axs[1, 0].set(ylabel="opto intensity (mW/mm²)")
    fig.savefig(f"{SAVEPATH}/trajectories.svg")
    fig.savefig(f"{SAVEPATH}/trajectories.png", transparent=False)


if __name__ == "__main__":
    cleo.utilities.style_plots_for_paper()

    firing_rates_sd = sys.argv[1]
    frs_sd = firing_rates_sd.split(",")
    ctrl_folders = [f"results/Spiking_model_PIcontrol_PV_rt_tSD_{fr}" for fr in frs_sd]
    baseline_folder = "results/Spiking_model_baseline"

    baseline_data = np.load(os.path.join(baseline_folder, "minimal_data.npz"))
    ctrl_datas = [
        np.load(os.path.join(ctrl_folder, "minimal_data.npz"))
        for ctrl_folder in ctrl_folders
    ]

    plot_weights(baseline_data, ctrl_datas)
    plot_firing(baseline_data, ctrl_datas)
    plot_trajectories(baseline_data, ctrl_datas)
