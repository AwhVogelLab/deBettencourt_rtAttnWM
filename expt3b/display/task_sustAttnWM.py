import sys
if 'psychopy' in sys.modules:
    from psychopy import visual, core, tools, event, monitors
from helper_functions_sustAttnWM import *
import numpy as np
from pylink import *
from scipy.spatial.distance import pdist
#from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy

#all the data files 
class Task(object):

    def __init__(self,expt_design,expt_display):

        self.dsgn = expt_design
        self.disp = expt_display  

    def welcomeToExperiment(self,f=None):

        self.disp.text_welcome.draw()           #welcome text at top of screen
        self.disp.text_advance.draw()           #advance text at bottom of screen
        self.disp.fix.draw()
        drawpath(self.disp,self.dsgn.nblocks)   #draw the path of the experiment
        self.disp.win.flip()                    #flip the window
        
        #if not self.dsgn.debug:
        wait_for_response(self.disp.win,keylist=self.dsgn.key_advance+self.dsgn.key_escape,f=f)
        self.disp.fix.draw()
        self.disp.win.flip()
        core.wait(.5)

    def instructionsSustAttn(self,clock,f=None):

        #INSTRUCTIONS
        self.disp.text_instructions = visual.TextStim(self.disp.win, 
            text="Every second, shapes will briefly appear. You should press the d key using the left pointer finger when the shapes are circles, like below",
                alignHoriz='center',wrapWidth=22,height=.75,pos=(0,7),color=(-1,-1,-1),
                fontFiles=[self.dsgn.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.disp.text_instructions.draw()     #instructions text at top of screen
        self.disp.fix.draw()
        self.disp.text_advance.pos = (0,-6)
        self.disp.text_advance.draw()           #advance text at bottom of screen

        #set up the rgb vales for each trial, for each circle
        instruct_colorrgb = self.dsgn.rgb_circlepts[int(np.random.choice(100,size=1))*5]

        #draw the stimuli (circles)
        self.disp.fix.fillColor = (-1,-1,-1)
        self.disp.fix.draw()
        for i in range(self.dsgn.setsize):
            self.disp.circle.fillColor = instruct_colorrgb
            self.disp.circle.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
            self.disp.circle.draw()           
        self.disp.win.flip()
        
        #wait for the advance button press
        wait_for_response(self.disp.win,keylist=self.dsgn.key_advance+self.dsgn.key_escape,f=f)

        #blank screen
        self.disp.fix.draw()
        self.disp.win.flip()
        core.wait(.5)

        #INSTRUCTIONS #2
        self.disp.text_instructions = visual.TextStim(self.disp.win, 
                text="Sometimes, squares will appear instead of circles. "+
                "Press the s key when squares appear using your left middle finger.",               
                alignHoriz='center',wrapWidth=22,height=.75,pos=(0,7),color=(-1,-1,-1),
                fontFiles=[self.dsgn.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.disp.text_instructions.draw()     #instructions text at top of screen
        self.disp.fix.draw()
        self.disp.text_advance.pos = (0,-6)
        self.disp.text_advance.draw()           #advance text at bottom of screen
        
        instruct_colorrgb = self.dsgn.rgb_circlepts[int(np.random.choice(100,size=1))*5]

        #draw the stimuli (squares)
        self.disp.fix.fillColor = (-1,-1,-1)
        self.disp.fix.draw()
        for i in range(self.dsgn.setsize):
            self.disp.square.fillColor = instruct_colorrgb
            self.disp.square.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
            self.disp.square.draw()         
        self.disp.win.flip()
        
        #wait for the advance button press
        wait_for_response(self.disp.win,keylist=self.dsgn.key_advance+self.dsgn.key_escape,f=f)   

        #blank screen
        self.disp.fix.draw()
        self.disp.win.flip()
        core.wait(.5)
        
        #INSTRUCTIONS #3
        self.disp.text_instructions = visual.TextStim(self.disp.win, 
            text="Press s for squares and d for circles. Let's practice this now. Get ready, because these shapes come quickly.\n\nPlease look at the black dot in the middle the whole time",
            alignHoriz='center',wrapWidth=22,height=.75,pos=(0,7),color=(-1,-1,-1),
            fontFiles=[self.dsgn.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.disp.text_instructions.draw()
        self.disp.fix.draw()
        self.disp.text_advance.draw()
        self.disp.win.flip() 

        #wait for the advance button press
        response = wait_for_response(self.disp.win,keylist=self.dsgn.key_advance+self.dsgn.key_escape+self.dsgn.key_skip,f=f)       

        #blank screen
        self.disp.fix.draw()
        self.disp.win.flip() 
        core.wait(.5)

        #SUSTAINED ATTENTION PRACTICE BLOCK
        npracticetrials = 10 #number of practice trial
        acc = np.zeros(npracticetrials)

        while True:

            #if they press skip
            if response==self.dsgn.key_skip[0]:
                break
            
            #preallocate
            practicetrials_colorind = np.zeros((npracticetrials),dtype=int)
            practicetrials_colorind = (np.random.choice(npracticetrials,size=npracticetrials,replace=False)*50)
            practicetrials_colorrgb = np.zeros((npracticetrials,self.dsgn.setsize,3))
            actual_response = np.zeros((npracticetrials))
            correct_response = [1,1,1,0,1,1,1,0,1,1]

            #loop through each trial
            for itrial in range(npracticetrials):

                #draw each stimuli
                self.disp.fix.fillColor = (-1,-1,-1)
                self.disp.fix.draw()
                if itrial==3 or itrial==7:
                    for i in range(self.dsgn.setsize):
                        self.disp.square.fillColor = self.dsgn.rgb_circlepts[practicetrials_colorind[itrial]]#practicetrials_colorrgb[itrial,0]
                        self.disp.square.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
                        self.disp.square.draw() 
                else:
                    for i in range(self.dsgn.setsize):
                        self.disp.circle.fillColor = self.dsgn.rgb_circlepts[practicetrials_colorind[itrial]]#practicetrials_colorrgb[itrial,0]
                        self.disp.circle.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
                        self.disp.circle.draw()           
                self.disp.win.flip()
                practicetrial_encarray_onset = clock.getTime() #time of flip
                 
                #response for each stimuli
                response = None
                stim_off = 0
                draw_resp = 0
                event.clearEvents(eventType='keyboard')
                while clock.getTime()<(practicetrial_encarray_onset+self.dsgn.t_enc):
                    if response is None:
                        response = poll_for_response(self.disp.win,self.dsgn.key_freq+self.dsgn.key_infreq+self.dsgn.key_escape)
                        if response is not None:
                            if response==self.dsgn.key_freq[0]:
                                actual_response[itrial]=1
                                draw_resp = 1
                            elif response==self.dsgn.key_infreq[0]:
                                actual_response[itrial]=0
                                draw_resp = 1
                            acc[itrial]=(correct_response[itrial]==actual_response[itrial])*1
                    
                    if draw_resp == 1:
                        self.disp.fix.fillColor = (1,1,1)
                        if stim_off == 0:
                            #draw stimuli
                            if itrial==3 or itrial==7:
                                for i in range(self.dsgn.setsize):
                                    self.disp.square.fillColor = self.dsgn.rgb_circlepts[practicetrials_colorind[itrial]]#practicetrials_colorrgb[itrial,0]
                                    self.disp.square.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
                                    self.disp.square.draw() 
                            else:
                                for i in range(self.dsgn.setsize):
                                    self.disp.circle.fillColor = self.dsgn.rgb_circlepts[practicetrials_colorind[itrial]]#practicetrials_colorrgb[itrial,0]
                                    self.disp.circle.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
                                    self.disp.circle.draw()  
                        self.disp.fix.draw()
                        self.disp.win.flip()
                        draw_resp=0
                            
                    if clock.getTime()>(practicetrial_encarray_onset+self.dsgn.t_stim-.5/120): #draw blank ISI
                        if stim_off == 0:
                            self.disp.fix.draw()
                            self.disp.win.flip()
                            time_stim_offset = clock.getTime()
                            stim_off = 1

            #blank screen
            self.disp.fix.fillColor = (-1,-1,-1)
            self.disp.fix.draw()
            self.disp.win.flip() 
            core.wait(.5)

            #display accuracy
            if np.mean(acc)>=.9: 
                self.disp.text_instructions = visual.TextStim(self.disp.win, 
                    text="You got " + str(int(np.round(np.mean(acc),decimals=2)*100)) + " percent correct. " +
                    "Great job!",
                    alignHoriz='center',wrapWidth=22,height=.75,pos=(0,7),color=(-1,-1,-1),
                    fontFiles=[self.dsgn.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
                self.disp.text_instructions.draw()     #instructions text at top of screen
                self.disp.fix.draw()
                self.disp.text_advance.draw()           #advance text at bottom of screen
                self.disp.win.flip()             
            else:
                self.disp.text_instructions = visual.TextStim(self.disp.win, 
                    text="You got " + str(int(np.round(np.mean(acc),decimals=2)*100)) + " percent correct. " +
                    "Let's try that again. Remember to press d for circles, s for squares",
                    alignHoriz='center',wrapWidth=22,height=.75,pos=(0,7),color=(-1,-1,-1),
                    fontFiles=[self.dsgn.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
                self.disp.text_instructions.draw()     #instructions text at top of screen
                self.disp.fix.draw()
                self.disp.text_advance.draw()           #advance text at bottom of screen
                self.disp.win.flip()       
            
            #wait for advance button press
            response = wait_for_response(self.disp.win,keylist=self.dsgn.key_advance+self.dsgn.key_escape+self.dsgn.key_skip,f=f)     

            #loop until accuracy > 90%
            if np.mean(acc)>=.9:
                break
            else:
                acc = np.zeros(npracticetrials)
            self.disp.fix.draw()
            self.disp.win.flip() 
            core.wait(.5)

    def instructionsWholeReport(self,clock,f=None):

        self.disp.text_instructions = visual.TextStim(self.disp.win, 
            text="Sometimes, the whole screen will go blank and grey. Then, a color wheel like the one below will appear.\n\n" +
            "You will use your mouse to click the color on the wheel that was closest to the color of the last array of shapes before they got jumbled.",
            alignHoriz='center',wrapWidth=22,height=.75,pos=(0,7),color=(-1,-1,-1),
            fontFiles=[self.dsgn.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.disp.text_instructions.draw()     #instructions text at top of screen
        self.disp.fix.draw()
        self.disp.text_advance.draw()           #advance text at bottom of screen 
        self.disp.colorcirc.draw()
        self.disp.win.flip() 
        response = wait_for_response(self.disp.win,keylist=self.dsgn.key_advance+self.dsgn.key_escape,f=f)       
        
        self.disp.fix.draw()
        self.disp.win.flip() 
        core.wait(.5)

        while True:

            self.disp.text_instructions = visual.TextStim(self.disp.win, 
                text="Let's practice just this color wheel task now. Please try to respond as quickly and as accurately as possible." +
                "Don't agonize too much over your decision, but try to go with gut feeling and just try your best!",
                alignHoriz='center',wrapWidth=22,height=.75,pos=(0,7),color=(-1,-1,-1),
                fontFiles=[self.dsgn.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
            self.disp.text_instructions.draw()      #instructions text at top of screen
            self.disp.fix.draw()
            self.disp.text_advance.draw()           #advance text at bottom of screen
            self.disp.win.flip() 
            wait_for_response(self.disp.win,keylist=self.dsgn.key_advance+self.dsgn.key_escape,f=f)  
                  
            self.disp.fix.draw()
            self.disp.win.flip() 
            core.wait(.5)

            practicetrials_colorind = np.random.choice(self.dsgn.n)

            #set up the rgb vales for each trial
            practicetrials_colorrgb = self.dsgn.rgb_circlepts[practicetrials_colorind]

            #draw the squares
            self.disp.fix.fillColor = (-1,-1,-1)
            self.disp.fix.draw()
            for i in range(self.dsgn.setsize):
                self.disp.circle.fillColor = practicetrials_colorrgb
                self.disp.circle.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
                self.disp.circle.draw()
            self.disp.win.flip()
            core.wait(self.dsgn.t_enc)
            
            self.disp.fix.draw() 
            self.disp.win.flip()
            core.wait(self.dsgn.t_poststim+self.dsgn.t_isi)
            
            #draw response screen
            self.disp.fix.draw()
            self.disp.colorcirc.ori = 0
            self.disp.colorcirc.draw()
            self.disp.fix.draw()
            self.disp.win.flip()

            #display mouse at fixation
            self.disp.mouse.setPos(newPos=(0,0))
            self.disp.mouse.setVisible(1)

            responded = 0
            while responded==0:
                if self.disp.mouse.isPressedIn(self.disp.colorcirc,buttons=[0]):
                    #log the time that they responded to that item
                    responded = 1
                    respx,respy = self.disp.mouse.getPos()
                    wm_respdeg, resprad = tools.coordinatetools.cart2pol(respx, respy, units='deg')
                    wm_respdeg_in_colorspace = (-1*angle_diff(wm_respdeg,90) + 360) % 360
                    responded=1  
            enc_array_color_angle = float(practicetrials_colorind)/self.dsgn.n*360
            wm_respcolorminusorigcolor = angle_diff(wm_respdeg_in_colorspace, enc_array_color_angle)
            acc=wm_respcolorminusorigcolor
                    

            #remove memory probe after last response
            self.disp.fix.draw()
            self.disp.win.flip()
            self.disp.mouse.setVisible(0)

            self.disp.text_instructions = visual.TextStim(self.disp.win, 
                text="You were " + str(np.abs(int(acc))) + " degrees off target.\n\n" +
                #"Anything within 40 degress is close to the target.\n\n" +
                "Press r to repeat this if you want more practice.",
                alignHoriz='center',wrapWidth=22,height=.75,pos=(0,7),color=(-1,-1,-1),
                fontFiles=[self.dsgn.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
            self.disp.text_instructions.draw()     #instructions text at top of screen
            self.disp.fix.draw()
            self.disp.text_advance.draw()           #advance text at bottom of screen
            self.disp.win.flip() 
            response = wait_for_response(self.disp.win,keylist=self.dsgn.key_advance+self.dsgn.key_escape+self.dsgn.key_repeat+self.dsgn.key_skip,f=f)  

            if response==self.dsgn.key_skip[0] or response=='space':
                break

            self.disp.fix.draw()
            self.disp.win.flip() 
            core.wait(.5)

    def instructionsBoth(self,clock,f=None):

        while True:
            self.disp.text_instructions = visual.TextStim(self.disp.win, 
                text="Now let's try both tasks together. Remember, for the main task, press d for circles, s for squares.\n\n" + 
                "Then, when the color wheel appears, use the mouse to click what the colors of the shapes immediately before had been.",
                alignHoriz='center',wrapWidth=22,height=.75,pos=(0,7),color=(-1,-1,-1),
                fontFiles=[self.dsgn.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
            self.disp.text_instructions.draw()      #instructions text at top of screen
            self.disp.fix.draw()
            self.disp.text_advance.draw()           #advance text at bottom of screen
            self.disp.win.flip() 
            response = wait_for_response(self.disp.win,keylist=self.dsgn.key_advance+self.dsgn.key_escape+self.dsgn.key_skip,f=f)  
            
            if response == self.dsgn.key_skip[0]:
                break

            self.disp.fix.draw()
            self.disp.win.flip() 
            core.wait(.5)        

            npracticetrials = 10
            acc = np.zeros(npracticetrials)       
            practicetrials_colorind = np.zeros((npracticetrials),dtype=int)
            practicetrials_colorind = (np.random.choice(npracticetrials,size=npracticetrials,replace=False)*50)
            practicetrials_colorrgb = np.zeros((npracticetrials,3))
            actual_response = np.zeros((npracticetrials))
            correct_response = [1,1,0,1,1,1,1,1,0,1]


            for itrial in range(npracticetrials):
                #set up the rgb vales for each trial
                practicetrials_colorrgb[itrial] = self.dsgn.rgb_circlepts[int(practicetrials_colorind[itrial])]

            for itrial in range(npracticetrials):
                self.disp.fix.fillColor = (-1,-1,-1)
                self.disp.fix.draw()
                if itrial==2 or itrial==8:
                    for i in range(self.dsgn.setsize):
                        self.disp.square.fillColor = practicetrials_colorrgb[itrial]
                        self.disp.square.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
                        self.disp.square.draw() 
                else:
                    for i in range(self.dsgn.setsize):
                        self.disp.circle.fillColor = practicetrials_colorrgb[itrial]
                        self.disp.circle.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
                        self.disp.circle.draw()           
                self.disp.win.flip()

                #save timing information
                practicetrial_encarray_onset = clock.getTime()

                #response for each stimuli
                response = None
                stim_off = 0
                draw_resp = 0
                event.clearEvents(eventType='keyboard')
                while clock.getTime()<(practicetrial_encarray_onset+self.dsgn.t_enc):
                    if response is None:
                        response = poll_for_response(self.disp.win,self.dsgn.key_freq+self.dsgn.key_infreq+self.dsgn.key_escape)
                        if response is not None:
                            if response==self.dsgn.key_freq[0]:
                                actual_response[itrial]=1
                                draw_resp = 1
                            elif response==self.dsgn.key_infreq[0]:
                                actual_response[itrial]=0
                                draw_resp = 1
                            acc[itrial]=(correct_response[itrial]==actual_response[itrial])*1
                    
                    if draw_resp == 1:
                        self.disp.fix.fillColor = (1,1,1)
                        if stim_off == 0:
                            #draw stimuli
                            if itrial==2 or itrial==8:
                                for i in range(self.dsgn.setsize):
                                    self.disp.square.fillColor = self.dsgn.rgb_circlepts[practicetrials_colorind[itrial]]#practicetrials_colorrgb[itrial,0]
                                    self.disp.square.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
                                    self.disp.square.draw() 
                            else:
                                for i in range(self.dsgn.setsize):
                                    self.disp.circle.fillColor = self.dsgn.rgb_circlepts[practicetrials_colorind[itrial]]#practicetrials_colorrgb[itrial,0]
                                    self.disp.circle.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
                                    self.disp.circle.draw()  
                        self.disp.fix.draw()
                        self.disp.win.flip()
                        draw_resp=0
                            
                    if clock.getTime()>(practicetrial_encarray_onset+self.dsgn.t_stim-.5/120): #draw blank ISI
                        if stim_off == 0:
                            self.disp.fix.draw()
                            self.disp.win.flip()
                            time_stim_offset = clock.getTime()
                            stim_off = 1
                            
                if itrial==7:
                    self.disp.fix.fillColor = (-1,-1,-1)
                    self.disp.fix.draw() 
                    self.disp.win.flip()
                    core.wait(self.dsgn.t_poststim)
                    
                    #draw response screen
                    self.disp.fix.draw()
                    self.disp.colorcirc.ori = 0# + self.dsgn.wm_colorwheel_shift[iblock,itrial]
                    self.disp.colorcirc.draw()
                    self.disp.win.flip()
                    
                    #display mouse at fixation
                    self.disp.mouse.setPos(newPos=(0,0))
                    self.disp.mouse.setVisible(1)
                    
                    count = 0
                    responded = 0
                    while responded==0:
                        if self.disp.mouse.isPressedIn(self.disp.colorcirc,buttons=[0]):
                            #log the time that they responded to that item
                            respx,respy = self.disp.mouse.getPos()
                            wm_respdeg, resprad = tools.coordinatetools.cart2pol(respx, respy, units='deg')
                            wm_respdeg_in_colorspace = (-1*angle_diff(wm_respdeg,90) + 360) % 360
                            responded=1
                    
                    enc_array_color_angle = float(practicetrials_colorind[itrial])/self.dsgn.n*360
                    wm_respcolorminusorigcolor = angle_diff(wm_respdeg_in_colorspace, enc_array_color_angle)
                    wholereportacc=wm_respcolorminusorigcolor

                    #remove memory probe after response
                    self.disp.fix.draw()
                    self.disp.win.flip()
                    self.disp.mouse.setVisible(0)
                    core.wait(self.dsgn.t_iti)
            
            self.disp.fix.draw()
            self.disp.win.flip() 
            core.wait(.5)   

            self.disp.text_instructions = visual.TextStim(self.disp.win, 
                text="On the main task, you got " + str(int(np.round(np.mean(acc),decimals=2)*100)) + " percent correct\n\n" + 
                "On the mouse clicking, you were " + str(np.abs(int(wholereportacc))) + " degrees away from the target.\n\n"+
                "Press r to repeat these trials if you want more practice on both tasks.",
                alignHoriz='center',wrapWidth=22,height=.75,pos=(0,7),color=(-1,-1,-1),
                fontFiles=[self.dsgn.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
            self.disp.text_instructions.draw()     #instructions text at top of screen
            self.disp.fix.fillColor = (-1,-1,-1)
            self.disp.fix.draw()
            self.disp.text_advance.draw()           #advance text at bottom of screen
            self.disp.win.flip() 
            response = wait_for_response(self.disp.win,keylist=self.dsgn.key_advance+self.dsgn.key_escape+self.dsgn.key_repeat,f=f)  

            self.disp.fix.fillColor = (-1,-1,-1)
            self.disp.fix.draw()
            self.disp.win.flip() 
            core.wait(.5)

            if response == 'space':
                break

        self.disp.text_instructions = visual.TextStim(self.disp.win, 
            text="Please find the experimenter if you have any questions. " + 
                "Otherwise press spacebar to start! Good luck!",
            alignHoriz='center',wrapWidth=22,height=.75,pos=(0,7),color=(-1,-1,-1),
            fontFiles=[self.disp.project_dir + 'display/fonts/Lato-Reg.ttf'],font=['Lato'])
        self.disp.text_instructions.draw()      #instructions text at top of screen
        self.disp.fix.draw()
        self.disp.text_advance.draw()           #advance text at bottom of screen
        self.disp.win.flip() 
        wait_for_response(self.disp.win,keylist=self.dsgn.key_advance+self.dsgn.key_escape,f=f)  
              
        self.disp.fix.draw()
        self.disp.win.flip() 
        core.wait(.5)   

    def startOfBlock(self,iblock,clock,f=None):

        #display the start of block screen
        self.disp.text_block_start.setText('Block ' + str(iblock+1) + ' of ' + str(self.dsgn.nblocks))   #set the block text to be the right block number
        self.disp.text_block_start.draw()                       #draw the block text
        self.disp.fix.fillColor = (-1,-1,-1)
        self.disp.fix.draw()
        drawpath(self.disp,self.dsgn.nblocks,i_fill=iblock-1)   #display progress
        self.disp.text_advance.pos = (0,-4)
        self.disp.text_advance.draw()                           #text advance
        self.disp.win.flip()                                    #flip the window
        
        #wait for the response to start the block
        response = wait_for_response(self.disp.win,keylist=self.dsgn.key_advance+self.dsgn.key_escape,f=f)
        self.dsgn.time_blockstart[iblock]=clock.getTime()


        self.disp.fix.draw()
        self.disp.win.flip()
        core.wait(self.dsgn.t_poststim)
        


    def encodingArray(self,iblock,itrial,clock,f=None):

        #draw stimuli
        self.disp.fix.fillColor = (-1,-1,-1)
        self.disp.fix.draw()
        if self.dsgn.freq_trials[iblock,itrial]==1:
            for i in range(self.dsgn.setsize):
                self.disp.circle.fillColor = self.dsgn.trials_colorrgb[iblock,itrial,i]
                self.disp.circle.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
                self.disp.circle.draw()
        else:
            for i in range(self.dsgn.setsize):
                self.disp.square.fillColor = self.dsgn.trials_colorrgb[iblock,itrial,i]
                self.disp.square.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
                self.disp.square.draw()
        self.disp.win.flip()

        #save timing information
        self.dsgn.time_encarray_onset[iblock,itrial] = clock.getTime()
        
        #wait for response
        response = None
        stim_off = 0
        draw_resp = 0
        event.clearEvents(eventType='keyboard')
        while clock.getTime()<(self.dsgn.time_encarray_onset[iblock,itrial]+self.dsgn.t_enc):
            if response is None:
                response = poll_for_response(self.disp.win,self.dsgn.key_freq+self.dsgn.key_infreq+self.dsgn.key_escape)
                if response is not None:
                    #log time response was made
                    self.dsgn.time_response[iblock,itrial] = clock.getTime()
                    self.dsgn.rts[iblock,itrial] = self.dsgn.time_response[iblock,itrial]-self.dsgn.time_encarray_onset[iblock,itrial]
                    draw_resp = 1
                    
                    #calculate real time details
                    if itrial>=self.dsgn.n_trials_atstart and itrial<self.dsgn.ntrials_perblock-2:
                        self.dsgn.rts_runningavg[iblock,itrial] = np.nanmean(self.dsgn.rts[iblock,0:itrial]) #cumulative running average
                        self.dsgn.rts_runningstd[iblock,itrial] = np.nanstd(self.dsgn.rts[iblock,0:itrial]) #cumulative running standard deviation
                        self.dsgn.rts_runningslowthresh[iblock,itrial] = self.dsgn.rts_runningavg[iblock,itrial]+self.dsgn.rts_runningstd[iblock,itrial] #slow RT threshold
                        self.dsgn.rts_runningfastthresh[iblock,itrial] = self.dsgn.rts_runningavg[iblock,itrial]-self.dsgn.rts_runningstd[iblock,itrial] #fast RT threshold
                        self.dsgn.rts_trailingavg[iblock,itrial] = np.nanmean(self.dsgn.rts[iblock,(itrial-2):(itrial+1)])
                        
                        if np.all(self.dsgn.freq_trials[iblock,(itrial-2):(itrial+1)]==1) and ~np.any(np.isnan(self.dsgn.rts[iblock,(itrial-2):(itrial+1)])) and np.all(self.dsgn.probe_trials[iblock,(itrial-2):(itrial+1)] == 0):

                            if self.dsgn.rts_trailingavg[iblock,itrial]>self.dsgn.rts_runningslowthresh[iblock,itrial] and np.nansum(self.dsgn.rt_triggered_slow[iblock,0:itrial])<self.dsgn.n_rt_triggered_slow:
                                self.dsgn.rt_triggered_slow[iblock,itrial] = 1

                            if self.dsgn.rts_trailingavg[iblock,itrial]<self.dsgn.rts_runningfastthresh[iblock,itrial] and np.nansum(self.dsgn.rt_triggered_fast[iblock,0:itrial])<self.dsgn.n_rt_triggered_fast:
                                self.dsgn.rt_triggered_fast[iblock,itrial] = 1

                        if self.dsgn.rt_triggered_slow[iblock,itrial] == 1 or self.dsgn.rt_triggered_fast[iblock,itrial] == 1:
                            self.dsgn.rt_triggered[iblock,itrial+1] = 1
                            self.dsgn.probe_trials[iblock,itrial+1] = 1
                        
                    #log response that was made
                    self.dsgn.actual_response_string[iblock][itrial] = response[0]
                    if response==self.dsgn.key_freq[0]:
                        self.dsgn.actual_response[iblock,itrial]=1
                    elif response==self.dsgn.key_infreq[0]:
                        self.dsgn.actual_response[iblock,itrial]=0

                    #see if the response was correct or not
                    self.dsgn.acc[iblock,itrial]=(self.dsgn.correct_response[iblock,itrial]==self.dsgn.actual_response[iblock,itrial])*1
                    
                    #if incorrect response, disallow probe
                    if self.dsgn.acc[iblock,itrial]==0:
                        self.dsgn.probe_trials[iblock,itrial] = 0
                        self.dsgn.rt_triggered[iblock,itrial] = 0
                        self.dsgn.rt_triggered_fast[iblock,itrial] = 0
                        self.dsgn.rt_triggered_slow[iblock,itrial] = 0
                    
            if draw_resp == 1:
                self.disp.fix.fillColor = (1,1,1)
                if stim_off == 0:
                    #draw stimuli
                    if self.dsgn.freq_trials[iblock,itrial]==0:
                        for i in range(self.dsgn.setsize):
                            self.disp.square.fillColor = self.dsgn.trials_colorrgb[iblock,itrial,i]
                            self.disp.square.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
                            self.disp.square.draw() 
                    else:
                        for i in range(self.dsgn.setsize):
                            self.disp.circle.fillColor = self.dsgn.trials_colorrgb[iblock,itrial,i]
                            self.disp.circle.pos = (self.dsgn.positions_x[i], self.dsgn.positions_y[i])
                            self.disp.circle.draw()  
                self.disp.fix.draw()
                self.disp.win.flip()
                draw_resp=0
                    
            if clock.getTime()>(self.dsgn.time_encarray_onset[iblock,itrial]+self.dsgn.t_stim-.5/120): #draw blank ISI
                if stim_off == 0:
                    self.disp.fix.draw()
                    self.disp.win.flip()
                    self.dsgn.time_encarray_offset[iblock,itrial] = clock.getTime()
                    stim_off = 1
                            
        if response is None:
            if itrial>=self.dsgn.n_trials_atstart:
                self.dsgn.rts_runningavg[iblock,itrial] = np.nanmean(self.dsgn.rts[iblock,0:itrial])
                self.dsgn.rts_runningstd[iblock,itrial] = np.nanstd(self.dsgn.rts[iblock,0:itrial])
                self.dsgn.rts_runningslowthresh[iblock,(itrial-1):(itrial+1)] = self.dsgn.rts_runningavg[iblock,itrial]+self.dsgn.rts_runningstd[iblock,itrial]
                self.dsgn.rts_runningfastthresh[iblock,(itrial-1):(itrial+1)] = self.dsgn.rts_runningavg[iblock,itrial]-self.dsgn.rts_runningstd[iblock,itrial]
                self.dsgn.rts_trailingavg[iblock,itrial] = np.nanmean(self.dsgn.rts[iblock,(itrial-2):(itrial+1)])
                self.dsgn.probe_trials[iblock,itrial] = 0
                self.dsgn.rt_triggered[iblock,itrial] = 0



    def retentionInterval(self,iblock,itrial,clock):
        self.disp.fix.fillColor = (-1,-1,-1)
        self.disp.fix.draw()
        self.disp.win.flip()

        core.wait(self.dsgn.t_poststim)
        

    def memoryProbe(self,iblock,itrial,clock,f=None):

        def drawEverything():
            self.disp.colorcirc.ori = 0# + self.dsgn.wm_colorwheel_shift[iblock,itrial]
            self.disp.colorcirc.draw()
            self.disp.fix.draw()
            self.disp.win.flip()
            
        
        event.clearEvents('mouse') #Continue until keypress     
        self.disp.mouse.setPos(newPos=(0,0)) #initialize to 0,0
        self.disp.mouse.setVisible(1) #make cursor visible
        
        drawEverything()
        
        flipCount = -1
        while True:

            if event.getKeys(['escape']):
                self.disp.win.close()
                core.wait(.5)
                core.quit()
                
            drawEverything() 
            flipCount = flipCount+1
            if flipCount==0:
                #save timing information
                self.dsgn.time_memprobe_onset[iblock,itrial] = clock.getTime()
            
            if self.disp.mouse.isPressedIn(self.disp.colorcirc,buttons=[0]):
                #if self.disp.innerring!=0 and not self.disp.mouse.isPressedIn(self.disp.innerring):
                self.dsgn.wm_rts[iblock,itrial]=clock.getTime()-self.dsgn.time_memprobe_onset[iblock,itrial]
                respx,respy = self.disp.mouse.getPos()
                self.dsgn.wm_respdeg[iblock,itrial], resprad = tools.coordinatetools.cart2pol(respx, respy, units='deg') # ranges from 0 (horizontal) to -180 (bottom) and +180 (top)

                #convert the degree where the mouse clicked into a color
                self.dsgn.wm_respdeg_in_colorspace[iblock,itrial] = (-1*angle_diff(self.dsgn.wm_respdeg[iblock,itrial],90) + 360) % 360                   # ranges from 0 (vertical) to 360 (90 is right part of circle, 180 is bottom, 270 is left part of circle)
                #deg_shift = (angle_diff(deg_in_colorspace,self.dsgn.wm_colorwheel_shift[iblock,itrial]) + 360) % 360     # accounts for shift
                self.dsgn.wm_respind[iblock,itrial] = np.round(self.disp.colortextureRes/360.0*self.dsgn.wm_respdeg_in_colorspace[iblock,itrial]).astype(int)  # which index of the texture
                if self.dsgn.wm_respind[iblock,itrial]==512:
                    self.dsgn.wm_respind[iblock,itrial]=511
                index=self.dsgn.wm_respind[iblock,itrial].astype(int)
                #print index
                self.dsgn.wm_resprgb[iblock,itrial] = self.disp.colortexrgb[-1,index,:]

                #calculate the angle that the color is 
                enc_array_color_angle = float(self.dsgn.trials_colorind[iblock,itrial][0])/self.dsgn.n*360
                
                #calculate the difference between the two angles
                self.dsgn.wm_respcolorminusorigcolor[iblock,itrial] = angle_diff(self.dsgn.wm_respdeg_in_colorspace[iblock,itrial], enc_array_color_angle)
                
                break
        
        #print self.dsgn.wm_respdeg[iblock,itrial], self.dsgn.wm_respdeg_in_colorspace[iblock,itrial], self.dsgn.trials_colorind[iblock,itrial][0], enc_array_color_angle, self.dsgn.wm_respcolorminusorigcolor[iblock,itrial]
        
        #remove memory probe after response
        self.disp.fix.draw()
        self.disp.win.flip()

        #save timing information
        self.dsgn.time_memprobe_offset[iblock,itrial] = clock.getTime()
        self.disp.mouse.setVisible(0)

    def itiWM(self,iblock,itrial,clock):
        self.disp.fix.draw()
        self.disp.win.flip()

        #save timing information
        self.dsgn.time_iti_onset[iblock,itrial] = clock.getTime()

        core.wait(self.dsgn.t_iti)

        #save timing information
        self.dsgn.time_iti_offset[iblock,itrial] = clock.getTime()

        
    def endOfBlock(self,iblock,clock,f=None):

        #display the start of block screen
        self.disp.text_block_start.setText('Finished block')   #set the block text to be the right block number
        self.disp.text_block_start.draw()
        self.disp.fix.draw()
        drawpath(self.disp,self.dsgn.nblocks,i_fill=iblock-1)   #display progress
        self.disp.text_advance.pos = (0,-4)
        self.disp.text_advance.draw()                           #text advance
        self.disp.win.flip()                                    #flip the window
        
        #wait for the response to start the block
        response = wait_for_response(self.disp.win,keylist=self.dsgn.key_advance+self.dsgn.key_escape,f=f)
        
        self.disp.fix.draw()
        self.disp.win.flip()
        self.dsgn.time_blockend[iblock] = clock.getTime()
        core.wait(.5)


    def endOfExperiment(self,f=None):
        self.disp.text_end_expt.draw()
        self.disp.win.flip()
        keys = event.waitKeys(keyList=['space','escape']) 
        