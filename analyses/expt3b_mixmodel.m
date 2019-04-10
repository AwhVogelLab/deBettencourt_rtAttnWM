%expt3b_mixmodel.m
%
%this runs mixture modeling for the sustained attention precision 02 dataset
%
%1. First, it runs mixture models for all probe trials for each subject
%2. Then, it runs mixture models for fast & slow trials for each subject
%3. Lastly, it runs mixture models for fast & slow trials using aggregate
%    data from all subjects
%
%Outputs a mat file "mixturemodel" to the results folder, with structs:
%- mixmodel
%- mixmodel_fast
%- mixmodel_slow
%
%MdB, 01/2019

%setpath
addpath(genpath('~/Documents/packages/MemToolbox/'))

%directories
proj_dir = '../expt3b/';
results_dir = [proj_dir 'results/'];

%subjects
subj_name = {'0109191_sustAttnPrecis02','0111191_sustAttnPrecis02',...
            '0111192_sustAttnPrecis02','0111193_sustAttnPrecis02',...
            '0114191_sustAttnPrecis02','0114192_sustAttnPrecis02',...
            '0114193_sustAttnPrecis02','0114194_sustAttnPrecis02',...
            '0116191_sustAttnPrecis02','1212181_sustAttnPrecis02',...
            '1212182_sustAttnPrecis02','1213181_sustAttnPrecis02',...
            '1213182_sustAttnPrecis02','1214181_sustAttnPrecis02',...
            '1214182_sustAttnPrecis02','1214183_sustAttnPrecis02',...
            '1214184_sustAttnPrecis02','1214185_sustAttnPrecis02',...
            '1214186_sustAttnPrecis02','1214187_sustAttnPrecis02',...
            '1214188_sustAttnPrecis02','1218181_sustAttnPrecis02',...
            '1219181_sustAttnPrecis02','1219182_sustAttnPrecis02',...
            };
nsubj = numel(subj_name);


%%

%preallocate empty aggregate variables
aggre_resperror = [];
aggre_resperror_fast = [];
aggre_resperror_slow = [];


for isubj = 1:numel(subj_name)
    
    isubj 
    
    %load the subject csv files
    M = readtable([proj_dir,'/subjects/' subj_name{isubj} '/data/beh/',subj_name{isubj},'_expdat.csv'],'Format','%d%d%d%d%d%d%f%d%d%d%d%f%d%d%d%f%f%f%f%f%f%f%d%f%f%f%f%f%f%f%f%f%f%f%f%f%f');

    %extract the relevant columns from the data
    wm_degdiff =  M.wm_respcolorminusorigcolor;
    probe_trials = M.probe_trials;
    probe_trials_fast = M.fast_rt_trigger;
    probe_trials_slow = M.slow_rt_trigger;

    %select the data from probed trials
    resperror = wm_degdiff(probe_trials==1);
    resperror_fast = wm_degdiff(find(probe_trials_fast)+1);
    resperror_slow = wm_degdiff(find(probe_trials_slow)+1);
    
    resperror_fast = resperror_fast(~isnan(resperror_fast));
    resperror_slow = resperror_slow(~isnan(resperror_slow));

    %aggregate data from this subject
    aggre_resperror = [aggre_resperror;resperror];
    aggre_resperror_fast = [aggre_resperror_fast;resperror_fast];
    aggre_resperror_slow = [aggre_resperror_slow;resperror_slow];
    
    %all probes
    comparefit = MemFit(resperror, {StandardMixtureModel,AllGuessingModel});
    mixmodel.n_trials(isubj) = numel(resperror);
    mixmodel.BIC(isubj,1:2) = comparefit.BIC;
    [~,mixmodel.model_pref(isubj)] = min(comparefit.BIC);
    if mixmodel.model_pref(isubj)==1
        subj_fit = MemFit(resperror, StandardMixtureModel,'Verbosity', 0);
        mixmodel.model_fit(isubj,1:2) = subj_fit.posteriorMean;
    else
        mixmodel.model_fit(isubj,1:2) = NaN;
    end

    %fast triggered probes
    comparefit = MemFit(resperror_fast, {StandardMixtureModel,AllGuessingModel});
    mixmodel_fast.n_trials(isubj) = numel(resperror_fast);
    mixmodel_fast.BIC(isubj,1:2) = comparefit.BIC;
    [~,mixmodel_fast.model_pref(isubj)] = min(comparefit.BIC);
    if mixmodel_fast.model_pref(isubj)==1
        subj_fit = MemFit(resperror_fast, StandardMixtureModel,'Verbosity', 0);
        mixmodel_fast.model_fit(isubj,1:2) = subj_fit.posteriorMean;
    else
        mixmodel_fast.model_fit(isubj,1:2) = NaN;
    end
    
    %slow triggered probes
    comparefit = MemFit(resperror_slow, {StandardMixtureModel,AllGuessingModel});
    mixmodel_slow.n_trials(isubj) = numel(resperror_slow);
    mixmodel_slow.BIC(isubj,1:2) = comparefit.BIC;
    [~,mixmodel_slow.model_pref(isubj)] = min(comparefit.BIC);
    if mixmodel_slow.model_pref(isubj)==1
        subj_fit = MemFit(resperror_slow, StandardMixtureModel,'Verbosity', 0);
        mixmodel_slow.model_fit(isubj,1:2) = subj_fit.posteriorMean;
    else
        mixmodel_slow.model_fit(isubj,1:2) = NaN;
    end
    
end



%% fitting aggregate data from all subjects


temp_fit = MemFit(aggre_resperror_fast, StandardMixtureModel,'Verbosity', 0);
mixmodel_fast.aggre_model_fit = temp_fit.posteriorMean;
mixmodel_fast.aggre_model_lowerCI = temp_fit.lowerCredible;
mixmodel_fast.aggre_model_upperCI = temp_fit.upperCredible;

temp_fit = MemFit(aggre_resperror_slow, StandardMixtureModel,'Verbosity', 0);
mixmodel_slow.aggre_model_fit = temp_fit.posteriorMean;
mixmodel_slow.aggre_model_lowerCI = temp_fit.lowerCredible;
mixmodel_slow.aggre_model_upperCI = temp_fit.upperCredible;


%% save data

save([proj_dir,'/results/mixturemodel.mat'],'mixmodel',...
        'mixmodel_fast','mixmodel_slow','subj_name')



