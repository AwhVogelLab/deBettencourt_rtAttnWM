import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os, sys, pickle
import csv
from scipy.stats import ttest_1samp, ttest_rel, ttest_ind
from statistics import mean, stdev
from math import sqrt 

def prettify_plot(ax,
					 xlim=None,xt=None,xtl=None,xl=None,xaxoffset=None,
					 ylim=None,yt=None,ytl=None,yl=None,ylrot=None,yaxoffset=None,
					 t=None,legend=None,legendloc=None):
    '''
    This is a plotting script that makes the default matplotlib plots a little prettier
    '''

    if os.path.isfile("/Library/Fonts/HelveticaNeue-Light.ttf"): 
        prop_light = fm.FontProperties(fname='/Library/Fonts/HelveticaNeue-Light.ttf')    
    else: 
        prop_light = fm.FontProperties()

    if os.path.isfile("/Library/Fonts/HelveticaNeue.ttf"): 
        prop_reg = fm.FontProperties(fname='/Library/Fonts/HelveticaNeue.ttf')    
    else: 
        prop_reg = fm.FontProperties()

    ax.spines['bottom'].set_linewidth(1)
    ax.spines['bottom'].set_color("gray")
    if xaxoffset is not None: ax.spines['bottom'].set_position(('outward', 10))
    if yaxoffset is not None: ax.spines['left'].set_position(('outward', 10))

    ax.spines['left'].set_linewidth(1)
    ax.spines['left'].set_color("gray")
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    ax.yaxis.set_ticks_position("left")   
    ax.tick_params(axis='y',direction='out',length=5,width=1,color='gray')
    ax.xaxis.set_ticks_position("bottom") 
    ax.tick_params(axis='x',direction='out',length=5,width=1,color='gray')
    
    if yt is not None: ax.set_yticks(yt)
    if ytl is not None: ax.set_yticklabels((ytl),fontsize=32,fontproperties=prop_light) 
    if yl is not None: h = ax.set_ylabel(yl,fontsize=36,fontproperties=prop_reg,labelpad=12)
    if ylim is not None: ax.set_ylim(ylim) 
        
    if xt is not None: ax.set_xticks(xt)
    if xtl is not None: ax.set_xticklabels((xtl),fontsize=32,fontproperties=prop_light)
    if xl is not None: ax.set_xlabel(xl,fontsize=36,fontproperties=prop_reg,labelpad=12)
    if xlim is not None: ax.set_xlim(xlim)
    

    if t is not None: ax.set_title(t,y=1.08,fontsize=36,fontproperties=prop_reg)
    if legend is not None: 
        if legendloc is None: L = ax.legend(loc='center left', bbox_to_anchor=(0,.85))
        else: L = ax.legend(loc='center right', bbox_to_anchor=legendloc)
        plt.setp(L.texts,fontsize='large',fontproperties=prop)
    ax.tick_params(axis='both',pad=10)
    plt.locator_params(nbins=8)
    plt.tight_layout()

def plot_adjust_spines(ax, spines):
    '''
    This is another plotting script, that moves spines outward if you don't want the x and y axes to touch 
    '''
    for loc, spine in ax.spines.items():
        if loc in spines:
            spine.set_position(('outward', 10))  # outward by 10 points

@np.vectorize
def calculate_aprime(h,fa):
    '''
    Calculates sensitivity, according to the aprime formula
    '''
    if np.greater_equal(h,fa): a = .5 + (((h-fa) * (1+h-fa)) / (4 * h * (1-fa)))
    else: a = .5 - (((fa-h) * (1+fa-h)) / (4 * fa * (1-h)))
    return a

