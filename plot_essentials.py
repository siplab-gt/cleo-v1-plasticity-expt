import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib import rcParams
from scipy import stats
import matplotlib.cm as cmaps
from analyse_experiment import *
import numpy as np

if __name__ == "__main__":
    dataname = 'Spiking_model_updated_cleo_test'
    savepath = './'
    reader = ExperimentReader('./%s'%dataname)
    # load all runs at once
    runs = reader.get_all_experiment_runs()
    run_nos = np.arange(1,2).astype(str) # TD removed, BCM type PYR-VIP 
    no_stimuli = runs[run_nos[0]]['config']['params']['N4']
    N_pyr = runs[run_nos[0]]['config']['params']['NPYR']
    N_pop = 4
    N_sst = runs[run_nos[0]]['config']['params']['NSOM']
    N_pv = runs[run_nos[0]]['config']['params']['NPV']
    N_vip = runs[run_nos[0]]['config']['params']['NVIP']
    seed = runs[run_nos[0]]['config']['params']['seed']
    nonplasticwarmup = runs[run_nos[0]]['config']['params']['nonplasticwarmup_simtime']['py/reduce'][1]['py/tuple'][0]['values']
    plasticwarmup = runs[run_nos[0]]['config']['params']['warmup_simtime']['py/reduce'][1]['py/tuple'][0]['values']
    rewardsimtime = runs[run_nos[0]]['config']['params']['reward_simtime']['py/reduce'][1]['py/tuple'][0]['values']
    norewardsimtime = runs[run_nos[0]]['config']['params']['noreward_simtime']['py/reduce'][1]['py/tuple'][0]['values']
    noSSTPVsimtime = runs[run_nos[0]]['config']['params']['noSSTPV_simtime']['py/reduce'][1]['py/tuple'][0]['values']

    gmax = runs[run_nos[0]]['config']['params']['gmax']['py/reduce'][1]['py/tuple'][0]['values']*siemens

    input_time = runs[run_nos[0]]['config']['params']['input_time']['py/reduce'][1]['py/tuple'][0]['values']
    warmup = nonplasticwarmup + plasticwarmup
    total = warmup+rewardsimtime+norewardsimtime+nonplasticwarmup+noSSTPVsimtime

    t = np.arange(.0,135.3,.0001)*second
    


    
    dep_param = np.zeros(len(run_nos)) 
    dep_param2 = np.zeros(len(run_nos)) 
    performance = np.zeros(len(run_nos))
    performance_binary = np.zeros(len(run_nos))
    W_sst_pv = np.zeros((len(run_nos),N_sst*N_pv))
    W_pyr = np.zeros((len(run_nos),N_pyr*N_pyr))
    W_pyr_i = np.zeros((len(run_nos),N_pyr*N_pyr))
    W_pyr_j = np.zeros((len(run_nos),N_pyr*N_pyr))
    con_SOM_VIP_i = np.zeros((len(run_nos),N_sst*N_vip))
    con_SOM_VIP_j = np.zeros((len(run_nos),N_sst*N_vip))
    con_VIP_SOM_i = np.zeros((len(run_nos),N_vip*N_sst))
    con_VIP_SOM_j = np.zeros((len(run_nos),N_vip*N_sst))

    r_pyr = np.zeros((len(run_nos),N_pyr))

    rel_select_increase_mean = np.zeros((len(run_nos)))
    rel_select_increase = np.zeros((len(run_nos),N_pop))
    resp_increase = np.zeros((len(run_nos),N_pop))
    rel_resp_increase = np.zeros((len(run_nos),N_pop))
    response_rel_to_max = np.zeros((len(run_nos),N_pop))
    response_rel_to_max_before = np.zeros((len(run_nos),N_pop))
    response = np.zeros((len(run_nos),N_pop))
    increase = np.zeros((len(run_nos),N_pop))
    simple_resp_increase = np.zeros((len(run_nos),N_pop))
    SST0_PVmean = np.zeros((len(run_nos)))
    SSTother_PVmean = np.zeros((len(run_nos)))
    impact = np.zeros((len(run_nos)))
    impact_afterreward = np.zeros((len(run_nos)))
    impactmax = np.zeros((len(run_nos)))
    impactmax_afterreward = np.zeros((len(run_nos)))
    sst_pv = np.zeros((len(run_nos)))
    tuning = np.zeros((len(run_nos)))
    SOM0VIPprob = np.zeros((len(run_nos),int(N_sst/30)))
    VIPSOM0prob = np.zeros((len(run_nos),int(N_sst/30)))

    tuning_initial = np.zeros((len(run_nos),N_pop, N_pop))
    tuning_final = np.zeros((len(run_nos),N_pop, N_pop))
    SSTtuning_initial = np.zeros((len(run_nos),N_pop, N_pop))
    SSTtuning_final = np.zeros((len(run_nos),N_pop, N_pop))
    PVtuning_initial = np.zeros((len(run_nos),N_pop, N_pop))
    PVtuning_final = np.zeros((len(run_nos),N_pop, N_pop))
    VIPtuning_initial = np.zeros((len(run_nos),N_pop, N_pop))
    VIPtuning_final = np.zeros((len(run_nos),N_pop, N_pop))


    W_sst_pv_means = np.zeros((len(run_nos),N_pop))
    W_sst_pv_std = np.zeros((len(run_nos),N_pop))
    W_sst_pv_means_afterreward = np.zeros((N_pop))
    W_sst_pv_std_afterreward = np.zeros((N_pop))

    varied_param2 = 'tau_spikelet'
    varied_param = 'p_PV_PYR'

    
    #plt.register_cmap(name='viridis', cmap=cmaps.viridis)
    plt.set_cmap(cmaps.viridis)
    
    checker = None
    
    for i, run_no in enumerate(run_nos):
        all_data = reader.try_loading_artifacts(run_no)
        # get parameter
        config = runs[run_no]['config']

        dep_param[i] = runs[run_no]['config']['params'][varied_param]#['py/reduce'][1]['py/tuple'][0]['values']
        dep_param2[i] = runs[run_no]['config']['params'][varied_param2]['py/reduce'][1]['py/tuple'][0]['values']
        

        results = all_data['results.pkl']
    spike_values=results['spike_values'][:]

    fig, axrs1 = plt.subplots(1,1)
    
    delta=1
    time_constant=200
    alpha=1-2.72**(-delta/time_constant)
    firing_rates=[]
    firing_rate=0
    for i in range(len(spike_values)):
        firing_rate=0
        if i<time_constant:
            firing_rates.append(0)
        else:
            for j in range(int(time_constant/delta)):
                firing_rate=firing_rate+1000*alpha*(1-alpha)**j*spike_values[i-1-j]
            firing_rates.append(firing_rate)

    
    #spike_values[0]=0
    axrs1.plot(results['spike_times'][:],firing_rates,linewidth=.05)
    axrs1.set_xlabel('spike time')  

    #axrs1.set_xlim(0,max(results['spike_times'][:]))
    axrs1.set_ylabel('firing rate')
    #axrs1.set_ylim(0,max(results['spike_indices'][:]))
    plt.savefig('%s/%s/%s/recorded_firing_rate_recalculated_200ms.pdf'%(savepath,dataname,run_no), bbox_inches='tight',format='pdf', transparent=True) 

    fig, axrs2 = plt.subplots(1,1)
    
    delta=1
    time_constant=1000
    alpha=1-2.72**(-delta/time_constant)
    firing_rates=[]
    firing_rate=0
    for i in range(len(spike_values)):
        firing_rate=0
        if i<time_constant:
            firing_rates.append(0)
        else:
            for j in range(int(time_constant/delta)):
                firing_rate=firing_rate+1000*alpha*(1-alpha)**j*spike_values[i-1-j]
            firing_rates.append(firing_rate)

    
    #spike_values[0]=0
    axrs2.plot(results['spike_times'][:],firing_rates,linewidth=.05)
    axrs2.set_xlabel('spike time')  

    #axrs1.set_xlim(0,max(results['spike_times'][:]))
    axrs2.set_ylabel('firing rate')
    #axrs1.set_ylim(0,max(results['spike_indices'][:]))
    plt.savefig('%s/%s/%s/recorded_firing_rate_recalculated_1000ms.pdf'%(savepath,dataname,run_no), bbox_inches='tight',format='pdf', transparent=True) 

    fig, axrs3 = plt.subplots(1,1)
    
    delta=1
    time_constant=50
    alpha=1-2.72**(-delta/time_constant)
    firing_rates=[]
    firing_rate=0
    for i in range(len(spike_values)):
        firing_rate=0
        if i<time_constant:
            firing_rates.append(0)
        else:
            for j in range(int(time_constant/delta)):
                firing_rate=firing_rate+1000*alpha*(1-alpha)**j*spike_values[i-1-j]
            firing_rates.append(firing_rate)

    
    #spike_values[0]=0
    axrs3.plot(results['spike_times'][:],firing_rates,linewidth=.05)
    axrs3.set_xlabel('spike time')  

    #axrs1.set_xlim(0,max(results['spike_times'][:]))
    axrs3.set_ylabel('firing rate')
    #axrs1.set_ylim(0,max(results['spike_indices'][:]))
    plt.savefig('%s/%s/%s/recorded_firing_rate_recalculated_50ms.pdf'%(savepath,dataname,run_no), bbox_inches='tight',format='pdf', transparent=True)

    fig, axrs4 = plt.subplots(1,1)
    
    delta=1
    time_constant=10
    alpha=1-2.72**(-delta/time_constant)
    firing_rates=[]
    firing_rate=0
    for i in range(len(spike_values)):
        firing_rate=0
        if i<time_constant:
            firing_rates.append(0)
        else:
            for j in range(int(time_constant/delta)):
                firing_rate=firing_rate+1000*alpha*(1-alpha)**j*spike_values[i-1-j]
            firing_rates.append(firing_rate)

    
    #spike_values[0]=0
    axrs4.plot(results['spike_times'][:],firing_rates,linewidth=.05)
    axrs4.set_xlabel('spike time')  

    #axrs1.set_xlim(0,max(results['spike_times'][:]))
    axrs4.set_ylabel('firing rate')
    #axrs1.set_ylim(0,max(results['spike_indices'][:]))
    plt.savefig('%s/%s/%s/recorded_firing_rate_recalculated_10ms.pdf'%(savepath,dataname,run_no), bbox_inches='tight',format='pdf', transparent=True)  


