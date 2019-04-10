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

font_file = "/Library/Fonts/HelveticaNeue-Light.ttf"
if os.path.isfile(font_file): 
    prop = fm.FontProperties(fname=font_file,size=24)
else: 
    prop = fm.FontProperties(size=24)
fig_dir = '../figures/'

#color defaults
col_slow = (0/255.,98/255.,100/255.)
col_fast = (218/255.,66/255.,36/255.)

#load data from Experiments 2b
subj_dat = load_data(project_name='expt2b')


isubj = 10
iblock = 3
ntrials = 800
t0 = 400
tF = 480
itrials = iblock*ntrials+np.arange(t0,tF,dtype=int)

fig = plt.figure(figsize=(8,6))
ax = plt.subplot(111)
#ax.plot(itrials,subj_dat[isubj].rts[itrials]*1000,'--',color='k',linewidth=1)
ax.plot(itrials,subj_dat[isubj].rts_trailingavg[itrials]*1000,'k',linewidth=4)
#ax.plot(itrials,subj_dat[isubj].rts_runningavg[itrials],'--',color='gray',linewidth=1)
ax.plot(itrials,subj_dat[isubj].rts_runningfastthresh[itrials]*1000,'--',color=col_fast)
ax.plot(itrials,subj_dat[isubj].rts_runningslowthresh[itrials]*1000,'--',color=col_slow)
ax.scatter(itrials[0]+np.where(subj_dat[isubj].fast_rt_trigger[itrials]==1)[0],
            .05*1000*np.ones(np.sum([subj_dat[isubj].fast_rt_trigger[itrials]==1])),
            s=100,color=col_fast,clip_on=False,zorder=20)
ax.scatter(itrials[0]+np.where(subj_dat[isubj].slow_rt_trigger[itrials]==1)[0],
            .7*1000*np.ones(np.sum(subj_dat[isubj].slow_rt_trigger[itrials]==1)),
           s=100,color=col_slow,clip_on=False)
prettify_plot(ax,ylrot=90,xlim=(itrials[0],itrials[-1]+1),ylim=[0,800],
         yt=([0,200,400,600,800]),ytl=([0,200,400,600,800]),yl="Trailing average RT (ms)",
         xt=((iblock*ntrials+400,iblock*ntrials+420,iblock*ntrials+440,iblock*ntrials+460,iblock*ntrials+480)),
         xtl=([400,420,440,460,480]),xl='Trial #',
         yaxoffset=True)
plt.show(block=False)

fig.savefig(fig_dir+ 'figure3b.pdf')
