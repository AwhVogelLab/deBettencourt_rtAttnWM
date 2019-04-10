import numpy as np
import os, sys, pickle
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc
from necessary_analysis_scripts import *
import scipy.io as sio

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


def calculate_respdeg_probetrials(subj_dat,shift):
    nsubj = len(subj_dat)

    nblocks = 4
    max_nfast_perblock = 30

    mem_fast = np.zeros((nsubj,nblocks*max_nfast_perblock))
    mem_fast[:] = np.nan
    mem_slow = np.zeros((nsubj,nblocks*max_nfast_perblock))
    mem_slow[:] = np.nan

    for isubj in range(nsubj):
    
        i_trig = np.ravel(subj_dat[isubj].rt_triggered)==1

        #calculate preRT for fast trials
        i_fast = np.ravel(subj_dat[isubj].fast_rt_trigger)==1        
        i_fast_ind = np.where(np.logical_and(i_fast[:-1]==True,i_trig[1:]==True))[0]
        for i,i_probe_fast in enumerate(i_fast_ind):
            mem_fast[isubj][i] = np.nanmean(subj_dat[isubj].wm_respcolorminusorigcolor[i_probe_fast+shift])
                
        #calculate preRT for slow trials
        i_slow = np.ravel(subj_dat[isubj].slow_rt_trigger)==1
        i_slow_ind = np.where(np.logical_and(i_slow[:-1]==True,i_trig[1:]==True))[0]
        for i,i_probe_slow in enumerate(i_slow_ind):
            mem_slow[isubj][i] = np.nanmean(subj_dat[isubj].wm_respcolorminusorigcolor[i_probe_slow+shift])   
        
    d_fast = np.nanmean(np.abs(mem_fast),axis=1)
    d_slow = np.nanmean(np.abs(mem_slow),axis=1)
    return d_fast, d_slow


def barscatterdata(ax,x,data,e,c):
    bw = .35
    lw = 3
    ax.bar(x,np.mean(data),bw,color='None',edgecolor=c,lw=lw)
    #standard error of the mean
    #ax.errorbar(0+x,np.mean(data),yerr=np.std(data)/np.sqrt(np.size(data)),
    #    color=c,lw=lw,capsize=5,capthick=lw)

    #normalized within subject errors bars
    ax.errorbar(0+x,np.mean(e),yerr=np.std(e)/np.sqrt(np.size(e)),
        color=c,lw=lw,capsize=8,capthick=lw)

    ax.scatter(np.zeros(np.size(data))+x,data,edgecolor='None',color='k',alpha=.25,clip_on=False)

col_fast = [218/255.,66/255.,36/255.]
col_slow = [0/255.,98/255.,100/255.]



fig,ax = plt.subplots(1,3,figsize=(16,7))

project_name='expt3a'
subj_dat = load_data(project_name=project_name)
nsubj = len(subj_dat)
bin_width=20.
bins = np.arange(-180,180+bin_width,bin_width)
bin_height = np.empty((nsubj,np.size(bins)-1))
x = bins[:-1]+bin_width/2
for isubj in range(nsubj):
    iprobe = ~np.isnan(subj_dat[isubj].wm_respcolorminusorigcolor)
    bin_height[isubj],_ = np.histogram(subj_dat[isubj].wm_respcolorminusorigcolor[iprobe],bins,density=True)
#for ib in range(np.size(bins)-1):
#    ax[0].scatter(np.zeros(nsubj)+bins[ib]+bin_width/2,bin_height[:,ib],color='k',alpha=.15,linewidths=None,edgecolors='none',clip_on=False)
ax[0].bar(x,np.mean(bin_height,axis=0),bin_width-3,color='None',edgecolor='k',linewidth=1,align='center')
ax[0].errorbar(bins[:-1]+bin_width/2,np.mean(bin_height,axis=0),yerr=np.std(bin_height,axis=0)/np.sqrt(float(nsubj)),
    linestyle='None',color='k',linewidth=1,capsize=0,capthick=2)
prettify_plot(ax[0],ylrot=90,ylim=[0,.02],
         yt=([0,.005,.01,.015,.02]),ytl=([0,.005,.01,.015,.02]),yl="Proportion",
         xt=[-180,-90,0,90,180],xtl=[-180,-90,0,90,180],xl='Response error (o)')


e3_d_fast, e3_d_slow = calculate_respdeg_probetrials(subj_dat,shift=1)
diff_slow_fast = e3_d_slow-e3_d_fast
avg_slow_fast = (e3_d_slow+e3_d_fast)/2.
norm_fast = e3_d_fast+(np.mean(avg_slow_fast)-avg_slow_fast)
norm_slow = e3_d_slow+(np.mean(avg_slow_fast)-avg_slow_fast)

barscatterdata(ax[1],0,e3_d_fast,norm_fast,col_fast)
barscatterdata(ax[1],1,e3_d_slow,norm_slow,col_slow)
ax[1].plot([0,1],[e3_d_fast,e3_d_slow],'gray',lw=1,alpha=.25)
prettify_plot(ax[1],ylrot=90,xlim=(-.5,1.5),ylim=[0,80],
         yt=([0,20,40,60,80]),ytl=([0,20,40,60,80]),yl="Delta (deg)",
         xt=([0,1]),xtl=(['Fast','Slow']),xl='Probe')

project_name='expt3b'
subj_dat = load_data(project_name=project_name)
nsubj = len(subj_dat)

e3_d_fast, e3_d_slow = calculate_respdeg_probetrials(subj_dat,shift=1)
diff_slow_fast = e3_d_slow-e3_d_fast
avg_slow_fast = (e3_d_slow+e3_d_fast)/2.
norm_fast = e3_d_fast+(np.mean(avg_slow_fast)-avg_slow_fast)
norm_slow = e3_d_slow+(np.mean(avg_slow_fast)-avg_slow_fast)

barscatterdata(ax[2],0,e3_d_fast,norm_fast,col_fast)
barscatterdata(ax[2],1,e3_d_slow,norm_slow,col_slow)
ax[2].plot([0,1],[e3_d_fast,e3_d_slow],'gray',lw=1,alpha=.25)
prettify_plot(ax[2],ylrot=90,xlim=(-.5,1.5),ylim=[0,80],
         yt=([0,20,40,60,80]),ytl=([0,20,40,60,80]),yl="Delta (deg)",
         xt=([0,1]),xtl=(['Fast','Slow']),xl='Probe')


plt.subplots_adjust(hspace=.5,wspace=.5)
#fig.savefig(fig_dir+ '/figure4bcd.pdf')
plt.show(block=False)

