%expt3a_mixmodel.m
%
%this runs mixture modeling for the sustained attention precision 01 dataset
%
%1. First, it runs mixture models for all probe trials for each subject
%2. Then, it runs mixture models for fast & slow trials for each subject
%3. Lastly, it runs mixture models for fast & slow trials using aggregate
%    data from all subjects
%
%Outputs a mat file "mixmodel" to the results folder, with structs:
%- mixmodel
%- mixmodel_fast
%- mixmodel_slow
%
%MdB, 09/2018

%setpath
addpath(genpath('~/Documents/packages/MemToolbox/'))

%directories
proj_dir = '/Users/megan/Documents/projects/sustAttnPrecis01';
results_dir = [proj_dir 'results/'];

%subjects
subj_name = {'0918181_sustAttnPrecis01', '0918182_sustAttnPrecis01', '0918183_sustAttnPrecis01',...
    '0918184_sustAttnPrecis01', '0918185_sustAttnPrecis01', '0918186_sustAttnPrecis01', ...
    '0919181_sustAttnPrecis01', '0919182_sustAttnPrecis01', '0919183_sustAttnPrecis01', ...
    '0919184_sustAttnPrecis01', '0919185_sustAttnPrecis01', '0920181_sustAttnPrecis01', ...
    '0920183_sustAttnPrecis01', '0920184_sustAttnPrecis01', '0920185_sustAttnPrecis01', ...
    '0920186_sustAttnPrecis01', '0920187_sustAttnPrecis01', '0920188_sustAttnPrecis01',...
    '0924181_sustAttnPrecis01', '0925181_sustAttnPrecis01','0928182_sustAttnPrecis01', ...
    '0928183_sustAttnPrecis01'};
nsubj = numel(subj_name);


%%

%preallocate empty aggregate variables
aggre_resperror = [];
aggre_resperror_fast = [];
aggre_resperror_slow = [];


for isubj = 1:numel(subj_name)
    
    isubj 
    
    %load the subject csv files
    M = readtable([proj_dir,'/subjects/' subj_name{isubj} '/data/beh/',subj_name{isubj},'_explog.csv'],'Format','%d%d%s%d%d%d%f%s%d%d%d%f%d%d%d%f%f%f%f%f%f%f%d%s%f%f%f%f%f%f%f%f');

    %extract the relevant columns from the data
    wm_degdiff =  M.wm_degdiff;
    probe_trials = M.probe_trials;
    probe_trials_fast = M.fast_rt_trigger;
    probe_trials_slow = M.slow_rt_trigger;

    %select the data from probed trials
    resperror = wm_degdiff(probe_trials==1);
    resperror_fast = wm_degdiff(find(probe_trials_fast)+1);
    resperror_slow = wm_degdiff(find(probe_trials_slow)+1);

    %aggregate data from this subject
    aggre_resperror = [aggre_resperror;resperror];
    aggre_resperror_fast = [aggre_resperror_fast;resperror_fast];
    aggre_resperror_slow = [aggre_resperror_slow;resperror_slow];
    
    %all probes
    comparefit = MemFit(resperror, {StandardMixtureModel,AllGuessingModel});
    mixmodel.BIC(isubj,1:2) = comparefit.BIC;
    [~,mixmodel.model_pref(isubj)] = min(comparefit.BIC);
    if mixmodel.model_pref(isubj)==1
        subj_fit = MemFit(resperror_fast, StandardMixtureModel,'Verbosity', 0);
        mixmodel.model_fit(isubj,1:2) = subj_fit.posteriorMean;
    else
        mixmodel.model_fit(isubj,1:2) = NaN;
    end

    %fast triggered probes
    comparefit = MemFit(resperror_fast, {StandardMixtureModel,AllGuessingModel});
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


