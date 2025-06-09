import multiprocessing

from sacred.observers import FileStorageObserver


def run_in_thread(firing_rate):
    from plot_essentials import plot_essentials
    from plot_Spikingmodel_stripped import plot_spiking_model
    from Spiking_model_cleo import ex

    print("Running with target firing rate:", firing_rate)
    if firing_rate != -1:
        dataname = f"Spiking_model_PIcontrol_PV_rt_tHz_{firing_rate}"
    else:
        dataname = "Spiking_model"

    ex.observers = [FileStorageObserver.create(dataname)]
    ex.run("run_network", config_updates={"target_firing_rate": firing_rate})
    plot_spiking_model(dataname)
    plot_essentials(dataname)


firing_rates = [
    -1,  # --> no optogenetic stimulation
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

if __name__ == '__main__':
    pool = multiprocessing.Pool(n_threads)
    pool.map(run_in_thread, firing_rates)