def resampling_statistics(data,chance,nsubj=None,nsamples=100000,skipfig=True):
    '''
    Nonparametric resampling statistics, for paired comparisons
    '''
    if nsubj is None: nsubj = np.size(data)
        
    #resample subjects with replacement 100,000 times
    subj_resampled = np.random.randint(0,nsubj,(nsamples,nsubj)) 

    #the empy matrix of resampled data for each of these resampled iterations
    data_resampled = np.empty(nsamples) 

    #recalculate mean given the resampled subjects
    for i in range(0,nsamples): data_resampled[i] = np.mean(data[subj_resampled[i,:]])

    #calculate p value 
    p = np.sum(np.less(data_resampled,chance))/float(nsamples) #count number of resample iterations below chance
    if np.equal(p,0): p = 1./float(nsamples)

    if skipfig is False:
        plt.figure(figsize=(4,3))
        ax = plt.subplot(111)
        plt.hist(data_resampled,normed=0,facecolor='gray',edgecolor='gray')
        plt.axvline(np.mean(data_resampled),color='b',lw=2,label='resampled mean')
        plt.axvline(np.mean(data),color='m',lw=1,label='original mean')
        plt.axvline(chance,color='c',lw=2,label='chance')
        make_plot_pretty(ax,ylrot=90,yl='Count (#)',legend='1') 
        plt.show()
    
    m = np.mean(data_resampled)
    sd = np.std(data_resampled)

    return p, m, sd

def resampling_statistics_btwnsubj(data1,data2,nsubj=None,nsamples=100000,skipfig=True):
    '''
    Nonparametric resampling statisticsm, for unpaired comparisons
    '''
    nsubj1 = np.size(data1)
    nsubj2 = np.size(data2)
        
    #resample subjects with replacement 100,000 times
    subj_resampled1 = np.random.randint(0,nsubj1,(nsamples,nsubj1)) 
    subj_resampled2 = np.random.randint(0,nsubj2,(nsamples,nsubj2)) 

    #the empy matrix of resampled data for each of these resampled iterations
    data1_resampled = np.empty(nsamples) 
    data2_resampled = np.empty(nsamples) 

    #recalculate mean given the resampled subjects
    for i in range(0,nsamples): 
        data1_resampled[i] = np.mean(data1[subj_resampled1[i,:]])
        data2_resampled[i] = np.mean(data2[subj_resampled2[i,:]])

    #calculate p value 
    p = np.sum(np.less(data1_resampled,data2_resampled))/float(nsamples) #count number of resample iterations below chance
    if np.equal(p,0): 
        p = 1./float(nsamples)

    if skipfig is False:
        plt.figure(figsize=(4,3))
        ax = plt.subplot(111)
        plt.hist(data_resampled,normed=0,facecolor='gray',edgecolor='gray')
        plt.axvline(np.mean(data_resampled),color='b',lw=2,label='resampled mean')
        plt.axvline(np.mean(data),color='m',lw=1,label='original mean')
        plt.axvline(chance,color='c',lw=2,label='chance')
        make_plot_pretty(ax,ylrot=90,yl='Count (#)',legend='1') 
        plt.show()
    
    m1 = np.mean(data1_resampled)
    m2 = np.mean(data2_resampled)

    return p, m1, m2


def load_data(project_name, load_csv_files=True, behav_dir = '/data/beh/'):
    '''
    Load experimental data

    INPUTS:
    -project_name: the folder name of the project, e.g. expt1a
    -load_csv_files: whether to load csv files (if False, loads pickle files, 
                        which might only be readable on some computers)

    OUTPUTS:
    -subj_dat: contains all of the data from all of the subjects
    '''
    
    #subject list
    project_dir = '../' + project_name + '/' #project directory
    subjects_dir = project_dir + 'subjects/' #subject directory
    subj_name = [f for f in os.listdir(subjects_dir) if not np.logical_or(np.logical_or(f.startswith('EXCLUDED'),f.startswith('.')),f.endswith('EXCLUDED'))]
    if project_name == 'expt3c':
        for i in range(np.size(subj_name)):
            subj_name[i] = subj_name[i][:18]
        subj_name = np.unique(subj_name)
    nsubj = np.size(subj_name) #number of subjects
    if load_csv_files:
        #load the data for each subject
        subj_dat={}
        for i,isubj in enumerate(subj_name):
            if project_name == 'expt3c':
                subj_dir = subjects_dir + behav_dir
            else:
                subj_dir = subjects_dir + isubj + behav_dir
            if project_name!='expt3':
                subj_dat[i]=pd.read_csv(subj_dir + isubj + '_expdat.csv')
            else:
                subj_dat[i]=pd.read_csv(subj_dir + isubj + '_explog.csv')

    else:
        #load the settings class
        display_dir = project_dir + 'display/'
        sys.path.insert(0, display_dir)
        import settings_sustAttnWM
  
        #load the data for each subject
        subj_dat = {}
        for i,isubj in enumerate(subj_name):
            subj_dir = project_dir + 'subjects/' + isubj + behav_dir
            subj_dat[i] = pickle.load( open(subj_dir + isubj + '_expdat.p','rb'))

    return subj_dat

