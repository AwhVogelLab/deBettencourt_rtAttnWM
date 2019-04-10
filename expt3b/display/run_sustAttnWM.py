#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''Runs the experiment.
Author: MdB 04/2017 s
'''

import pygame, time, pickle, csv
import numpy as np
import os.path
from psychopy import core, gui, event
from task_sustAttnWM import Task
from datetime import datetime
from shutil import copyfile
import settings_sustAttnWM as settings
import helper_functions_sustAttnWM as hf


#get basic specifications for this experiment from GUI
gui_specs = hf.get_specs()
print "Subject: ", gui_specs['subj_name']

#set up the experimental design
if not gui_specs['restarting'] or gui_specs['debug']:
    #create experiment design
    expt_design = settings.ExperimentalDesign(gui_specs)
else:
    expt_design = hf.openorcreate_designfile(gui_specs)

#set up the experiment display and task variables 
expt_display = settings.ExperimentalDisplay(expt_design,gui_specs)
exp = Task(expt_design,expt_display)

#save files
filename = gui_specs['save_dir'] + gui_specs['subj_name'] + '_' + 'expdat.p'
pickle.dump( exp.dsgn, open( filename, "wb" ) )

#open csv files to save
f = hf.open_csv_data_file(gui_specs,gui_specs['subj_name'] + '_explog')
hf.open_csv_info_file(gui_specs,gui_specs['subj_name'] + '_expinfo')

#initialize the clock
clock = core.Clock()
clock.reset()

#set mouse invisible 
if not gui_specs['debug']:
    exp.disp.win.setMouseVisible(False)

#welcome screen
exp.welcomeToExperiment()

#instructions
if exp.dsgn.counter_trial[0]==0:
    exp.instructionsSustAttn(clock)
    exp.instructionsWholeReport(clock)
    exp.instructionsBoth(clock)

#block loop
block0 = np.where(exp.dsgn.counter_trial<exp.dsgn.ntrials_perblock)[0][0]
print block0
for iblock in range(block0,exp.dsgn.nblocks):

    #display start of block screen 
    exp.startOfBlock(iblock,clock,f=f)

    #if first trial of first block, write header line to file
    if iblock == 0 and exp.dsgn.counter_trial[iblock]==0:
        hf.write_to_csv_data_file(f,0,0,exp.dsgn,headerLine=True)
        
    #set mouse invisible 
    if not gui_specs['debug']:
        exp.disp.win.setMouseVisible(False)
        
    #trial loop
    for itrial in np.arange(exp.dsgn.counter_trial[iblock],exp.dsgn.ntrials_perblock):
        print itrial
        exp.encodingArray(iblock,itrial,clock)
        if exp.dsgn.probe_trials[iblock,itrial]==1:
            exp.retentionInterval(iblock,itrial,clock)
            exp.memoryProbe(iblock,itrial,clock,f=f)
            exp.itiWM(iblock,itrial,clock)
            
        #update counter
        exp.dsgn.counter_trial[iblock] = exp.dsgn.counter_trial[iblock]+1
       
        #save pickle file
        filename = gui_specs['save_dir'] + gui_specs['subj_name'] + '_' + 'expdat.p'
        pickle.dump( exp.dsgn, open( filename, "wb" ) )
        
        #save csv
        hf.write_to_csv_data_file(f,iblock,itrial,exp.dsgn) 


#close and copy files with timestamps to prevent overwriting by accident
today = datetime.now()
filename_old = gui_specs['save_dir'] + gui_specs['subj_name'] + '_explog.csv'
filename_new = gui_specs['save_dir'] + gui_specs['subj_name'] + '_explog_' + today.strftime('%Y%m%d_%H%M%S') + '.csv'
copyfile(filename_old,filename_new)
filename_old = gui_specs['save_dir'] + gui_specs['subj_name'] + '_expdat.p'
filename_new = gui_specs['save_dir'] + gui_specs['subj_name'] + '_expdat_' + today.strftime('%Y%m%d_%H%M%S') + '.csv'
copyfile(filename_old,filename_new)

# end of experiment screen 
exp.endOfExperiment(f=f)