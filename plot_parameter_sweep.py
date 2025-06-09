import sys

import brian2.only as b2
import cleo
import cleo.utilities
import matplotlib.cm as cmaps
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import gridspec, rcParams
from scipy import stats

import analyse_experiment


def findendweights(data):
    est = np.mean(np.squeeze(data[:]))
    sd = np.std(np.squeeze(data[:]))
    return est, sd


def plot_weights():
    dataname = []
    readers = []
    results = []
    SOMPV_w_list = []
    all_datas = []
    PYR0toothers_list = []
    # fig, ((ax1),(ax2), (ax3))=plt.subplots(3,1)
    # fig, ((ax1),(ax2))=plt.subplots(2,1)
    fig, ((ax1), (ax2)) = plt.subplots(2, 1)
    opto_fig, opto_ax = plt.subplots()
    for i in range(8):
        dataname.append("Spiking_model_PIcontrol_PV_rt_tHz_{}".format(525 + i * 25))
        readers.append(analyse_experiment.ExperimentReader("./%s" % dataname[i]))
        savepath = "./"
        all_datas.append(readers[i].try_loading_artifacts(readers[i].get_latest_exp_id))
        results.append(all_datas[i]["results.pkl"])
        current_result = all_datas[i]["results.pkl"]
        # SOMPV_w_list.append(results[i]['SOMPV_w'][:])
        SOMPV_w = current_result["SOMPV_w"][:]
        # PYR0toothers_list.append(results[i]['PYR0toothers'][:])
        firing_rates = current_result["firing_rates"][:]
        firing_rate_mean = np.mean(np.squeeze(firing_rates[43400:67900]))
        firing_rate_std = np.std(np.squeeze(firing_rates[43400:67900]))
        (
            est1,
            sd1,
        ) = findendweights((current_result["PYR0toothers"][:, -1]) / b2.nS)
        ax1.errorbar(
            i * 25 + 525, est1, yerr=sd1, marker="*", capsize=10, color=cmaps.viridis(0)
        )
        est2, sd2 = findendweights(SOMPV_w[:3600, -1] / b2.nS)
        # ax2_2.errorbar(i*25+525,firing_rate_mean,yerr=firing_rate_std, marker='*', capsize=10,color=cmaps.viridis(0))
        ax2.errorbar(
            i * 25 + 525, est2, yerr=sd2, marker="*", capsize=10, color=cmaps.viridis(0)
        )
        # ax1.plot(i*25+525,est1,color='g',marker='x')
        # ax2.plot(i*25+525,est2,color='g',marker='x')
        opto_intensity = current_result["opto_values"]
        t_ms = current_result["spike_times"]
        opto_ax.plot(t_ms, opto_intensity, label=525 + i * 25)
        opto_ax.legend()
        # opto_intensity_sum=0
        # for t_index in range(len(opto_intensity)):
        #     opto_intensity_sum=opto_intensity_sum+opto_intensity[t_index]
        # opto_intensity_sum=opto_intensity_sum/1000
        # ax3.plot(i*25+525,opto_intensity_sum,marker='*',color='b')

        # ax3.errorbar(firing_rate_mean, opto_intensity_sum, xerr=firing_rate_std,marker='*', capsize=10,color=cmaps.viridis(0))
    opto_fig.savefig(f"{savepath}/opto_intensity_vs_time.png")
    # Add plotting of results with no opto stimulation
    dataname_no_opto = "Spiking_model"
    reader_no_opto = analyse_experiment.ExperimentReader("./%s" % dataname_no_opto)
    data_no_opto = reader_no_opto.try_loading_artifacts(
        reader_no_opto.get_latest_exp_id
    )
    result_no_opto = data_no_opto["results.pkl"]
    SOMPV_w = result_no_opto["SOMPV_w"][:]
    (
        est1,
        sd1,
    ) = findendweights((result_no_opto["PYR0toothers"][:, -1]) / b2.nS)
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

    spike_values = result_no_opto["spike_values"][:]
    firing_rates_opto_off = result_no_opto["firing_rates"][:]
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
    fig.savefig("%s/WCM_parametersweep_cleo.png" % (savepath))
    fig.savefig("%s/WCM_parametersweep_cleo.svg" % (savepath))


def plot_firing():
    fig2, ax = plt.subplots(figsize=(1.7, 2.5))
    for i in range(8):
        dataname = f"./Spiking_model_PIcontrol_PV_rt_tHz_{525 + i * 25}"
        reader = analyse_experiment.ExperimentReader(dataname)
        all_data = reader.try_loading_artifacts(reader.get_latest_exp_id)
        current_result = all_data["results.pkl"]
        firing_rates = current_result["firing_rates"][:]
        firing_rate_mean = np.mean(np.squeeze(firing_rates[43400:67900]))
        firing_rate_std = np.std(np.squeeze(firing_rates[43400:67900]))
        ax.errorbar(
            i * 25 + 525,
            firing_rate_mean,
            yerr=firing_rate_std,
            marker="*",
            capsize=10,
            color="black",
        )

    dataname_no_opto = "Spiking_model"
    reader_no_opto = analyse_experiment.ExperimentReader("./%s" % dataname_no_opto)
    data_no_opto = reader_no_opto.try_loading_artifacts(
        reader_no_opto.get_latest_exp_id
    )
    result_no_opto = data_no_opto["results.pkl"]
    firing_rates = result_no_opto["firing_rates"][:]
    firing_rate_mean = np.mean(np.squeeze(firing_rates[43400:67900]))
    firing_rate_std = np.std(np.squeeze(firing_rates[43400:67900]))

    ax.axhline(firing_rate_mean, linestyle="-", color="k")
    ax.axhline(firing_rate_mean - firing_rate_std, linestyle="--", color="k")
    ax.axhline(firing_rate_mean + firing_rate_std, linestyle="--", color="k")
    ax21ymin, ax21ymax = ax.get_ylim()

    ax.set_xlabel("Target firing rate (Hz)")
    ax.set_ylabel("Achieved multi-unit firing rate (Hz)")
    plt.savefig("WCM_firing.pdf")
    plt.savefig("WCM_firing.svg")


def plot_trajectories():
    datanames = ["Spiking_model"] + [
        f"./Spiking_model_PIcontrol_PV_rt_tHz_{525 + i * 25}" for i in range(8)
    ]
    targets = [-1] + [525 + i * 25 for i in range(8)]
    fig, axs = plt.subplots(2, 9, figsize=(10, 4), sharex=True, sharey='row')
    for i, dataname in enumerate(datanames):
        reader = analyse_experiment.ExperimentReader(dataname)
        all_data = reader.try_loading_artifacts(reader.get_latest_exp_id)
        current_result = all_data["results.pkl"]
        axs[0, i].plot(
            np.array(current_result["spike_times"]) / 1000,
            current_result["firing_rates"],
        )
        axs[1, i].plot(
            np.array(current_result["spike_times"]) / 1000,
            current_result["opto_values"],
            color='xkcd:sky blue'
        )
        axs[0, i].set(title=targets[i])
        axs[1, i].set(xlabel='time (s)')
    axs[0, 0].set(ylabel='firing rate (Hz)')
    axs[1, 0].set(ylabel='opto intensity (mW/mm²)')
    fig.savefig("WCM_trajectories.pdf")
    fig.savefig("WCM_trajectories.png", transparent=False)

if __name__ == "__main__":
    cleo.utilities.style_plots_for_paper()

    # plot_weights()
    # plot_firing()
    plot_trajectories()
