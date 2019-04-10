import numpy as np
import os, sys, pickle
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib import rc
from necessary_analysis_scripts import *

## plotting defaults
plt.rcParams.update({'font.size': 14})
rc('text', usetex=False)
plt.rcParams['pdf.fonttype'] = 42

font_file = "/Library/Fonts/HelveticaNeue-Light.ttf" #font file on Macs
if os.path.isfile(font_file): 
    prop = fm.FontProperties(fname=font_file,size=24)
else: 
    prop = fm.FontProperties(size=24)


figure_dir = '../figures' 

def calculate_rterrvscorr(subj_dat):

    #analyze RTs
    shift = 3
    shifts = np.arange(-1*shift,0)
    nshifts = np.size(shifts)

    nsubj = len(subj_dat)
    ninfreq = int(4*800*.1)
    rts_shift = np.zeros((ninfreq,nshifts))
    infreq_trials_acc = np.zeros(ninfreq)
    rts_corr = np.zeros((nsubj,nshifts))
    rts_err = np.zeros((nsubj,nshifts))
    for isubj in range(nsubj):

        #sustained attention task 
        infreq_trials_ind = np.where(subj_dat[isubj].freq_trials[:3200]==0)[0]
        infreq_trials_acc = subj_dat[isubj].acc[infreq_trials_ind]==1
        
        #calculate rts prior to each infrequent trial
        for ishift in range(np.size(shifts)):
            shift_inds = infreq_trials_ind+shifts[ishift]
            shift_inds_withinrange = np.logical_and((shift_inds % 800)>=0,(shift_inds% 800)<799)
            rts_shift[shift_inds_withinrange,ishift] = subj_dat[isubj].rts[shift_inds[shift_inds_withinrange]]#-rts_m
        
            
        for ishift in range(np.size(shifts)):
            rts_corr[isubj,ishift] = np.nanmean(rts_shift[:,ishift][np.where(infreq_trials_acc==True)[0]]) #using where because of a bug in a version of numpy
            rts_err[isubj,ishift] = np.nanmean(rts_shift[:,ishift][np.where(infreq_trials_acc==False)[0]])

    rts_corr = np.nanmean(rts_corr,axis=1)*1000
    rts_err = np.nanmean(rts_err,axis=1)*1000

    return rts_corr, rts_err

def calculate_wmerrvscorr(subj_dat):
    
    #number of subjects
    nsubj = len(subj_dat)

    #preallocate empty vectors, 
    wm_n_corr = np.zeros(nsubj) #mean number correct for correct responses in the attention task
    wm_n_err = np.zeros(nsubj)  #mean number correct for incorrect responses in the attention task

    for isubj in range(nsubj):
        #probe trials
        probe_trials = subj_dat[isubj].probe_trials[:3200]==1
        
        #whether the participant got the probe trial correct/incorrect in the sustained attention task
        probes_attnacc = subj_dat[isubj].acc[:3200][probe_trials]

        #how many items the participant got right in the sustained attention task
        wm_n = subj_dat[isubj].wholereport_respacc_total[:3200][probe_trials]

        #average across the same accuracy in the sustained attention task
        wm_n_corr[isubj] = np.nanmean(wm_n[probes_attnacc==1]) #correct responses
        wm_n_err[isubj] = np.nanmean(wm_n[probes_attnacc!=1])  #incorrect resposnes

    return wm_n_corr, wm_n_err

def barscatterdata(ax,x,data,c,i=None):
    bw = .3
    lw = 5

    if i==None:
        i = np.ones(np.size(data))==1
    else:
        i = ~np.isnan(data)
    ax.bar(x,np.nanmean(data[i]),bw,color='None',edgecolor=c,lw=lw)
    #standard error of the mean
    ax.errorbar(0+x,np.nanmean(data[i]),yerr=np.nanstd(data[i])/np.sqrt(np.sum(i)),
       color=c,lw=lw,capsize=10,capthick=lw)

    #normalized within subject errors bars
    # ax.errorbar(0+x,np.mean(e),yerr=np.std(e)/np.sqrt(np.size(e)),
    #     color=c,lw=lw,capsize=8,capthick=lw)

    ax.scatter(np.zeros(np.sum(i))+x,data[i],edgecolor='None',color='k',alpha=.25,clip_on=False)



