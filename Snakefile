import os

FIRING_RATES_SD = [0, 0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2]
BASELINE_FILE = "results/base_mean_sd.txt"
EXTRA_OVERRIDES = "'params.timestep_ms_=2' 'codegen_target=numpy'"


# Baseline stats
# rule test:
#     input:
#         "dep1.done",
#         "dep2.done",
#     output:
#         "test.done",
#     shell:
#         'echo "Test rule executed" > {output}'


# rule test_dep:
#     input:
#         "dep_dep.done",
#     output:
#         "dep{i}.done",
#     shell:
#         'echo "Dependency {wildcards.i} done" > {output}'


# rule test_dep_dep:
#     input:
#         'dep_dep.input'
#     output:
#         'dep_dep.done'
#     shell:
#         'echo "Dependency dep done" > {output}'


def sd_to_hz_target(fr_sd):
    with open(BASELINE_FILE, "r") as f:
        lines = f.readlines()
        mean = float(lines[0].strip())
        sd = float(lines[1].strip())
    return mean + fr_sd * sd


rule all:
    input:
        "results/weights_vs_targets.svg",
        "results/control_trajectories.pdf",
        "results/firing.svg",


all_ctrl_results = {
    str(fr_sd): f"results/Spiking_model_PIcontrol_PV_rt_tSD_{fr_sd}/results.pkl"
    for fr_sd in FIRING_RATES_SD
} | {"baseline": "results/Spiking_model_baseline/results.pkl"}


rule plot_weights_vs_targets:
    input:
        BASELINE_FILE,
        **all_ctrl_results,
    output:
        "results/weights_vs_targets.svg",
    script:
        "scripts/plot_weights_vs_targets.py"


rule plot_firing_vs_targets:
    input:
        BASELINE_FILE,
        **all_ctrl_results,
    output:
        "results/firing.svg",
    script:
        "scripts/plot_firing.py"


rule plot_control_trajectories:
    input:
        BASELINE_FILE,
        **all_ctrl_results,
    output:
        "results/control_trajectories.pdf",
    script:
        "scripts/plot_control_trajectories.py"


rule ctrl_run:
    input:
        "Spiking_model_cleo.py",
        BASELINE_FILE,
    output:
        protected("results/Spiking_model_PIcontrol_PV_rt_tSD_{fr_sd}/results.pkl"),
    params:
        fr=lambda wc: sd_to_hz_target(wc.fr_sd),
        file_storage=lambda wildcards, output: os.path.dirname(output[0]),
        extra_overrides=EXTRA_OVERRIDES,
    shell:
        "python Spiking_model_cleo.py -F {params.file_storage} with 'target_firing_rate={params.fr}' {params.extra_overrides}"


rule run_baseline:
    input:
        "Spiking_model_cleo.py",
    output:
        protected("results/Spiking_model_baseline/results.pkl"),
    params:
        file_storage=lambda wildcards, output: os.path.dirname(output[0]),
        extra_overrides=EXTRA_OVERRIDES,
    shell:
        "python Spiking_model_cleo.py -F {params.file_storage} with 'target_firing_rate=-1' {params.extra_overrides}"


rule get_targets_from_baseline:
    input:
        "results/Spiking_model_baseline/results.pkl",
    output:
        BASELINE_FILE,
    run:
        import pickle
        import numpy as np

        with open(input[0], "rb") as f:
            result = pickle.load(f)
        firing_rates = result["firing_rates"][:]
        fr_arr = np.squeeze(firing_rates)
        mean = fr_arr.mean()
        sd = fr_arr.std()
        with open(output[0], "w") as f:
            f.write(f"{mean}\n{sd}\n")


rule run:
    input:
        base_mean="results/base_mean.txt",
        base_sd="results/base_sd.txt",
    output:
        outdir="Spiking_model_PIcontrol_PV_rt_tHz_{rate}/results.pkl",
    params:
        param_overrides=lambda wildcards: os.environ.get("PARAM_OVERRIDES", ""),
    shell:
        "python Spiking_model_cleo.py with 'target_firing_rate={wildcards.rate} {params.param_overrides}'"


# Optionally, you can add a rule for run_base if needed
# rule run_base:
#     output:
#         outdir="Spiking_model_PIcontrol_PV_rt_tHz_-1/results.pkl"
#     shell:
#         "python Spiking_model_cleo.py with 'target_firing_rate=-1 {params}'"
#     params:
#         lambda wildcards: os.environ.get("PARAM_OVERRIDES", "")
