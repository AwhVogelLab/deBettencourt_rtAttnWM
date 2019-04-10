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
    from psychopy import visual, core, event, tools

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
        if not self.env == 'other':
            self.win = visual.Window(size = (self.scrw,self.scrh),monitor=self.env,fullscr = self.scrfull, color=self.scrcolor, units=self.scrunits) #main 
        else:
            self.win = visual.Window(size = (self.scrw,self.scrh),monitor='testMonitor',fullscr = self.scrfull, color=self.scrcolor, units=self.scrunits) #main 

        #fixation dot parameters
        self.fixrad = .1
        self.fixcolor = -1.
        self.fixlinecolor = 0
        self.fix = visual.Circle(self.win,radius=self.fixrad, fillColor=self.fixcolor,lineColor=self.fixlinecolor)

        #
        self.colors_ind = expt_design.colors_ind
        self.ncolors = expt_design.ncolors
        self.colors_rgb = expt_design.colors_rgb

        #stimulus parameters of squares
        self.square_size = 1.5
        self.square = visual.Rect(self.win, width = self.square_size, height = self.square_size, lineColor=None, fillColor = [1,1,1], fillColorSpace='rgb')
        self.square_pos = {}
        for i in range(6):
            self.square_pos[i] = visual.Rect(self.win, width = self.square_size, height = self.square_size, 
                                            pos = (expt_design.positions_x[i],expt_design.positions_y[i]),
                                            lineColor=[-1,-1,-1], lineWidth=2, fillColor = None, fillColorSpace='rgb')
        
        self.wholereportpos = [[-.5,.5],[0,.5],[.5,.5],[-.5,0],[0,0],[.5,0],[-.5,-.5],[0,-.5],[.5,-.5]]
        self.wholereportsquare = {}
        for i in range(6):
            for j in range(9):
                self.wholereportsquare[i,j] = visual.Rect(self.win, width = self.square_size/3, height = self.square_size/3, 
                            pos = self.wholereportpos[i], lineColor=None, fillColor = self.colors_rgb[j], fillColorSpace='rgb')
                self.wholereportsquare[i,j].pos = (self.wholereportpos[int(j)][0] + expt_design.positions_x[i], 
                                                    self.wholereportpos[int(j)][1] + expt_design.positions_y[i])
        self.circle = visual.Circle(self.win, radius = self.square_size/2, edges=32, lineColor=None, fillColor = [1,1,1], fillColorSpace='rgb')

        #other task parameters
        self.mouse = event.Mouse(visible=0,win=self.win)  #mouse
        self.stimposrad = 4.

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
        self.text_welcome = visual.TextStim(self.win, text='Welcome to the circles and squares game!',alignHoriz='center',wrapWidth=20,height=1,pos=(0,7),color=(-1,-1,-.5),fontFiles=[self.project_dir + 'display/fonts/BowlbyOneSC-Regular.ttf'],font=['Bowlby One SC'])
        self.text_block_start = visual.TextStim(self.win, text='Block i of n',alignHoriz='center',wrapWidth=20,height=1,pos=(0,7),color=(-1,-1,-.5),fontFiles=[self.project_dir + 'display/fonts/BowlbyOneSC-Regular.ttf'],font=['Bowlby One SC'])             
        self.text_instructions5 = visual.TextStim(self.win, text="Now, finally, let's put it all together. We will practice both tasks: Press d for circles, s for squares, and then use your mouse to click at each location",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,7),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_instructions6 = visual.TextStim(self.win, text="If this is confusing, please ask the experimenter any questions that you may have!\n\nOr, press spacebar to start the experiment. Good luck!",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,7),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])

        self.text_feedbackCorrect = visual.TextStim(self.win, text="Correct!",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,1),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_feedbackIncorrect = visual.TextStim(self.win, text="Incorrect",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,1),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_advance = visual.TextStim(self.win, text='Press spacebar to continue',alignHoriz='center',wrapWidth=20,height=.75,pos=(0,-8),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_end_expt = visual.TextStim(self.win, text='All done!\n\nPress spacebar to exit',alignHoriz='center',wrapWidth=20,height=1,pos=(0,3),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])        
        self.text_either_key = visual.TextStim(self.win, text='Press either key (s or d) to continue',alignHoriz='center',wrapWidth=20,height=.75,pos=(0,-2.5),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])

        self.text_CDinstructions0 = visual.TextStim(self.win, text="In the last part, colorful blocks like this one will appear on the screen\n\nYour goal will be to remember the color of each block",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,3),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_CDinstructions1 = visual.TextStim(self.win, text="Then, after some time, one block will reappear.\n\nSometimes it will be the same color",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,3),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_CDinstructions2 = visual.TextStim(self.win, text="And sometimes it will reappear in a different color",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,3),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_CDinstructions3 = visual.TextStim(self.win, text="So you'll need to hold in mind the original color of each block\n\nThen, if it reappears in the same color, press the key with a ?\nOr, if it reappears in a different color press the z key",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,3),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_CDinstructions4 = visual.TextStim(self.win, text="Let's practice this now",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,3),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_CDinstructions5 = visual.TextStim(self.win, text="Let's try another, but now 2 blocks will appear at the start\n\nThe computer will randomly test you on one of the blocks",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,3),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_CDinstructions6 = visual.TextStim(self.win, text="In the real game, there will be 6 blocks all at once.\n\nIt may feel challenging, but please try your best!\n\nLet's practice this now",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,3),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_CDinstructions7 = visual.TextStim(self.win, text="Press spacebar to start the main game. Good luck!",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,3),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])      
        self.text_CDinstructionsCorrect = visual.TextStim(self.win, text="Correct!",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,3),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_CDinstructionsIncorrect = visual.TextStim(self.win, text="Incorrect\n\nRemember to hold in mind the color of the blocks, and then decide if the color is the same (?) or different (z).\n\nLet's try that again",alignHoriz='center',wrapWidth=22,height=.75,pos=(0,3),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_same = visual.TextStim(self.win, text=u'Press ? if same',alignHoriz='center',wrapWidth=22,height=.75,pos=(4,-6),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.text_diff = visual.TextStim(self.win, text=u'Press z if different',alignHoriz='center',wrapWidth=22,height=.75,pos=(-4,-6),color=(-1,-1,-1),fontFiles=[self.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])         


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
        self.key_same = ['slash']
        self.key_diff = ['z']
        self.key_one = ['1']
        self.key_two = ['2']
        self.key_three = ['3']
        self.key_four = ['4']
        self.key_freq = ['d']
        self.key_infreq = ['s']
        self.key_repeat = ['r']
        self.key_skip = ['p']

        self.colors_ind = np.arange(9)
        self.ncolors = np.size(self.colors_ind)
        self.colors_rgb = [[1, -1, -1],[-1, 1, -1],[-1, -1, 1],[1, 1, -1],[1, -1, 1],[-1, 1, 1],[1, 1, 1],[-1, -1, -1],[1, 0, -1]]

        if self.debug:          #when debugging, run fewer # blocks and # trials
            self.nblocks = 1
        else:
            self.nblocks = 4

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
        self.trials_colorrgb = np.zeros((self.nblocks,self.ntrials_perblock,self.setsize,3))
        self.correct_response = np.zeros((self.nblocks,self.ntrials_perblock),dtype=np.int)

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
                self.trials_colorind[ib,it] = np.random.choice(self.ncolors,size=self.setsize, replace=False)

            #ensure that the same color doesn't appear in the same position back to back
            for ii in range(self.setsize):
                diff_zero = np.diff(self.trials_colorind[ib][:,ii])
                for it in np.where(diff_zero==0)[0]:
                    if it > 0:
                        used_colors = np.append(np.append(self.trials_colorind[ib][it,:],self.trials_colorind[ib][it-1,ii]),self.trials_colorind[ib][it+1,ii])
                        avail_colors = np.setdiff1d(self.colors_ind,used_colors)
                        self.trials_colorind[ib,it,ii] = np.random.choice(avail_colors,size=1)

            #set up the rgb vales for each trial
            for it in range(self.ntrials_perblock):
                for ii in range(self.setsize):
                    self.trials_colorrgb[ib,it][ii] = self.colors_rgb[self.trials_colorind[ib,it][ii]]

        #which trials to test WM
        self.prop_probe = .5
        self.n_probes_perblock = int(np.round(self.ntrials_perblock*(1-self.prop_freq)*self.prop_probe))
        self.n_freq_perblock = int(np.sum(self.freq_trials[0]==1))
        self.n_infreq_perblock = int(np.sum(self.freq_trials[0]==0))
        self.probetrials_dist = 2

        self.probe_trials = np.zeros((self.nblocks,self.ntrials_perblock),dtype=int)
        self.probe_trials_ind = np.zeros((self.nblocks,self.n_probes_perblock),dtype=int)
        for ib in range(self.nblocks):
            
            #randomize order of probe trials 
            z = np.random.choice(self.n_freq_perblock,size=self.n_probes_perblock,replace=False)
            while np.any(z[0:3]==0) or np.any(z[-3:]==0) or np.any(np.diff(np.where(z==0)[0])<self.probetrials_dist):
                z = np.random.choice(self.n_freq_perblock,size=self.n_probes_perblock,replace=False)

            freq_trials_ind = np.where(self.freq_trials[ib]==1)[0]

            self.probe_trials_ind[ib] = freq_trials_ind[z]
            self.probe_trials[ib][self.probe_trials_ind[ib]] = 1

        #sustained attention responses
        self.actual_response_string = [[" " for i in range(self.ntrials_perblock)] for j in range(self.nblocks)]
        self.actual_response = np.zeros((self.nblocks,self.ntrials_perblock))
        self.actual_response[:] = np.nan
        self.acc = np.zeros((self.nblocks,self.ntrials_perblock))
        self.acc[:] = np.nan
        self.rts = np.zeros((self.nblocks,self.ntrials_perblock))
        self.rts[:] = np.nan

        #mouse click responses
        self.wholereport_resp = np.zeros((self.nblocks,self.ntrials_perblock,self.setsize))
        self.wholereport_resporder = np.zeros((self.nblocks,self.ntrials_perblock,self.setsize))
        self.wholereport_respcolorind = np.zeros((self.nblocks,self.ntrials_perblock,self.setsize))
        self.wholereport_resprgb = np.zeros((self.nblocks,self.ntrials_perblock,self.setsize,3))
        self.wholereport_respacc = np.zeros((self.nblocks,self.ntrials_perblock,self.setsize))
        self.wholereport_rts = np.zeros((self.nblocks,self.ntrials_perblock,self.setsize))
        self.wholereport_resp[:] = np.nan
        self.wholereport_resporder[:] = np.nan
        self.wholereport_respcolorind[:] = np.nan
        self.wholereport_resprgb[:] = np.nan
        self.wholereport_respacc[:] = np.nan
        self.wholereport_rts[:] = np.nan

        #counter
        self.counter_trial = np.zeros(self.nblocks+1,dtype=int)

        #experiment parameters
        self.cd_setsize = 6 #1 = repeated images from day 1, 2 = trial unique set size 1 images, 3 = trial unique set size 2 images
        self.cd_same_or_diff = [1, 0]
        self.cd_probe_quad = [1, 2, 3, 4]
        if self.debug:
            self.cd_ntrials_percondition = 1
        else:
            self.cd_ntrials_percondition = 12
        
        #full factorial design
        self.cd_fullfact = hf.fullfact([np.size(self.cd_setsize),np.size(self.cd_same_or_diff),np.size(self.cd_probe_quad),self.cd_ntrials_percondition])
        np.random.shuffle(self.cd_fullfact)
        
        #number of trials within each fully balanced block
        self.cd_ntrials_perblock = np.shape(self.cd_fullfact)[0]
        
        #details on the colors
        self.cd_colors_ind = self.colors_ind
        self.cd_ncolors = self.ncolors
        self.cd_colors_rgb = self.colors_rgb
        
        #possible quadrants 
        self.stim_quad = [1,1,2,2,3,3,4,4]
        
        #Stimulus parameters:
        self.cd_same_probe = np.empty(self.cd_ntrials_perblock,dtype=int)
        self.cd_encarray_colorind = np.empty((self.cd_ntrials_perblock,self.cd_setsize))
        self.cd_encarray_colorrgb = np.empty((self.cd_ntrials_perblock,self.cd_setsize,3))
        self.cd_encarray_quad = np.empty((self.cd_ntrials_perblock,self.cd_setsize))
        self.cd_encarray_r = np.empty((self.cd_ntrials_perblock,self.cd_setsize))
        self.cd_encarray_theta = np.empty((self.cd_ntrials_perblock,self.cd_setsize))
        self.cd_encarray_x = np.empty((self.cd_ntrials_perblock,self.cd_setsize))
        self.cd_encarray_y = np.empty((self.cd_ntrials_perblock,self.cd_setsize))
        self.cd_encarray_mindist = np.empty(self.cd_ntrials_perblock)
        
        #Set stimulus parameters to NaN
        self.cd_encarray_colorind[:] = np.nan
        self.cd_encarray_colorrgb[:] = np.nan
        self.cd_encarray_quad[:] = np.nan
        self.cd_encarray_r[:] = np.nan
        self.cd_encarray_theta[:] = np.nan
        self.cd_encarray_x[:] = np.nan
        self.cd_encarray_y[:] = np.nan
        
        #Probe parameters:
        self.cd_memprobe_ind = np.empty(self.cd_ntrials_perblock,dtype=int)
        self.cd_memprobe_origcolorind = np.empty(self.cd_ntrials_perblock,dtype=int)
        self.cd_memprobe_origcolorrgb = np.empty((self.cd_ntrials_perblock,3),dtype=int)
        self.cd_memprobe_probecolorind= np.empty(self.cd_ntrials_perblock,dtype=int)
        self.cd_memprobe_probecolorrgb= np.empty((self.cd_ntrials_perblock,3),dtype=int)
        self.cd_memprobe_quad = np.empty(self.cd_ntrials_perblock,dtype=int)
        self.cd_memprobe_x = np.empty(self.cd_ntrials_perblock)
        self.cd_memprobe_y = np.empty(self.cd_ntrials_perblock)

        #Response params
        self.cd_correct_response = np.empty(self.cd_ntrials_perblock)
        self.cd_actual_response = np.empty(self.cd_ntrials_perblock)
        self.cd_actual_response_string = ["" for i in range(self.cd_ntrials_perblock)]
        self.cd_acc = np.empty(self.cd_ntrials_perblock,dtype=int)
        self.cd_rt = np.empty(self.cd_ntrials_perblock)
        self.cd_actual_response[:] = np.nan
        self.cd_rt[:] = np.nan
        
        #Randomize things within each block
            
        #whether or not each trial is a change
        self.cd_same_probe[self.cd_fullfact[:,1]==1]=1 #same trials
        self.cd_same_probe[self.cd_fullfact[:,1]==0]=0 #different trials
            
        # correct response for each trial
        self.cd_correct_response[self.cd_same_probe[:]==1]=1 #same trials
        self.cd_correct_response[self.cd_same_probe[:]==0]=0 #different trials  
        
        #calculate the position of each square within the encoding array
        for it in range(self.cd_ntrials_perblock):
            #set size for this trial
            ss = int(self.cd_setsize)
            
            #which quadrant will each square be in (max 2 per quadrant)
            self.cd_encarray_quad[it,0] = self.cd_fullfact[it,2]
            possible_quads = np.append(np.arange(0,4),np.setdiff1d(np.arange(0,4),self.cd_encarray_quad[it,0]))
            self.cd_encarray_quad[it][np.arange(1,ss)] = np.random.choice(possible_quads,ss-1,replace=False)
            
            #calculate the stimulus locations via centroid coordinates
            current_min_dist = 0
            self.cd_stim_mindist=2
            self.cd_rad_min = 1
            self.cd_rad_max = 5
            while current_min_dist<self.cd_stim_mindist:
                
                #polar angle for square position
                r =  self.cd_rad_min + ( self.cd_rad_max - self.cd_rad_min)*np.random.random(ss) #radius of eccentricity for square position
                theta = np.random.random(ss)*90+90*self.cd_encarray_quad[it][np.arange(ss)] #[degrees] for square position
               
                #cartesian coordinates corresponding to polar position for square position
                x, y = tools.coordinatetools.pol2cart(theta,r,units='deg')
                
                #check that they all satisfy min_dist
                current_min_dist = np.min(pdist(np.transpose(np.vstack((x,y)))))
            
            #save the minimum distance for the array
            self.cd_encarray_mindist[it] = current_min_dist
            
            #save the final positions of all blocks in the dat structure
            self.cd_encarray_r[it][np.arange(0,ss)] = r
            self.cd_encarray_theta[it][np.arange(0,ss)] = theta
            self.cd_encarray_x[it][np.arange(0,ss)] = x
            self.cd_encarray_y[it][np.arange(0,ss)] = y
            
        #save details of the probe
        self.cd_memprobe_ind[:] = 0 #index of squares (ranges from 1 to set size of that trial)
        for it in range(self.cd_ntrials_perblock):
            self.cd_memprobe_quad[it] = self.cd_encarray_quad[it][self.cd_memprobe_ind[it]] #quadrant of the probed square
        
        #choose color assignments
        balanced_probe_colors = 0
        while balanced_probe_colors == 0:
            for it in range(self.cd_ntrials_perblock):
                ss = int(self.cd_setsize)
                self.cd_encarray_colorind[it][np.arange(ss)] = np.random.choice(np.arange(self.cd_ncolors),ss,replace=False)
                for iss in range(ss):
                    self.cd_encarray_colorrgb[it][iss] = self.cd_colors_rgb[int(self.cd_encarray_colorind[it][iss])]
                
                    
            #count the number of times each color is probed
            min_num_per_color = np.zeros(self.cd_ncolors,dtype=int)
            for it in range(self.cd_ntrials_perblock):
                min_num_per_color[int(self.cd_encarray_colorind[it][self.cd_memprobe_ind[it]])] = min_num_per_color[int(self.cd_encarray_colorind[it][self.cd_memprobe_ind[it]])] + 1
            
            #make sure that each color is probed at least 3 times per block 
            if np.floor(self.cd_ntrials_perblock/self.cd_ncolors)>6:
                color_thresh = 6
            else:
                color_thresh = np.floor(self.cd_ntrials_perblock/self.cd_ncolors)
            if np.min([min_num_per_color])>=color_thresh:
                balanced_probe_colors = 1
            
        #save more details of the probe
        for it in range(self.cd_ntrials_perblock):
            
            #what color was the probe originally during encoding
            self.cd_memprobe_origcolorind[it] = int(self.cd_encarray_colorind[it][self.cd_memprobe_ind[it]]) #color index of the probed squares
            self.cd_memprobe_origcolorrgb[it] = self.cd_colors_rgb[self.cd_memprobe_origcolorind[it]]
            
            #what color will the probe be at the time of the probe
            if self.cd_same_probe[it]==0: #if the probe is different, select from within the other colors
                self.cd_memprobe_probecolorind[it] = np.random.choice(np.setdiff1d(self.cd_colors_ind,self.cd_memprobe_origcolorind[it]),1,replace=False)
            else:#if the probe is the same, set its color to be the original color
                self.cd_memprobe_probecolorind[it] = self.cd_memprobe_origcolorind[it]
            self.cd_memprobe_probecolorrgb[it] = self.cd_colors_rgb[self.cd_memprobe_probecolorind[it]] #save the probe RGB values
            
            #save the probe's x, y positions 
            self.cd_memprobe_x[it] = self.cd_encarray_x[it][self.cd_memprobe_ind[it]]
            self.cd_memprobe_y[it] = self.cd_encarray_y[it][self.cd_memprobe_ind[it]] 

        #wm timing
        self.t_stim = .8
        self.t_poststim = 1
        self.t_iti = 1

        #Working memory logging timing parameters:
        self.time_blockstart = np.empty(self.nblocks+1)
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

        #change detection timing
        self.cd_t_encarray = .5
        self.cd_t_retinterval = 1
        self.cd_t_itirange = .25
        self.cd_t_itimean = .5
        self.cd_t_iti = np.random.rand(self.cd_ntrials_perblock)*self.cd_t_itirange+self.cd_t_itimean-self.cd_t_itirange/2

        #Timing parameters:
        self.cd_time_blockstart = 0
        self.cd_time_encarray_onset = np.empty(self.cd_ntrials_perblock)
        self.cd_time_encarray_offset = np.empty(self.cd_ntrials_perblock)
        self.cd_time_memprobe_onset = np.empty(self.cd_ntrials_perblock)
        self.cd_time_memprobe_offset = np.empty(self.cd_ntrials_perblock)
        self.cd_time_iti_onset = np.empty(self.cd_ntrials_perblock)
        self.cd_time_iti_offset = np.empty(self.cd_ntrials_perblock)

