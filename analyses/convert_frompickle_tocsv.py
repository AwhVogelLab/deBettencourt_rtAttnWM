import numpy as np
import os, sys, pickle, csv


def convert_frompickle_tocsv(project_name):
    sys.path.append('../' + project_name +'/display')
    print('../' + project_name +'/display')
    print(os.listdir('../' + project_name +'/display'))
    import settings_sustAttnWM as dsgn

    subj_name = [f for f in os.listdir('../' + project_name + '/subjects/') if not np.logical_or(f.endswith('EXCLUDED'),f.startswith('.'))]



    for i,isubj in enumerate(subj_name):
        print i,isubj

        with open('../' + project_name + "/subjects/" + isubj + "/data/beh/" + isubj + "_expdat.p",'rb') as f:
            subj_dat=pickle.load(f)

        nb = subj_dat.nblocks
        nt = subj_dat.ntrials_perblock
        setsize = subj_dat.setsize
        #print header line
        header=['block',
                'trial',
                'freq_trials',
                'correct_response',
                'actual_response',
                'acc',
                'rts',
                'probe_trials']

        if (project_name=='expt2a') or (project_name=='expt2b') or (project_name=='expt3a') or (project_name=='expt3b'):
            header.append('fast_rt_trigger')
            header.append('slow_rt_trigger')
            header.append('rt_triggered')
            header.append('rts_runningavg')
            header.append('rts_runningstd')
            header.append('rts_runningfastthresh')
            header.append('rts_runningslowthresh')
            header.append('rts_runningstd')
            header.append('rts_trailingavg')
        if (project_name=='expt2a') or (project_name=='expt2b'):
            for j in range(setsize):
                header.append('trials_colorind' + str(j))
            for j in range(setsize):
                header.append('wholereport_resp' + str(j))
            for j in range(setsize):
                header.append('wholereport_respacc' + str(j))
            header.append('wholereport_respacc_total')
            for j in range(setsize):
                header.append('wholereport_respcolorind' + str(j))
            for j in range(setsize):
                header.append('wholereport_resporder' + str(j))
            for j in range(setsize):
                header.append('wholereport_rts' + str(j))
        else:
            header.append('trials_colorind')
            header.append('trials_colorrgb0')
            header.append('trials_colorrgb1')
            header.append('trials_colorrgb2')
            header.append('wm_respdeg')
            header.append('wm_respdeg_in_colorspace')
            header.append('wm_respcolorminusorigcolor')
            header.append('wm_resptexind')
            header.append('wm_resptexrgb0')
            header.append('wm_resptexrgb1')
            header.append('wm_resptexrgb2')
            header.append('wm_rts')
        header.append('time_blockstart')
        header.append('time_encarray_offset')
        header.append('time_encarray_onset')
        header.append('time_response')
        header.append('time_iti_offset')
        header.append('time_iti_onset')
        header.append('time_memprobe_offset')
        header.append('time_memprobe_onset')


        with open("../" + project_name + "/subjects/" + isubj + "/data/beh/" + isubj + "_expdat.csv",'wb') as f:
            writer=csv.writer(f,'excel',delimiter=',')

            writer.writerow(header)

            for iblock in range(nb):
                for itrial in range(nt):
                    row=[str(iblock+1), #block
                        str(itrial+1), #trial
                        str(subj_dat.freq_trials[iblock,itrial]), #frequent category trials = 1, infrequent = 0
                        str(subj_dat.correct_response[iblock,itrial]), #correct response 
                        str(subj_dat.actual_response[iblock,itrial]), #actual actual 
                        str(subj_dat.acc[iblock,itrial]), #accuracy
                        str(subj_dat.rts[iblock,itrial]), #rts
                        str(subj_dat.probe_trials[iblock,itrial])] #whether the trial was probed
                    if (project_name=='expt2a') or (project_name=='expt2b') or (project_name=='expt3a') or (project_name=='expt3b'):
                        row.append(str(subj_dat.rt_triggered_fast[iblock,itrial]))
                        row.append(str(subj_dat.rt_triggered_slow[iblock,itrial]))
                        row.append(str(subj_dat.rt_triggered[iblock,itrial]))
                        row.append(str(subj_dat.rts_runningavg[iblock,itrial]))
                        row.append(str(subj_dat.rts_runningstd[iblock,itrial]))
                        row.append(str(subj_dat.rts_runningfastthresh[iblock,itrial]))
                        row.append(str(subj_dat.rts_runningslowthresh[iblock,itrial]))
                        row.append(str(subj_dat.rts_runningstd[iblock,itrial]))
                        row.append(str(subj_dat.rts_trailingavg[iblock,itrial]))
                    if (project_name=='expt2a') or (project_name=='expt2b'):
                        for j in range(setsize):
                            row.append(str(subj_dat.trials_colorind[iblock,itrial][j])) #color ind
                        for j in range(setsize):
                            row.append(str(subj_dat.wholereport_resp[iblock,itrial][j])) #whole resp
                        for j in range(setsize):
                            row.append(str(subj_dat.wholereport_respacc[iblock,itrial][j])) #whole resp
                        row.append(str(np.nansum(subj_dat.wholereport_respacc[iblock,itrial]))) #whole acc
                        for j in range(setsize):
                            row.append(str(subj_dat.wholereport_respcolorind[iblock,itrial][j])) #whole colors
                        for j in range(setsize):
                            row.append(str(subj_dat.wholereport_resporder[iblock,itrial][j])) #whole order
                        for j in range(setsize):
                            row.append(str(subj_dat.wholereport_rts[iblock,itrial][j])) #whole rts
                    else:
                        row.append(str(subj_dat.trials_colorind[iblock,itrial,0]))
                        row.append(str(subj_dat.trials_colorrgb[iblock,itrial][0,0]))
                        row.append(str(subj_dat.trials_colorrgb[iblock,itrial][0,1]))
                        row.append(str(subj_dat.trials_colorrgb[iblock,itrial][0,2]))
                        row.append(str(subj_dat.wm_respdeg[iblock,itrial]))
                        row.append(str(subj_dat.wm_respdeg_in_colorspace[iblock,itrial]))
                        row.append(str(subj_dat.wm_respcolorminusorigcolor[iblock,itrial]))
                        if project_name=='expt3b':
                            row.append(str(subj_dat.wm_respind[iblock,itrial]))
                            row.append(str(subj_dat.wm_resprgb[iblock,itrial,0]))
                            row.append(str(subj_dat.wm_resprgb[iblock,itrial,1]))
                            row.append(str(subj_dat.wm_resprgb[iblock,itrial,2]))
                        else:
                            row.append(str(subj_dat.wm_resptexind[iblock,itrial]))
                            row.append(str(subj_dat.wm_resptexrgb[iblock,itrial,0]))
                            row.append(str(subj_dat.wm_resptexrgb[iblock,itrial,1]))
                            row.append(str(subj_dat.wm_resptexrgb[iblock,itrial,2]))
                        row.append(str(subj_dat.wm_rts[iblock,itrial][0]))
                    row.append(str(subj_dat.time_blockstart[iblock]))      #time the block started 
                    row.append(str(subj_dat.time_encarray_onset[iblock,itrial]))  #time the encoding array appeared
                    row.append(str(subj_dat.time_encarray_offset[iblock,itrial])) #time the encoding array disappeared
                    row.append(str(subj_dat.time_response[iblock,itrial]))        #time the sustained attention response was made
                    row.append(str(subj_dat.time_iti_onset[iblock,itrial]))       #time the screen became blank
                    row.append(str(subj_dat.time_iti_offset[iblock,itrial]))       #time the screen stopped being blank
                    row.append(str(subj_dat.time_memprobe_onset[iblock,itrial]))  #time memory probe appeared
                    row.append(str(subj_dat.time_memprobe_offset[iblock,itrial])) #time memory probe disappeared
                    writer.writerow(row)

convert_frompickle_tocsv('expt3b')