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


def findendweights(data):
    est = np.mean(np.squeeze(data[:]))
    sd = np.std(np.squeeze(data[:]))
    return est, sd


def plot_weights(baseline_reader, baseline_results, ctrl_readers_results):
    SOMPV_w_list = []
    PYR0toothers_list = []
    # fig, ((ax1),(ax2), (ax3))=plt.subplots(3,1)
    # fig, ((ax1),(ax2))=plt.subplots(2,1)
    fig, ((ax1), (ax2)) = plt.subplots(2, 1)
    for reader, results in ctrl_readers_results:
        # SOMPV_w_list.append(results[i]['SOMPV_w'][:])
        SOMPV_w = results["SOMPV_w"][:]
        # PYR0toothers_list.append(results[i]['PYR0toothers'][:])
        firing_rates = results["firing_rates"][:]
        firing_rate_mean = np.mean(np.squeeze(firing_rates[43400:67900]))
        firing_rate_std = np.std(np.squeeze(firing_rates[43400:67900]))
        config = reader.get_experiment_config(reader.get_latest_exp_id)
        firing_rate_target = config["target_firing_rate"]
        (
            est1,
            sd1,
        ) = findendweights((results["PYR0toothers"][:, -1]) / b2.nS)
        ax1.errorbar(
            firing_rate_target,
            est1,
            yerr=sd1,
            marker="*",
            capsize=10,
            color=cmaps.viridis(0),
        )
        est2, sd2 = findendweights(SOMPV_w[:3600, -1] / b2.nS)
        # ax2_2.errorbar(i*25+525,firing_rate_mean,yerr=firing_rate_std, marker='*', capsize=10,color=cmaps.viridis(0))
        ax2.errorbar(
            firing_rate_target,
            est2,
            yerr=sd2,
            marker="*",
            capsize=10,
            color=cmaps.viridis(0),
        )
        # ax1.plot(i*25+525,est1,color='g',marker='x')
        # ax2.plot(i*25+525,est2,color='g',marker='x')

    # Add plotting of results with no opto stimulation
    SOMPV_w = baseline_results["SOMPV_w"][:]
    (
        est1,
        sd1,
    ) = findendweights((baseline_results["PYR0toothers"][:, -1]) / b2.nS)
    # ax1.errorbar(500,est1,sd1,marker='*', capsize=10,color='k')
    est2, sd2 = findendweights(SOMPV_w[:3600, -1] / b2.nS)
    # ax2.errorbar(500,est2,sd2,marker='*', capsize=10,color='k')
    # ax3.plot(500,0,marker='*',color='k')

    # dataname_open_loop='Spiking_model_open_loop_PV_pt75'
    # reader_open_loop=ExperimentReader('./%s'%dataname_open_loop)
    # data_open_loop=reader_open_loop.try_loading_artifacts('1')
    # result_open_loop=data_open_loop['results.pkl']

    # firing_rates_open_loop=result_open_loop['firing_rates'][:]
    # est1openloop, sd1openloop=findendweights((result_open_loop['PYR0toothers'][:,-1])/nS)
    # SOMPV_w_open_loop=(result_open_loop['SOMPV_w'][:])
    # est2openloop,sd2openloop=findendweights(SOMPV_w_open_loop[:3600,-1]/nS)
    # opto_intensity_sum=.75*(67900-43400)/1000
    # firing_rate_mean_open_loop=np.mean(np.squeeze(firing_rates_open_loop[43400:67900]))
    # firing_rate_std_open_loop=np.std(np.squeeze(firing_rates_open_loop[43400:67900]))

    spike_values = baseline_results["spike_values"][:]
    firing_rates_opto_off = baseline_results["firing_rates"][:]
    firing_rate_mean_no_opto = np.mean(np.squeeze(firing_rates_opto_off[43400:67900]))
    firing_rate_std_no_opto = np.std(np.squeeze(firing_rates_opto_off[43400:67900]))
    # ax1_2.errorbar(575,est1,sd1,marker='*', capsize=10,color='y')
    # ax2_2.errorbar(575,est2,sd2,marker='*', capsize=10,color='y')
    ax1xmin, ax1xmax = ax1.get_xlim()
    ax2xmin, ax2xmax = ax2.get_xlim()
    ax1.plot([ax1xmin, ax1xmax], [est1, est1], linestyle="-", color="k")
    ax1.plot([ax1xmin, ax1xmax], [est1 - sd1, est1 - sd1], linestyle="--", color="k")
    ax1.plot([ax1xmin, ax1xmax], [est1 + sd1, est1 + sd1], linestyle="--", color="k")
    ax2.plot([ax2xmin, ax2xmax], [est2, est2], linestyle="-", color="k")
    ax2.plot([ax2xmin, ax2xmax], [est2 - sd2, est2 - sd2], linestyle="--", color="k")
    ax2.plot([ax2xmin, ax2xmax], [est2 + sd2, est2 + sd2], linestyle="--", color="k")

    ax1.set_xlim(ax1xmin, ax1xmax)
    ax2.set_xlim(ax2xmin, ax2xmax)
    ax1.set_xlabel("Target Firing Rate (Spikes/s)")
    ax1.set_ylabel("PC-to-PC Neural Weights (nS)")
    ax2.set_xlabel("Target Firing Rate (Detected Spikes/s)")
    ax2.set_ylabel("SST-to-PV Neural Weights (nS)")
    ax1.set_ylim(-0.025, 0.3)
    ax2.set_ylim(-0.025, 1)
    # ax3.set_ylim(-1,30)
    fig.set_figheight(2.5)
    fig.set_figwidth(1.7)
    fig.savefig(f"{SAVEPATH}/weights.png", transparent=False)
    fig.savefig(f"{SAVEPATH}/weights.svg")


