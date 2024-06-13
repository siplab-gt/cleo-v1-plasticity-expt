import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib import rcParams
from scipy import stats
import matplotlib.cm as cmaps
from analyse_experiment import *
import numpy as np


def findendweights(data):
    est = np.mean(np.squeeze(data[:]))
    sd = np.std(np.squeeze(data[:]))
    return est,sd

if __name__ == "__main__":
    dataname=[]
    reader=[]
    results=[]
    SOMPV_w_list=[]
    all_datas=[]
    PYR0toothers_list=[]
    #fig, ((ax1),(ax2), (ax3))=plt.subplots(3,1)
    #fig, ((ax1),(ax2))=plt.subplots(2,1)
    fig, ((ax1),(ax2))=plt.subplots(2,1)
    for i in range(8):
        dataname.append('Spiking_model_PIcontrol_PV_rt_tHz_{}_updated'.format(525+i*25))
        reader.append(ExperimentReader('./%s'%dataname[i]))
        savepath = './'
        all_datas.append(reader[i].try_loading_artifacts('1'))
        results.append(all_datas[i]['results.pkl'])
        current_result=all_datas[i]['results.pkl']
        #SOMPV_w_list.append(results[i]['SOMPV_w'][:])
        SOMPV_w=(current_result['SOMPV_w'][:])
        #PYR0toothers_list.append(results[i]['PYR0toothers'][:])
        firing_rates=current_result['firing_rates'][:]  
        firing_rate_mean=np.mean(np.squeeze(firing_rates[43400:67900]))
        firing_rate_std=np.std(np.squeeze(firing_rates[43400:67900]))
        est1, sd1,=findendweights((current_result['PYR0toothers'][:,-1])/nS)
        ax1.errorbar(i*25+525,est1,yerr=sd1,marker='*', capsize=10,color=cmaps.viridis(0))
        est2,sd2=findendweights(SOMPV_w[:3600,-1]/nS)
        #ax2_2.errorbar(i*25+525,firing_rate_mean,yerr=firing_rate_std, marker='*', capsize=10,color=cmaps.viridis(0))
        ax2.errorbar(i*25+525,est2,yerr=sd2,marker='*', capsize=10,color=cmaps.viridis(0))
        #ax1.plot(i*25+525,est1,color='g',marker='x')
        #ax2.plot(i*25+525,est2,color='g',marker='x')
        opto_intensity=current_result['opto_values'][:]
        opto_intensity_sum=0
        for t_index in range(len(opto_intensity)):
            opto_intensity_sum=opto_intensity_sum+opto_intensity[t_index]
        opto_intensity_sum=opto_intensity_sum/1000
        #ax3.plot(i*25+525,opto_intensity_sum,marker='*',color='b')
        
        #ax3.errorbar(firing_rate_mean, opto_intensity_sum, xerr=firing_rate_std,marker='*', capsize=10,color=cmaps.viridis(0))
    #Add plotting of results with no opto stimulation    
    dataname_no_opto='Spiking_model_updated_cleo_test'
    reader_no_opto=ExperimentReader('./%s'%dataname_no_opto)
    data_no_opto=reader_no_opto.try_loading_artifacts('1')
    result_no_opto=data_no_opto['results.pkl']
    SOMPV_w=(result_no_opto['SOMPV_w'][:])
    est1, sd1,=findendweights((result_no_opto['PYR0toothers'][:,-1])/nS)
    #ax1.errorbar(500,est1,sd1,marker='*', capsize=10,color='k')
    est2,sd2=findendweights(SOMPV_w[:3600,-1]/nS)
    #ax2.errorbar(500,est2,sd2,marker='*', capsize=10,color='k')
    #ax3.plot(500,0,marker='*',color='k')


    dataname_open_loop='Spiking_model_open_loop_PV_pt75'
    reader_open_loop=ExperimentReader('./%s'%dataname_open_loop)
    data_open_loop=reader_open_loop.try_loading_artifacts('1')
    result_open_loop=data_open_loop['results.pkl']
    
    firing_rates_open_loop=result_open_loop['firing_rates'][:]
    est1openloop, sd1openloop=findendweights((result_open_loop['PYR0toothers'][:,-1])/nS)
    SOMPV_w_open_loop=(result_open_loop['SOMPV_w'][:])
    est2openloop,sd2openloop=findendweights(SOMPV_w_open_loop[:3600,-1]/nS)
    opto_intensity_sum=.75*(67900-43400)/1000
    firing_rate_mean_open_loop=np.mean(np.squeeze(firing_rates_open_loop[43400:67900]))
    firing_rate_std_open_loop=np.std(np.squeeze(firing_rates_open_loop[43400:67900]))


    spike_values=result_no_opto['spike_values'][:]
    firing_rates_opto_off=result_no_opto['firing_rates'][:]  
    firing_rate_mean_no_opto=np.mean(np.squeeze(firing_rates_opto_off[43400:67900]))
    firing_rate_std_no_opto=np.std(np.squeeze(firing_rates_opto_off[43400:67900]))
    #ax1_2.errorbar(575,est1,sd1,marker='*', capsize=10,color='y')
    #ax2_2.errorbar(575,est2,sd2,marker='*', capsize=10,color='y')
    ax1xmin, ax1xmax = ax1.get_xlim()
    ax2xmin, ax2xmax = ax2.get_xlim()
    ax1.plot([ax1xmin, ax1xmax],[est1, est1], linestyle='-',color='k')
    ax1.plot([ax1xmin, ax1xmax],[est1-sd1, est1-sd1], linestyle='--',color='k')
    ax1.plot([ax1xmin, ax1xmax],[est1+sd1, est1+sd1], linestyle='--',color='k')
    ax2.plot([ax2xmin, ax2xmax],[est2, est2], linestyle='-',color='k')
    ax2.plot([ax2xmin, ax2xmax],[est2-sd2, est2-sd2], linestyle='--',color='k')
    ax2.plot([ax2xmin, ax2xmax],[est2+sd2, est2+sd2], linestyle='--',color='k')

    ax1.set_xlim(ax1xmin,ax1xmax)
    ax2.set_xlim(ax2xmin,ax2xmax)
    ax1.set_xlabel('Target Firing Rate (Spikes/s)')
    ax1.set_ylabel('PC-to-PC Neural Weights (nS)')
    ax2.set_xlabel('Target Firing Rate (Detected Spikes/s)')
    ax2.set_ylabel('SST-to-PV Neural Weights (nS)')
    ax1.set_ylim(-.025,.3)
    ax2.set_ylim(-.025,1)
    #ax3.set_ylim(-1,30)
    fig.set_figheight(10)
    fig.set_figwidth(6)
    plt.savefig('%s/WCM_parametersweep_cleo_updated_v1.png'%(savepath), format='png', transparent=False)
    plt.savefig('%s/WCM_parametersweep_cleo_updated_v1.pdf'%(savepath), format='pdf', transparent=False)

    fig2, ((ax21))=plt.subplots(1,1)
    for i in range(8):
        dataname.append('Spiking_model_PIcontrol{}_PV_rt_tHz_{}'.format(23+i,525+i*25))
        reader.append(ExperimentReader('./%s'%dataname[i]))
        savepath = './'
        all_datas.append(reader[i].try_loading_artifacts('1'))
        results.append(all_datas[i]['results.pkl'])
        current_result=all_datas[i]['results.pkl']
        firing_rates=current_result['firing_rates'][:]  
        firing_rate_mean=np.mean(np.squeeze(firing_rates[43400:67900]))
        firing_rate_std=np.std(np.squeeze(firing_rates[43400:67900]))
        ax21.errorbar(i*25+525,firing_rate_mean,yerr=firing_rate_std,marker='*', capsize=10,color=cmaps.viridis(0))

    dataname_no_opto='Spiking_model_updated_cleo_test'
    reader_no_opto=ExperimentReader('./%s'%dataname_no_opto)
    data_no_opto=reader_no_opto.try_loading_artifacts('1')
    result_no_opto=data_no_opto['results.pkl']
    firing_rates=result_no_opto['firing_rates'][:]  
    firing_rate_mean=np.mean(np.squeeze(firing_rates[43400:67900]))
    firing_rate_std=np.std(np.squeeze(firing_rates[43400:67900]))

    ax21xmin, ax21xmax = ax21.get_xlim()
    ax21.plot([ax21xmin, ax21xmax],[firing_rate_mean, firing_rate_mean], linestyle='-',color='k')
    ax21.plot([ax21xmin, ax21xmax],[firing_rate_mean-firing_rate_std, firing_rate_mean-firing_rate_std], linestyle='--',color='k')
    ax21.plot([ax21xmin, ax21xmax],[firing_rate_mean+firing_rate_std, firing_rate_mean+firing_rate_std], linestyle='--',color='k')
    ax21ymin, ax21ymax = ax21.get_ylim()

    ax21.set_xlim(ax21xmin,ax21xmax)
    #ax21.set_ylim(min([ax21xmin, ax21ymin]),max(ax21xmax,ax21ymax))
    ax21.set_xlabel('Target Firing Rate (Spikes/s)')
    ax21.set_ylabel('Detected Firing Rate (Detected Spikes/s)')
    fig2.set_figheight((6)*(ax21ymax-ax21ymin)/(ax21xmax-ax21xmin))
    fig2.set_figwidth(6)
    plt.savefig('%s/WCM_parametersweep_cleo_updated_firing_rate_v1.png'%(savepath), format='png', transparent=False)
    plt.savefig('%s/WCM_parametersweep_cleo_updated_firing_rate_v1.pdf'%(savepath), format='pdf', transparent=False)
