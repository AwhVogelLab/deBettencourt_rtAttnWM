from __future__ import division
import time, os, platform, math, pickle, sys, types
import numpy as np
from datetime import datetime
if 'psychopy' in sys.modules:
    #import pygame
    from psychopy import visual, core, tools, monitors, gui, event
    import psychopy.event

def get_specs(subj_name='mmddyyn_wmLoadMem02'):
    """Opens a GUI to set up the experiment
    """
    
    dictDlg = gui.DlgFromDict({'Participant number': '121X181_sustAttnPrecis02',     #subject name: month, day, year, number, and project name
                                'Environment':['booth','imac','laptop','Dirk VU','edslab'],    #which environment (aka monitor name in Tools > Monitor Center)
                                'Restarting experiment?':False,     #whether restarting an experiment that was aborted in the middle
                                'Debug':False},
                                title='Welcome to the experiment',  #title for GUI
                                fixed=[' '],
                                order=['Participant number','Environment','Restarting experiment?','Debug']) #choose order of elements
    if dictDlg.OK == True:
        gui_specs = {}
        gui_specs['subj_name']=str(dictDlg.data[0])
        gui_specs['env'] = dictDlg.data[1]
        gui_specs['restarting'] = dictDlg.data[2]
        gui_specs['expt_date'] = datetime.now().strftime("%m/%d/%Y %H:%M")
        gui_specs['debug'] = dictDlg.data[3]
        gui_specs['seed'] = int(time.time())
    else:
        core.quit()
        
    #check the specs
    assert isinstance(gui_specs['subj_name'],basestring), "subj_name is not an string: %r" % specs['subj_name']
    assert isinstance(gui_specs['env'],basestring), "env is not a string: %r" % specs['env']
    assert isinstance(gui_specs['expt_date'],basestring), "expt_date is not a string: %r" % specs['expt_date']
    assert isinstance(gui_specs['seed'],int), "seed is not a int: %r" % specs['seed']

    #which environment is being used to run the experiment
    gui_specs['project_dir']='./../'
        
    #which directory to use to save the data
    gui_specs['save_dir'] = gui_specs['project_dir'] + 'subjects/' + gui_specs['subj_name'] + '/data/beh/'
    
    #if the directory where data will be saved does not exist yet
    if not os.path.isdir(gui_specs['save_dir']):
        print "saving files to: ", gui_specs['save_dir']
        os.makedirs(gui_specs['save_dir']) #this command can make multiple subfolders
        
    return gui_specs

def openorcreate_designfile(gui_specs):

    filename_expdat = gui_specs['save_dir'] + gui_specs['subj_name'] + '_expdat.p'
    filename_expdesign = gui_specs['save_dir']+ gui_specs['subj_name'] + '_expdesign.p'
    if os.path.isfile(filename_expdat):
        expt_design = pickle.load( open( filename_expdat, "rb" ) )
    elif os.path.isfile(filename_expdesign):
        expt_design = pickle.load( open( filename_expdesign, "rb" ) )
    else:
        expt_design = settings.ExperimentalDesign(gui_specs)

    #overwrite the specs to match what you specified in the gui for this time
    expt_design.restarting = gui_specs['restarting']
    expt_design.env = gui_specs['env']
    expt_design.exptDate = gui_specs['expt_date']
    expt_design.debug = gui_specs['debug']

    return expt_design

def angle_diff(t1, t2):
    t1r = np.radians(t1)
    t2r = np.radians(t2)
    
    x = np.cos(t1r-t2r)
    y = np.sin(t1r-t2r)
    dr = np.arctan2(y,x)
    return np.degrees(dr) 


def wait_for_response(win,keylist=None,f=None):
    event.clearEvents(eventType='keyboard')
    if keylist == None:
        keys = psychopy.event.waitKeys()
    else:
        keys = psychopy.event.waitKeys(keyList=keylist)
    if keys[0] == 'escape':
        if f is not None: f.close()
        win.close()
        core.quit()
    response = keys[0]
                    
    return response

def poll_for_response(win,keylist=None,f=None):
    if keylist is not None:
        keys = psychopy.event.getKeys(keyList=keylist)
    else:
        keys = psychopy.event.getKeys()
    if np.size(keys)>0:# is not None:
        if keys[0] == 'escape':
            if f is not None: f.close()
            win.close()
            core.quit()
        response = keys[0]
    else:
        response = None
                    
    return response
   