def plot_firing(baseline_reader, baseline_results, ctrl_readers_results):
    fig, ax = plt.subplots(figsize=(1.7, 2.5))
    for reader, results in ctrl_readers_results:
        firing_rates = results["firing_rates"][:]
        firing_rate_mean = np.mean(np.squeeze(firing_rates[43400:67900]))
        firing_rate_std = np.std(np.squeeze(firing_rates[43400:67900]))
        target = reader.get_experiment_config(reader.get_latest_exp_id)[
            "target_firing_rate"
        ]
        ax.errorbar(
            target,
            firing_rate_mean,
            yerr=firing_rate_std,
            marker="*",
            capsize=10,
            color="black",
        )

    firing_rates = baseline_results["firing_rates"][:]
    firing_rate_mean = np.mean(np.squeeze(firing_rates[43400:67900]))
    firing_rate_std = np.std(np.squeeze(firing_rates[43400:67900]))

    ax.axhline(firing_rate_mean, linestyle="-", color="k")
    ax.axhline(firing_rate_mean - firing_rate_std, linestyle="--", color="k")
    ax.axhline(firing_rate_mean + firing_rate_std, linestyle="--", color="k")
    ax21ymin, ax21ymax = ax.get_ylim()

    ax.set_xlabel("Target firing rate (Hz)")
    ax.set_ylabel("Achieved multi-unit firing rate (Hz)")
    fig.savefig(f"{SAVEPATH}/firing.png", transparent=False)
    fig.savefig(f"{SAVEPATH}/firing.svg")


def plot_trajectories(baseline_reader, baseline_results, ctrl_readers_results):
    readers_results = [(baseline_reader, baseline_results)] + ctrl_readers_results
    n_cols = len(readers_results)
    fig, axs = plt.subplots(2, n_cols, figsize=(n_cols * 1.3, 4), sharex=True, sharey="row")
    for i, (reader, results) in enumerate(readers_results):
        config = reader.get_experiment_config(reader.get_latest_exp_id)
        target = config["target_firing_rate"]
        axs[0, i].plot(
            np.array(results["spike_times"]) / 1000,
            results["firing_rates"],
        )
        axs[1, i].plot(
            np.array(results["spike_times"]) / 1000,
            results["opto_values"],
            color="xkcd:sky blue",
        )
        axs[0, i].set(title=target)
        axs[1, i].set(xlabel="time (s)")
    axs[0, 0].set(ylabel="firing rate (Hz)")
    axs[1, 0].set(ylabel="opto intensity (mW/mm²)")
    fig.savefig(f"{SAVEPATH}/trajectories.svg")
    fig.savefig(f"{SAVEPATH}/trajectories.png", transparent=False)


def load_data(baseline_folder, ctrl_folders):
    ctrl_readers_results = []
    for ctrl_folder in ctrl_folders:
        reader = analyse_experiment.ExperimentReader(ctrl_folder)
        data = reader.try_loading_artifacts(reader.get_latest_exp_id)
        results = data["results.pkl"]
        ctrl_readers_results.append((reader, results))
        print(f"loaded {ctrl_folder}")

    baseline_reader = analyse_experiment.ExperimentReader(baseline_folder)
    data = baseline_reader.try_loading_artifacts(baseline_reader.get_latest_exp_id)
    baseline_results = data["results.pkl"]
    print(f"loaded {baseline_folder}")

    return baseline_reader, baseline_results, ctrl_readers_results


if __name__ == "__main__":
    cleo.utilities.style_plots_for_paper()

    firing_rates_sd = sys.argv[1]
    frs_sd = firing_rates_sd.split(",")
    ctrl_folders = [f"results/Spiking_model_PIcontrol_PV_rt_tSD_{fr}" for fr in frs_sd]
    baseline_folder = "results/Spiking_model_baseline"

    baseline_reader, baseline_results, ctrl_readers_results = load_data(
        baseline_folder, ctrl_folders
    )

    plot_weights(baseline_reader, baseline_results, ctrl_readers_results)
    plot_firing(baseline_reader, baseline_results, ctrl_readers_results)
    plot_trajectories(baseline_reader, baseline_results, ctrl_readers_results)
