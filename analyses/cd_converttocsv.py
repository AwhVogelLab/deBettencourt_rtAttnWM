import numpy as np
import os, sys, pickle, csv


def converttocsv(project_name):
    sys.path.append('../' + project_name +'/display')
    import settings_sustAttnWM as dsgn

    subj_name = [f for f in os.listdir('../' + project_name + '/subjects/') if not np.logical_or(f.endswith('EXCLUDED'),f.startswith('.'))]


    for i,isubj in enumerate(subj_name):
        print i,isubj

        with open('../' + project_name + "/subjects/" + isubj + "/data/beh/" + isubj + "_expdat.p",'rb') as f:
            subj_dat=pickle.load(f)

        nt = subj_dat.cd_ntrials_perblock

        #print header line
        header=['cd_trial',
                'cd_same_probe',
                'cd_acc',
                'cd_rt']


        with open("../" + project_name + "/subjects/" + isubj + "/data/beh/" + isubj + "_cd.csv",'wb') as f:
            writer=csv.writer(f,'excel',delimiter=',')

            writer.writerow(header)

            for itrial in range(nt):
                row=[str(itrial+1), #trial
                    str(subj_dat.cd_same_probe[itrial]), 
                    str(subj_dat.cd_acc[itrial]), #correct response 
                    str(subj_dat.cd_rt[itrial])]
                writer.writerow(row)

converttocsv('expt2a')
converttocsv('expt2b')