def drawpath(expt_display,n_circles,i_fill=None):
    
    # draw the circle that indicates the start of experiment
    expt_display.start_circle.draw()
    expt_display.start_text.draw()
    
    # draw the star that indicates the end of experiment
    expt_display.finish_star.draw()
    expt_display.finish_text.draw()
    
    # center of all the circles
    circle_centerX = np.linspace(-3.5,3.5,n_circles)
    
    # draw each circle
    for i in range(n_circles):
        x = circle_centerX[i]
        y = -6  #np.sin(2*np.pi*(i/nCircles))-6
        expt_display.block_outter.fillColor = (-1,-1+2*(i/n_circles),0)
        expt_display.block_outter.pos = (x,y)
        expt_display.block_outter.draw()
        expt_display.block_inner.pos = (x,y)
        if i_fill is not None:
            if i<=i_fill:
                expt_display.block_inner.fillColor= (-1,-1+2*(i/n_circles),0)
            else:
                expt_display.block_inner.fillColor= expt_display.scrcolor
        else:
            expt_display.block_inner.fillColor= expt_display.scrcolor
        expt_display.block_inner.draw()
    

def open_csv_data_file(gui_specs,data_filename,overwrite_ok=None):
    """Opens the csv file and writes the header.
    Parameters:
        - gui_specs: all the selections from the gui at the start of the experiment
        - filename: the name of the CSV file (without the .csv)
    """
    
    #if the filename has .csv delete it
    if data_filename[-4:] == '.csv':
        data_filename = data_filename[:-4]
    
    #add the path to the file name
    data_filename = gui_specs['save_dir'] + data_filename + '.csv'
    
    #open the csv file
    data_file = open(data_filename, 'a')
    
    return data_file

def open_csv_info_file(gui_specs,data_filename):

    #if the filename has .csv delete it
    if data_filename[-4:] == '.csv':
        data_filename = data_filename[:-4]
    
    #add the path to the file name
    data_filename = gui_specs['save_dir'] + data_filename + '.csv'

    #open the csv file
    data_file = open(data_filename, 'a')

    #write all the header information
    for key, value in gui_specs.iteritems():
        data_file.write('"')
        data_file.write(key)
        data_file.write(',')
        data_file.write(str(value))
        data_file.write('"')
        data_file.write('\n')
    data_file.write('\n')

def write_to_csv_data_file(data_file,iblock,itrial,dsgn,headerLine=False):
    if headerLine:
        data_file.write('block,trial,time,setsize,freqtrials,'+
                        'trials_colorind,trials_colordeg,colorrgb0,colorrgb1,colorrgb2,'+
                        'correct_response,actual_response,acc,rts,'+
                        'probe_trials,rt_triggered_fast,rt_triggered_slow,'+
                        'rt_strailingavg,rts_runningavg,rts_runningstd,rts_runningslowthresh,rts_runningfastthresh,'+
                        'wm_respdeg,wm_respind,wm_resprgb0,wm_resprgb1,wm_resprgb2,'+
                        'wm_respcolorminusorigcolor,wm_rts,'+
                        'time_blockstart,time_encarray_onset,time_response,'+
                        'time_encarray_offest,time_memprobe_onset,time_memprobe_offset\n')
    else:
        data_file.write(str(iblock) +','+ str(itrial) +','+ 
                        datetime.utcnow().strftime("%M%S") +','+ 
                        str(dsgn.setsize) +','+ str(dsgn.freq_trials[iblock,itrial]) +','+ 
                        str(dsgn.trials_colorind[iblock,itrial][0]) +','+
                        str(dsgn.trials_colordeg[iblock,itrial][0]) +','+ 
                        str(dsgn.trials_colorrgb[iblock,itrial][0,0]) +','+
                        str(dsgn.trials_colorrgb[iblock,itrial][0,1]) +','+
                        str(dsgn.trials_colorrgb[iblock,itrial][0,2]) +','+
                        str(dsgn.correct_response[iblock,itrial]) +','+ 
                        str(dsgn.actual_response[iblock,itrial]) +','+ 
                        str(dsgn.acc[iblock,itrial]) +','+ 
                        str(dsgn.rts[iblock,itrial]) +','+ 
                        str(dsgn.probe_trials[iblock,itrial]) +','+ 
                        str(dsgn.rt_triggered_fast[iblock,itrial]) +','+ 
                        str(dsgn.rt_triggered_slow[iblock,itrial]) +','+ 
                        str(dsgn.rts_trailingavg[iblock,itrial]) +','+ 
                        str(dsgn.rts_runningavg[iblock,itrial]) +','+ 
                        str(dsgn.rts_runningstd[iblock,itrial]) +','+ 
                        str(dsgn.rts_runningslowthresh[iblock,itrial]) +','+ 
                        str(dsgn.rts_runningfastthresh[iblock,itrial]) +','+
                        str(dsgn.wm_respdeg[iblock,itrial]) +','+ 
                        str(dsgn.wm_respind[iblock,itrial]) +','+ 
                        str(dsgn.wm_resprgb[iblock,itrial][0]) +','+ 
                        str(dsgn.wm_resprgb[iblock,itrial][1]) +','+ 
                        str(dsgn.wm_resprgb[iblock,itrial][2]) +','+ 
                        str(dsgn.wm_respcolorminusorigcolor[iblock,itrial]) +','+ 
                        str(dsgn.wm_rts[iblock,itrial][0]) +','+ 
                        str(dsgn.time_blockstart[iblock]) +','+ 
                        str(dsgn.time_encarray_onset[iblock,itrial]) +','+ 
                        str(dsgn.time_response[iblock,itrial]) +','+ 
                        str(dsgn.time_encarray_offset[iblock,itrial]) +','+ 
                        str(dsgn.time_memprobe_onset[iblock,itrial]) +','+
                        str(dsgn.time_memprobe_offset[iblock,itrial])
                        )
        data_file.flush()
        data_file.write('\n')


