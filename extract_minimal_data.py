import os
import sys

import brian2.only as b2
import numpy as np

import analyse_experiment


def findendweights(data):
    est = np.mean(np.squeeze(data[:]))
    sd = np.std(np.squeeze(data[:]))
    return est, sd


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
    outdir = sys.argv[1]

    reader = analyse_experiment.ExperimentReader(outdir)
    data = reader.try_loading_artifacts(reader.get_latest_exp_id)
    results = data["results.pkl"]

    config = reader.get_experiment_config(reader.get_latest_exp_id)

    pc_pc_mean, pc_pc_sd = findendweights(results["PYR0toothers"][:, -1] / b2.nS)
    sst_pv_mean, sst_pv_sd = findendweights(results["SOMPV_w"][:][:3600, -1] / b2.nS)

    firing_rates = results["firing_rates"][:]
    fr_mean = np.mean(np.squeeze(firing_rates[43400:67900]))
    fr_sd = np.std(np.squeeze(firing_rates[43400:67900]))

    outfile = os.path.join(outdir, "minimal_data.npz")
    np.savez(
        outfile,
        target_firing_rate=config["target_firing_rate"],
        pc_pc_mean=pc_pc_mean,
        pc_pc_sd=pc_pc_sd,
        sst_pv_mean=sst_pv_mean,
        sst_pv_sd=sst_pv_sd,
        firing_rates=firing_rates,
        fr_mean=fr_mean,
        fr_sd=fr_sd,
        spike_times_s=np.array(results["spike_times"]) / 1000,
        opto_values=np.array(results["opto_values"]),
    )
    print(f'distilled results into {outfile}')
