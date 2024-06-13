import multiprocessing
from sacred.observers import FileStorageObserver


def run_in_thread(firing_rate):
    from Spiking_model_cleo import ex

    # print("Running with firing rate:", firing_rate)
    # return
    ex.observers.append(
        FileStorageObserver.create(f"Spiking_model_PIcontrol_PV_rt_tHz_{firing_rate}")
    )
    ex.run("run_network", config_updates={'target_firing_rate': firing_rate})


firing_rates = [
    -1,
    525,
    550,
    575,
    600,
    625,
    650,
    675,
    700,
]
n_threads = len(firing_rates)
pool = multiprocessing.Pool(n_threads)
pool.map(run_in_thread, firing_rates)
