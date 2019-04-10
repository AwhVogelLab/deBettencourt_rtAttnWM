%expt3c_mixmodel.m
%
%this runs mixture modeling for the wmPrecis01 experiment
%
%1. First, it runs mixture models for all probe trials for each subject
%2. Then, it runs mixture models using aggregate data from all subjects
%
%Outputs a mat file "mixturemodel" to the results folder, with struct 
% mixmodel with fields:
% - BIC:             BIC of models (standard, guessing)
% - model_pref:      whether a mixture model is preferred over guessing
% - model_fit:       fit to each participant separately
% - aggre_model_fit: fit to aggregate data 
%
%MdB, 01/2019

%setpath
addpath(genpath('~/Documents/packages/MemToolbox/'))

%directories
proj_dir = '../expt3c/';
results_dir = [proj_dir 'results/'];

%subjects
subj_name = {'1206181_wmPrecis01', '1206182_wmPrecis01', '1206183_wmPrecis01',...
             '1207181_wmPrecis01', '1207183_wmPrecis01', '1207184_wmPrecis01',...
             '1207185_wmPrecis01', '1207186_wmPrecis01', '1207187_wmPrecis01',...
             '1207188_wmPrecis01', '1207189_wmPrecis01', '1208181_wmPrecis01',...
             '1208182_wmPrecis01', '1208183_wmPrecis01', '1208184_wmPrecis01',...
             '1208185_wmPrecis01', '1208186_wmPrecis01', '1208187_wmPrecis01',...
             '1208188_wmPrecis01', '1208189_wmPrecis01', '1210181_wmPrecis01',...
             '1210182_wmPrecis01', '1210183_wmPrecis01'};
nsubj = numel(subj_name);


%%

%preallocate empty aggregate variables
aggre_resperror = [];
aggre_resperror_fast = [];
aggre_resperror_slow = [];


for isubj = 1:numel(subj_name)
    
    isubj 
    
    %load the subject csv files
    M = readtable([proj_dir,'/subjects/' subj_name{isubj},'_explog.csv'],'Format','%d%d%f%f%f%f%f%f%f%f%f%f%f%f%f%d%s%f%f');

    %extract the relevant columns from the data
    resperror =  double(M.wm_degdiff);

    %aggregate data from all subjects
    aggre_resperror = [aggre_resperror;resperror];
    
    %all probes
    comparefit = MemFit(resperror, {StandardMixtureModel,AllGuessingModel});
    mixmodel.BIC(isubj,1:2) = comparefit.BIC;
    [~,mixmodel.model_pref(isubj)] = min(comparefit.BIC);
    if mixmodel.model_pref(isubj)==1
        subj_fit = MemFit(resperror, StandardMixtureModel,'Verbosity', 0);
        mixmodel.model_fit(isubj,1:2) = subj_fit.posteriorMean;
    else
        mixmodel.model_fit(isubj,1:2) = NaN;
    end
    
end



%% fitting aggregate data from all subjects


temp_fit = MemFit(aggre_resperror, StandardMixtureModel,'Verbosity', 0);
mixmodel.aggre_model_fit = temp_fit.posteriorMean;
mixmodel.aggre_model_lowerCI = temp_fit.lowerCredible;
mixmodel.aggre_model_upperCI = temp_fit.upperCredible;



%% save data

save([proj_dir,'/results/mixturemodel.mat'],'mixmodel','subj_name')