def load_data_cd(project_name):
    '''
    load_data_cd loads the files for the change detection portion of the experiment 
    
    INPUTS:
    - project_name: project folder, for example "expt1a". 
    '''
    #subject list
    project_dir = '../' + project_name + '/' #project directory
    subjects_dir = project_dir + 'subjects/' #subject directory
    subj_name = [f for f in os.listdir(subjects_dir) if not np.logical_or(f.endswith('EXCLUDED'),f.startswith('.'))]
    nsubj = np.size(subj_name) #number of subjects

    subj_dat={}
    for i,isubj in enumerate(subj_name):
        subj_dir = subjects_dir + isubj + '/data/beh/'
        subj_dat[i]=pd.read_csv(subj_dir + isubj + '_cd.csv') 

    return subj_dat 
    
def run_stats_onetail(data1,data2=None):
    '''
    run_stats_onetail runs parametric and nonparametric statistics for the paired comparison data1 > data2
    
    INPUTS
    - data1: a vector of length # subjects
    - data2: can either be a vector of the same size as data1, for a paired comparison
              or a single value, which means that it is chance
    '''

    if data2 is None:
        data = data1
        t, p = ttest_1samp(data1,0) #ttest
    elif np.size(data1)==np.size(data2):
        data = data1-data2
        t, p = ttest_rel(data1,data2) #ttest
    else:
        data = data1-data2
        t, p = ttest_1samp(data1,data2) #ttest

    #parametric - note: I didn't report parametric tests as not all data was normally distributed
    print("Parametric: ttest: t ", np.round(t,decimals=2), "p", '{:0.2e}'.format(p/2)) #one-sided

    #nonparametric
    p,m,sd = resampling_statistics(data,0)
    if np.round(p,decimals=3)<0.001:
        print("Nonparametric p < 0.001")
    else:
        print("Nonparametric p: = {:.3f}".format(p))

    return p

def run_stats_twotail(data1,data2=None):
    '''
    run_stats_twotail runs parametric and nonparametric statistics for the paired comparison data1 != data2
    
    - data2 can either be a vector of the same size as data1, for a paired comparison
            or a single value, which means that it is chance
    '''
    
    if data2 is None:
        data = data1
    elif np.size(data1)==np.size(data2):
        data = data1-data2
    else:
        data = data1-data2
    
    #parametric - note: I didn't report parametric tests as not all data was normally distributed
    t, p = ttest_rel(data1,data2) #ttest
    print("Parametric: ttest: t ", np.round(t,decimals=2), "p", '{:0.2e}'.format(p))

    #nonparametric
    p,m,sd = resampling_statistics(data,0)
    if p>.5:
        p = 1-p
    p = p*2
    if np.round(p,decimals=3)<0.001:
        print("Nonparametric p < 0.001")
    else:
        print("Nonparametric p: = {:.3f}".format(p))
    
    return p

def run_stats_btwnsubj(data1,data2):
    '''
    run_stats_onetail runs parametric and nonparametric statistics for the unpaired comparison data1 > data2
    
    - data1 and data2 do not need to be the same size
    '''
    
    #parametric
    t, p = ttest_ind(data1,data2) #ttest
    print("Parametric: ttest: t ", np.round(t,decimals=2), "p", '{:0.2e}'.format(p/nd))

    #nonparametric
    p,m1,m2 = resampling_statistics_btwnsubj(data1,data2)
    if np.round(p,decimals=3)<0.001:
        print("Nonparametric p < 0.001")
    else:
        print("Nonparametric p: = {:.3f}".format(p))

    return p