def write_to_csv_data_file_cd(data_file,iblock,itrial,dsgn,headerLine=False):
    if headerLine:
        data_file.write('blockNum,trialNum,time,setSize,sameProbe,encArrayColorInd,encArrayQuad,encArrayMinDist,' +
                        'memProbeInd,memProbeOrigColorInd,memProbeOrigColorRGB,memProbeProbeColorInd,memPRobeProbeColorRGB,memProbeQuad,memProbeX,memProbeY' +
                        'corrResp,actualResp,actualRespString,acc,RT,' +
                        'timeBlockStart,timeEncArrayOnset,timeEncArrayOffset,timeMemProbeOnset,timeMemProbeOffset\n')
    else:
        data_file.write(str(iblock) + ','+ str(itrial) + ',' + datetime.utcnow().strftime("%H:%M:%S:%f") + ',' + str(dsgn.cd_setsize) +',' + str(dsgn.cd_same_probe[itrial]) + ',' + str(dsgn.cd_encarray_colorind[itrial]) + ',' + str(dsgn.cd_encarray_quad[itrial]) + ',' +str(dsgn.cd_encarray_mindist[itrial]) + ',' +str(dsgn.cd_memprobe_ind[itrial])+','+str(dsgn.cd_memprobe_origcolorind[itrial]) + ',' +str(dsgn.cd_memprobe_probecolorind[itrial]) + ',' + str(dsgn.cd_memprobe_probecolorrgb[itrial]) + ',' + str(dsgn.cd_memprobe_quad[itrial]) + ',' + str(dsgn.cd_memprobe_x[itrial]) + ',' + str(dsgn.cd_memprobe_y[itrial]) + ',' +str(dsgn.cd_correct_response[itrial]) + ',' + str(dsgn.cd_actual_response[itrial]) + ',' + dsgn.cd_actual_response_string[itrial] + ',' +str(dsgn.cd_acc[itrial]) + ',' + str(dsgn.cd_rt[itrial]) + ',' + str(dsgn.cd_time_blockstart) + ',' + str(dsgn.cd_time_encarray_onset[itrial]) + ',' +str(dsgn.cd_time_encarray_offset[itrial]) + ',' + str(dsgn.cd_time_memprobe_onset[itrial]) + ',' + str(dsgn.cd_time_memprobe_offset[itrial]))
        data_file.flush()
        data_file.write('\n')

def fullfact(levels):
    """
        Create a general full-factorial design
        
        Parameters
        ----------
        levels : array-like
        An array of integers that indicate the number of levels of each input
        design factor.
        
        Returns
        -------
        mat : 2d-array
        The design matrix with coded levels 0 to k-1 for a k-level factor
        
        Example
        -------
        ::
        
        >>> fullfact([2, 4, 3])
        array([[ 0.,  0.,  0.],
        [ 1.,  0.,  0.],
        [ 0.,  1.,  0.],
        [ 1.,  1.,  0.],
        [ 0.,  2.,  0.],
        [ 1.,  2.,  0.],
        [ 0.,  3.,  0.],
        [ 1.,  3.,  0.],
        [ 0.,  0.,  1.],
        [ 1.,  0.,  1.],
        [ 0.,  1.,  1.],
        [ 1.,  1.,  1.],
        [ 0.,  2.,  1.],
        [ 1.,  2.,  1.],
        [ 0.,  3.,  1.],
        [ 1.,  3.,  1.],
        [ 0.,  0.,  2.],
        [ 1.,  0.,  2.],
        [ 0.,  1.,  2.],
        [ 1.,  1.,  2.],
        [ 0.,  2.,  2.],
        [ 1.,  2.,  2.],
        [ 0.,  3.,  2.],
        [ 1.,  3.,  2.]])
        
        """
    n = len(levels)  # number of factors
    nb_lines = np.prod(levels)  # number of trial conditions
    H = np.zeros((nb_lines, n))
    
    level_repeat = 1
    range_repeat = np.prod(levels)
    for i in range(n):
        range_repeat //= levels[i]
        lvl = []
        for j in range(levels[i]):
            lvl += [j]*level_repeat
        rng = lvl*range_repeat
        level_repeat *= levels[i]
        H[:, i] = rng
    
    return H
