import os
import sys

import brian2.only as b2
import cleo
import matplotlib.cm as cmaps
import matplotlib.pyplot as plt
import numpy as np

import analyse_experiment as ae
from Spiking_model_cleo import Struct


def tsplot(ax, data, **kw):
    x = np.arange(data.shape[1]) / 10  # convert to seconds
    est = np.mean(data, axis=0)
    sd = np.std(data, axis=0)
    cis = (est - 2 * sd, est + 2 * sd)
    ax.fill_between(x, cis[0], cis[1], alpha=0.2, **kw)
    ax.plot(x, est, **kw)
    ax.margins(x=0)


def plot_weights_over_time(no_opto_dataname, max_opto_dataname):
    no_opto_reader = ae.ExperimentReader(no_opto_dataname)
    max_opto_reader = ae.ExperimentReader(max_opto_dataname)

    config = no_opto_reader.get_experiment_config(no_opto_reader.get_latest_exp_id)
    p = Struct(**config["params"])
    max_opto_target_fr = max_opto_reader.get_experiment_config(
        max_opto_reader.get_latest_exp_id
    )["target_firing_rate"]

    nonplasticwarmup = p.nonplasticwarmup_simtime / b2.second
    plasticwarmup = p.warmup_simtime / b2.second
    rewardsimtime = p.reward_simtime / b2.second
    norewardsimtime = p.noreward_simtime / b2.second
    noSSTPVsimtime = p.noSSTPV_simtime / b2.second
    input_time = p.input_time / b2.second

    warmup = nonplasticwarmup + plasticwarmup
    total = warmup + rewardsimtime + norewardsimtime + nonplasticwarmup + noSSTPVsimtime

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(2.05, 1.3), layout="compressed", sharey=True)

    for ax, reader in [(ax1, no_opto_reader), (ax2, max_opto_reader)]:
        data = reader.try_loading_artifacts(reader.get_latest_exp_id)
        results = data["results.pkl"]

        PYR0toothers = results['PYR0toothers'][:]
        otherstoPYR0 = results['otherstoPYR0'][:]
        PYR1toothers = results['PYR1toothers'][:]
        try:
            PYR2toothers = results['PYR4toothers'][:]
        except KeyError:
            PYR2toothers = results['PYR2toothers'][:]
        PYR1and2toothers = np.concatenate((PYR1toothers,PYR2toothers))

        nS = b2.nS
        ax.axvspan(
            (nonplasticwarmup + plasticwarmup),
            (nonplasticwarmup + plasticwarmup + rewardsimtime),
            facecolor=".8",
            lw=0.0,
            alpha=0.5,
        )

        tsplot(
            ax, data=PYR1and2toothers[:, :] / nS, color=cmaps.viridis(1.0)
        )  # ,label='others to others')
        tsplot(
            ax, data=PYR0toothers[:, :] / nS, color=cmaps.viridis(0.0)
        )  # ,label ='1 to others')
        tsplot(
            ax, data=otherstoPYR0[:, :] / nS, color=cmaps.viridis(0.5)
        )  # ,label='others to 1')

        ax.set_xlabel("time (s)")

    ax1.set_ylabel("PC-PC weights (nS)")
    ax1.set_ylim(-0.01, None)
    ax1.set_title("no stim")
    ax2.set_title(f"{max_opto_target_fr} Hz clamp")

    fig.savefig("results/weights_over_time.png", transparent=False)
    fig.savefig("results/weights_over_time.svg")


if __name__ == "__main__":
    cleo.utilities.style_plots_for_paper()

    no_opto_dataname = sys.argv[1]
    max_opto_dataname = sys.argv[2]

    plot_weights_over_time(no_opto_dataname, max_opto_dataname)
