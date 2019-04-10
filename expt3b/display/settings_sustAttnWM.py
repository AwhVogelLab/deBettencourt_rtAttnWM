# -*- coding: utf-8 -*-
'''settings.py
Define global and environment-specific settings here.
'''

from __future__ import division
import os, glob, sys, math, itertools
import numpy as np
from scipy.spatial.distance import pdist
import helper_functions_sustAttnWM as hf
if 'psychopy' in sys.modules:
    from psychopy import visual, core, event, tools, misc, monitors
    import psychopy.tools.colorspacetools as cst
#all the details about the images
class ExperimentalDisplay(object):

    
    def __init__(self,expt_design,gui_specs):

        #basic specs
        self.subj_name = gui_specs['subj_name']
        self.debug = gui_specs['debug']
        self.env = gui_specs['env']
        self.project_dir = gui_specs['project_dir']

        #screen window
        self.scrcolor = (0,0,0)
        self.scrunits = 'deg'
        if self.debug:
            self.scrfull = False
            self.scrw = 1200
            self.scrh = 1200
        else:
            self.scrfull = True
            self.scrw = 1440
            self.scrh = 900
        self.win = visual.Window(size = (self.scrw,self.scrh),monitor=self.env,fullscr = self.scrfull, color=self.scrcolor, units=self.scrunits) #main 
        self.mon = monitors.Monitor(self.env)
        
        #fixation dot parameters
        self.fixrad = .1
        self.fixcolor = -1.
        self.fixlinecolor = 0
        self.fix = visual.Circle(self.win,radius=self.fixrad, fillColor=self.fixcolor,lineColor=self.fixlinecolor)

        #stimuli appear at fixed eccentricity along a circle
        self.circrad = expt_design.positions_rad
        self.circoffset = .25
        self.circedges = 256.

        #stimulus parameters of squares
        self.square_size = 1.5
        self.square = visual.Rect(self.win, width = self.square_size, height = self.square_size, lineColor=None, fillColor = [1,1,1], fillColorSpace='rgb')
        self.circle = visual.Circle(self.win, radius = self.square_size/2, edges = self.circedges, lineColor=None, fillColor = [1,1,1], fillColorSpace='rgb')

        #other task parameters
        self.mouse = event.Mouse(visible=0,win=self.win)  #mouse

        #make the colorwheel
        self.colortextureRes = 512
        self.colortexhsv = np.ones([self.colortextureRes,self.colortextureRes,3], dtype=float)
        self.colortexhsv[:,:,0] = np.linspace(0,self.colortextureRes,self.colortextureRes, endpoint=False)
        self.colortexhsv[:,:,1] = 1
        self.colortexhsv[:,:,2] = 1
        rgb = misc.hsv2rgb(self.colortexhsv)
        rgb = np.tile(expt_design.rgb_circlepts,(self.colortextureRes,1,1))
        mask = np.zeros([100,1])
        mask[-10:] = 1  # 10% of the radius is 1 (visible)
        self.colortexrgb = rgb
        self.colorcirc = visual.RadialStim(self.win, tex=rgb, mask = mask,size=(self.circrad+self.circoffset)*2,ori=0, angularRes=256, angularCycles=1, interpolate=True)        

        #stimuli for drawing the path of the experiment
        self.start_circle = visual.ShapeStim(self.win,size=1.5,vertices=((-1,-.75),(-1,.75),(1,.75),(1,-.75)),pos=(-6,-6),lineWidth=2,lineColor='black',fillColor='white')
        self.start_text = visual.TextStim(self.win,text='Start',pos=(-6,-5.75),height=1,color=-1,fontFiles=[self.project_dir +'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.block_outter= visual.Circle(self.win, units = 'deg',radius = .5, pos = (-5,-7.75), lineColor=0,lineWidth=0,fillColor=-1)
        self.block_inner= visual.Circle(self.win, units = 'deg',radius = .4, pos = (-5,-7.75), lineColor=0,lineWidth=0,fillColor=0)
        star5vertices = [(-7,2.5),(-3.5,-2),(-5,-7),(-.5,-4.5),(5,-7),(3.5,-2),(7,2.5),(2,2),(-.5,7),(-2,2)]
        self.finish_star = visual.ShapeStim(self.win,size=.25,vertices=star5vertices,pos=(6,-5.5),lineWidth=2,lineColor='black',fillColor='white')
        self.finish_text = visual.TextStim(self.win,text='End',pos=(6,-5.75),height=1,color=-1,fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.prog_rect = visual.Rect(self.win, units = 'deg',width = 10, height = 5, pos = (0,0), lineColor=-1,lineWidth=5,fillColor=0)
        self.prog_bar = visual.Rect(self.win, units = 'deg',width = .1, height = 5, pos = (0,0), lineColor=-1,lineWidth=5,fillColor=-1)

        #text parameters
        self.text_welcome = visual.TextStim(self.win, text='Welcome to the magical technicolor shapes adventure!',alignHoriz='center',wrapWidth=20,height=1,pos=(0,7),color=(-1,-1,-.5),fontFiles=[self.project_dir + 'display/fonts/BowlbyOneSC-Regular.ttf'],font=['Bowlby One SC'])
        self.text_block_start = visual.TextStim(self.win, text='Block i of n',alignHoriz='center',wrapWidth=20,height=1,pos=(0,7),color=(-1,-1,-.5),fontFiles=[self.project_dir + 'display/fonts/BowlbyOneSC-Regular.ttf'],font=['Bowlby One SC'])             
        self.text_advance = visual.TextStim(self.win, text='Press spacebar to continue',alignHoriz='center',wrapWidth=20,height=.75,pos=(0,-8),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_end_expt = visual.TextStim(self.win, text='All done!\n\nPress spacebar to exit',alignHoriz='center',wrapWidth=20,height=1,pos=(0,3),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])        


#all the details about the experiment
class ExperimentalDesign(object):

    def __init__(self,gui_specs):

        #basic settings from gui
        self.subj_name = gui_specs['subj_name']
        self.restarting = gui_specs['restarting']
        self.env = gui_specs['env']
        self.expt_date = gui_specs['expt_date']
        self.debug = gui_specs['debug']
        self.seed = gui_specs['seed'] 
        self.project_dir = gui_specs['project_dir']
        self.save_dir = gui_specs['save_dir']
        np.random.seed(seed = self.seed) #seed the random number generator

        self.key_escape = ['escape']
        self.key_advance = ['space']
        self.key_freq = ['d']
        self.key_infreq = ['s']
        self.key_repeat = ['r']
        self.key_skip = ['p']

        if self.debug:          #when debugging, run fewer # blocks and # trials
            self.nblocks = 1
        else:
            self.nblocks = 6

        #the set sizes of the encoding arrays
        self.setsize = 6

        #proportion of the frequent trials
        self.prop_freq = .9

        #possible position
        self.positions_rad = 4
        self.positions = np.arange(0,self.setsize)
        self.positions_deg = self.positions*360/self.setsize
        self.positions_x = np.zeros(self.setsize)
        self.positions_y = np.zeros(self.setsize)
        for i in range(self.setsize):
            self.positions_x[i],self.positions_y[i] = tools.coordinatetools.pol2cart(self.positions_deg[i],self.positions_rad,units='deg')

        #number of trials within each fully balanced block - assumes multiple of 100!
        if self.debug:
            self.ntrials_perblock = 100
        else:
            self.ntrials_perblock = 800 
        
        #trial parameters:
        self.freq_trials = np.zeros((self.nblocks,self.ntrials_perblock),dtype=np.int)
        self.freq_categ = 'circle'
        self.infreq_categ = 'square'

        self.trials_colorind = np.zeros((self.nblocks,self.ntrials_perblock,self.setsize),dtype=np.int)
        self.trials_colordeg = np.zeros((self.nblocks,self.ntrials_perblock,self.setsize),dtype=np.int)
        self.trials_colorrgb = np.zeros((self.nblocks,self.ntrials_perblock,self.setsize,3))
        self.correct_response = np.zeros((self.nblocks,self.ntrials_perblock),dtype=np.int)

        self.l = 70
        self.a = 20
        self.b = 38
        self.r = 60
        self.n = 512
        self.lab_circlepts = np.empty((self.n,2))
        self.rgb_circlepts = np.empty((self.n,3))
        for i in range(self.n):
            x = (self.a + self.r * np.sin(np.deg2rad(float(i)/self.n*360)))
            y = (self.b + self.r * np.cos(np.deg2rad(float(i)/self.n*360)))
            self.lab_circlepts[i] = [x,y]
            self.rgb_circlepts[i] = cst.cielab2rgb([self.l, x, y],transferFunc=cst.srgbTF,clip=True)

        self.miniblocksize = 100
        self.infreqtrials_dist = 2
        for ib in range(self.nblocks):
            
            #reshuffle the full factorial design for each block
            for i in range(int(self.ntrials_perblock/self.miniblocksize)):
                x = np.ones(int(self.miniblocksize*self.prop_freq),dtype=int)
                y = np.zeros(int(np.round(self.miniblocksize*(1-self.prop_freq))),dtype=int)
                z = np.append(x,y)
                np.random.shuffle(z)
                while np.any(z[0]==0) or np.any(z[-1]==0) or np.any(np.diff(np.where(z==0)[0])<self.infreqtrials_dist):
                    np.random.shuffle(z)
                self.freq_trials[ib][i*self.miniblocksize+np.arange(0,self.miniblocksize)] = z
            
            #correct response for each trial
            self.correct_response[ib][self.freq_trials[ib,:]==1]=1 #same trials
            self.correct_response[ib][self.freq_trials[ib,:]==0]=0 #different trials  

            #color assigned to each position
            for it in range(self.ntrials_perblock):
                self.trials_colorind[ib,it] = np.tile(np.random.choice(self.n,1, replace=False)[0],self.setsize)
                self.trials_colordeg[ib,it] = np.tile(float(self.trials_colorind[ib,it][0])/self.n*360,self.setsize)

            #ensure that the same color doesn't appear in the same position back to back
            diff_zero = np.abs(np.diff(self.trials_colorind[ib][:,0]))
            for it in np.where(diff_zero<=42)[0]:
                used_colors1 = np.arange(self.trials_colorind[ib,it-1][0]-42,self.trials_colorind[ib,it-1][0]+42) % self.n
                used_colors2 = np.arange(self.trials_colorind[ib,it+1][0]-42,self.trials_colorind[ib,it+1][0]+42) % self.n
                used_colors = np.unique(np.append(used_colors1,used_colors2))
                avail_colors = np.setdiff1d(np.arange(self.n),used_colors)
                self.trials_colorind[ib,it] = np.tile(np.random.choice(avail_colors,size=1)[0],self.setsize)
                self.trials_colordeg[ib,it] = np.tile(float(self.trials_colorind[ib,it][0])/self.n*360,self.setsize)

            #set up the rgb vales for each trial
            for it in range(self.ntrials_perblock):
                for ii in range(self.setsize):
                    #hsv = (self.trials_colorind[ib,it][ii],1,1)
                    #print hsv
                    self.trials_colorrgb[ib,it][ii] = self.rgb_circlepts[self.trials_colorind[ib,it][ii]]
                    #print self.trials_colorrgb[ib,it]

        #which trials to test WM
        self.n_trials_atstart = 80
        self.n_probes_atstart = int(self.n_trials_atstart*.05)
        self.n_freq_perblock = int(np.sum(self.freq_trials[0]==1))
        self.n_infreq_perblock = int(np.sum(self.freq_trials[0]==0))
        self.probetrials_dist = 2
        self.nprobetrials = int(self.ntrials_perblock*.05) 
        self.probe_trials = np.zeros((self.nblocks,self.ntrials_perblock),dtype=int)

        for ib in range(self.nblocks):

            #randomize order of probe trials 
            z = np.random.choice(self.n_trials_atstart,size=self.n_probes_atstart,replace=False)
            while np.any(z<3) or np.any(z>(self.n_trials_atstart-3)) or np.any(np.diff(z)<self.probetrials_dist) or np.any(self.freq_trials[ib,z]==0):
                z = np.random.choice(self.n_trials_atstart,size=self.n_probes_atstart,replace=False)

            self.probe_trials[ib][z] = 1

        #sustained attention responses
        self.actual_response_string = [[" " for i in range(self.ntrials_perblock)] for j in range(self.nblocks)]
        self.actual_response = np.zeros((self.nblocks,self.ntrials_perblock))
        self.actual_response[:] = np.nan
        self.acc = np.zeros((self.nblocks,self.ntrials_perblock))
        self.acc[:] = np.nan
        self.rts = np.zeros((self.nblocks,self.ntrials_perblock))
        self.rts[:] = np.nan

        #real-time triggering variables
        self.rts_trailingavg = np.zeros((self.nblocks,self.ntrials_perblock))
        self.rts_runningavg = np.zeros((self.nblocks,self.ntrials_perblock))
        self.rts_runningstd = np.zeros((self.nblocks,self.ntrials_perblock))
        self.rts_runningslowthresh = np.zeros((self.nblocks,self.ntrials_perblock))
        self.rts_runningfastthresh = np.zeros((self.nblocks,self.ntrials_perblock))
        self.rt_triggered_slow = np.zeros((self.nblocks,self.ntrials_perblock))
        self.rt_triggered_fast = np.zeros((self.nblocks,self.ntrials_perblock))
        self.rt_triggered = np.zeros((self.nblocks,self.ntrials_perblock))
        self.n_rt_triggered_slow = int(self.nprobetrials/2-self.n_probes_atstart/2)
        self.n_rt_triggered_fast = int(self.nprobetrials/2-self.n_probes_atstart/2)

        #set the first 80 to nan
        self.rts_trailingavg[:,0:self.n_trials_atstart] = np.nan
        self.rts_runningavg[:,0:self.n_trials_atstart] = np.nan
        self.rts_runningstd[:,0:self.n_trials_atstart] = np.nan
        self.rts_runningslowthresh[:,0:self.n_trials_atstart] = np.nan
        self.rts_runningfastthresh[:,0:self.n_trials_atstart] = np.nan
        self.rt_triggered_slow[:,0:self.n_trials_atstart] = np.nan
        self.rt_triggered_fast[:,0:self.n_trials_atstart] = np.nan
        self.rt_triggered[:,0:self.n_trials_atstart] = np.nan

        #mouse click responses
        self.wm_mousepos = np.zeros((self.nblocks,self.ntrials_perblock))
        self.wm_respdeg = np.zeros((self.nblocks,self.ntrials_perblock))
        self.wm_respdeg_in_colorspace = np.zeros((self.nblocks,self.ntrials_perblock))
        self.wm_respind = np.zeros((self.nblocks,self.ntrials_perblock))
        self.wm_resprgb = np.zeros((self.nblocks,self.ntrials_perblock,3))
        self.wm_respcolorminusorigcolor = np.zeros((self.nblocks,self.ntrials_perblock))
        self.wm_rts = np.zeros((self.nblocks,self.ntrials_perblock,self.setsize))

        self.wm_mousepos[:] = np.nan
        self.wm_respdeg[:] = np.nan
        self.wm_respdeg_in_colorspace[:] = np.nan
        self.wm_respind[:] = np.nan
        self.wm_respcolorminusorigcolor[:] = np.nan
        self.wm_rts[:] = np.nan

        #counter
        self.counter_trial = np.zeros(self.nblocks,dtype=int)

        #wm timing
        self.t_stim = .5
        self.t_isi = .3
        self.t_enc = self.t_stim+self.t_isi
        self.t_poststim = 1.
        self.t_iti = 1.

        #Working memory logging timing parameters:
        self.time_blockstart = np.empty(self.nblocks)
        self.time_blockstart[:] = np.nan
        self.time_encarray_onset = np.empty((self.nblocks,self.ntrials_perblock))
        self.time_encarray_onset[:] = np.nan
        self.time_encarray_offset = np.empty((self.nblocks,self.ntrials_perblock))
        self.time_encarray_offset[:] = np.nan
        self.time_memprobe_onset = np.empty((self.nblocks,self.ntrials_perblock))
        self.time_memprobe_onset[:] = np.nan
        self.time_response = np.empty((self.nblocks,self.ntrials_perblock))
        self.time_response[:] = np.nan
        self.time_memprobe_offset = np.empty((self.nblocks,self.ntrials_perblock))
        self.time_memprobe_offset[:] = np.nan
        self.time_iti_onset = np.empty((self.nblocks,self.ntrials_perblock))
        self.time_iti_onset[:] = np.nan
        self.time_iti_offset = np.empty((self.nblocks,self.ntrials_perblock))
        self.time_iti_offset[:] = np.nan

