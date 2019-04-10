import numpy as np
import os, sys, pickle
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc
from necessary_analysis_scripts import *

## plotting defaults
#plt.rcParams.update({'font.size': 14})
#rc('text', usetex=False)
plt.rcParams['pdf.fonttype'] = 42

font_file = "/Library/Fonts/HelveticaNeue-Light.ttf"
if os.path.isfile(font_file): prop = fm.FontProperties(fname=font_file,size=24)
else: prop = fm.FontProperties(size=24)
fig_dir = '../figures'

#color defaults
col_slow = (0/255.,98/255.,100/255.)
col_fast = (218/255.,66/255.,36/255.)


def calculate_mem_probetrials(subj_dat,shift):
    nsubj = len(subj_dat)

    nblocks = 4
    max_nfast_perblock = 20

    mem_fast = np.zeros((nsubj,nblocks*max_nfast_perblock))
    mem_fast[:] = np.nan
    mem_slow = np.zeros((nsubj,nblocks*max_nfast_perblock))
    mem_slow[:] = np.nan

    for isubj in range(nsubj):
        
        #rt for all trials for this subject
        wm_numcorr_alltrials = subj_dat[isubj].wholereport_respacc_total
    

        #calculate preRT for fast trials
        i_fast = np.ravel(subj_dat[isubj].fast_rt_trigger)==1        
        i_fast_ind = np.where(i_fast==True)[0]
        for i,i_probe_fast in enumerate(i_fast_ind):
            mem_fast[isubj][i] = np.nanmean(wm_numcorr_alltrials[i_probe_fast+shift])
            
        
        #calculate preRT for slow trials
        i_slow = np.ravel(subj_dat[isubj].slow_rt_trigger)==1
        i_slow_ind = np.where(i_slow==True)[0]
        for i,i_probe_slow in enumerate(i_slow_ind):
            mem_slow[isubj][i] = np.nanmean(wm_numcorr_alltrials[i_probe_slow+shift])   
        
    n_fast = np.nanmean(mem_fast,axis=1)
    n_slow = np.nanmean(mem_slow,axis=1)
    return n_fast, n_slow

def barscatterdata(ax,x,data,e,c):
    bw = .5
    lw = 3
    ax.bar(x,np.mean(data),bw,color='None',edgecolor=c,lw=lw)
    #standard error of the mean
    #ax.errorbar(0+x,np.mean(data),yerr=np.std(data)/np.sqrt(np.size(data)),
    #    color='k',lw=lw,capsize=5,capthick=lw)

    #normalized within subject errors bars
    ax.errorbar(0+x,np.mean(e),yerr=np.std(e)/np.sqrt(np.size(e)),
        color=c,lw=lw,capsize=8,capthick=lw)

    ax.scatter(np.zeros(np.size(data))+x,data,edgecolor='None',color='k',alpha=.25,clip_on=False)



fig,ax = plt.subplots(1,2,figsize=(9,7))

#EXPERIMENT 2a
subj_dat = load_data(project_name='expt2a')
nsubj = len(subj_dat)
e2a_n_fast, e2a_n_slow = calculate_mem_probetrials(subj_dat,shift=0)
diff_slow_fast = e2a_n_slow-e2a_n_fast
avg_slow_fast = (e2a_n_slow+e2a_n_fast)/2.
norm_fast = e2a_n_fast+(np.mean(avg_slow_fast)-avg_slow_fast)
norm_slow = e2a_n_slow+(np.mean(avg_slow_fast)-avg_slow_fast)
barscatterdata(ax[0],0,e2a_n_fast,norm_fast,col_fast)
barscatterdata(ax[0],1,e2a_n_slow,norm_slow,col_slow)

ax[0].plot([0,1],[e2a_n_fast,e2a_n_slow],'gray',lw=1,alpha=.25)
prettify_plot(ax[0],ylrot=90,xlim=(-.5,1.5),ylim=[1.5,2.5],
         yt=([0,1,2,3,4]),ytl=([0,1,2,3,4]),yl="Working memory performance\n# items correct",
         xt=([0,1]),xtl=(['Fast','Slow']),xl='Probe')


#EXPERIMENT 2b
subj_dat = load_data(project_name='expt2b')
nsubj = len(subj_dat)

e2b_n_fast, e2b_n_slow = calculate_mem_probetrials(subj_dat,shift=1)
diff_slow_fast = e2b_n_slow-e2b_n_fast
avg_slow_fast = (e2b_n_slow+e2b_n_fast)/2.
norm_fast = e2b_n_fast+(np.mean(avg_slow_fast)-avg_slow_fast)
norm_slow = e2b_n_slow+(np.mean(avg_slow_fast)-avg_slow_fast)
barscatterdata(ax[1],0,e2b_n_fast,norm_fast,col_fast)
barscatterdata(ax[1],1,e2b_n_slow,norm_slow,col_slow)
ax[1].plot([0,1],[e2b_n_fast,e2b_n_slow],'gray',lw=1,alpha=.25)
prettify_plot(ax[1],ylrot=90,xlim=(-.5,1.5),ylim=[1.5,2.5],
         yt=([0,1,2,3,4]),ytl=([0,1,2,3,4]),yl=" ",
         xt=([0,1]),xtl=(['Fast','Slow']),xl='Probe')


plt.subplots_adjust(hspace=1,wspace=1.5)
fig.savefig(fig_dir+ '/figure3cd.pdf')
plt.show(block=False)