col_err = [218/255.,66/255.,36/255.]
col_corr = [0/255.,98/255.,100/255.]

dat_1a = load_data(project_name='expt1a')
dat_1b = load_data(project_name='expt1b')

nsubj_1a = len(dat_1a)
nsubj_1b = len(dat_1b)

wm_n_corr_1a,wm_n_err_1a = calculate_wmerrvscorr(dat_1a)
wm_n_corr_1b,wm_n_err_1b = calculate_wmerrvscorr(dat_1b)

rts_corr_1a,rts_err_1a = calculate_rterrvscorr(dat_1a)
rts_corr_1b,rts_err_1b = calculate_rterrvscorr(dat_1b)

fig = plt.figure(figsize=(16,15.5))

ax = plt.subplot(221)
barscatterdata(ax,0,wm_n_err_1a,c=col_err)
barscatterdata(ax,1,wm_n_corr_1a,c=col_corr)
ax.plot([0,1],[np.mean(wm_n_err_1a),np.mean(wm_n_corr_1a)],'k',linewidth=3,zorder=1)
prettify_plot(ax,ylrot=90,xlim=(-.5,1.5),ylim=([0,4]),
             yt=([0,1,2,3,4]),ytl=([0,1,2,3,4]),yl='Working memory performance\n# items correct',t='Expt. 1a',
             xt=([0,1]),xtl=(['Incorrect','Correct']))

ax = plt.subplot(223)
barscatterdata(ax,0,wm_n_err_1b[~np.isnan(wm_n_err_1b)],c=col_err)
barscatterdata(ax,1,wm_n_corr_1b[~np.isnan(wm_n_err_1b)],c=col_corr)
ax.plot([0,1],[np.nanmean(wm_n_err_1b),np.nanmean(wm_n_corr_1b[~np.isnan(wm_n_err_1b)])],'k',linewidth=3,zorder=1)
prettify_plot(ax,ylrot=90,xlim=(-.5,1.5),ylim=([0,4]),
             yt=([0,1,2,3,4]),ytl=([0,1,2,3,4]),yl='Working memory performance\n# items correct',t='Expt. 1b',
             xt=([0,1]),xtl=(['Incorrect','Correct']))

ax = plt.subplot(222)
barscatterdata(ax,0,rts_err_1a,c=col_err)
barscatterdata(ax,1,rts_corr_1a,c=col_corr)
ax.plot([0,1],[np.mean(rts_err_1a),np.mean(rts_corr_1a)],'k',linewidth=3,zorder=1)
prettify_plot(ax,ylrot=90,xlim=(-.5,1.5),ylim=([0,500]),
             yt=([0,100,200,300,400,500]),ytl=([0,100,200,300,400,500]),yl='Trailing average RT (ms)\n3 preceding trials',
             xt=([0,1]),xtl=(['Incorrect','Correct']),t='Expt. 1a')

ax = plt.subplot(224)
barscatterdata(ax,0,rts_err_1b,c=col_err)
barscatterdata(ax,1,rts_corr_1b,c=col_corr)
ax.plot([0,1],[np.mean(rts_err_1b),np.mean(rts_corr_1b)],'k',linewidth=3,zorder=1)
prettify_plot(ax,ylrot=90,xlim=(-.5,1.5),ylim=([0,500]),
             yt=([0,100,200,300,400,500]),ytl=([0,100,200,300,400,500]),yl='Trailing average RT (ms)\n3 preceding trials',
             xt=([0,1]),xtl=(['Incorrect','Correct']),t='Expt. 1b')

plt.subplots_adjust(hspace=.5,wspace=1)

fig.savefig(figure_dir+ '/figure2.pdf')
plt.show(block=False)

