"""
use SVM to predict outcome variables based on connectivity

"""

import numpy
import sklearn.preprocessing
import scipy.stats
from run_classification import run_classification
from load_myconnectome_data import *

xvar_names=['panas.positive','panas.negative','panas.fatigue','afterscan.Anxietyduringscan','afterscan.diastolic',
'afterscan.pulse','afterscan.systolic','morning.Sleepquality','morning.Soreness','prevevening.Alcohol',
'prevevening.Guthealth','prevevening.Psoriasisseverity','prevevening.Stress', 'prevevening.Timespentoutdoors',
"email.LIWC_negemo","email.LIWC_posemo",'zeo.zq']

rnaseq_data,gene_names,rnaseq_dates,rnaseq_subcodes=load_rnaseq_data()
behavdata,behav_vars,behav_dates,behav_subcodes=load_behav_data(xvars=xvar_names)

rnaseq_joint,behavdata_joint,subcodes_joint=get_matching_datasets(rnaseq_data,behavdata,rnaseq_subcodes,behav_subcodes)    


type='regression'
#f=open('/Users/poldrack/Dropbox/data/selftracking/prediction_results/wgcna_behav_predict.txt','w')
    
predacc=run_classification(rnaseq_joint,behavdata_joint,n_train_runs=50,verbose=False,type=type)        
predacc_null=run_classification(rnaseq_joint,behavdata_joint,n_shuffle_runs=1000,shuffle=True,verbose=False,type=type)

#f.write('%s\t%f\t%f\n'%(behav_vars[varnum],numpy.mean(predacc),pval))
#f.close()

max_all=numpy.max(predacc_null,1)
pcorr=numpy.zeros(predacc.shape[1])
puncorr=numpy.zeros(predacc.shape[1])

for var in range(predacc.shape[1]):
    pcorr[var]=(100.0 - scipy.stats.percentileofscore(max_all, numpy.mean(predacc[:,var])))/100.0
    puncorr[var]=(100.0 - scipy.stats.percentileofscore(predacc_null[:,var], numpy.mean(predacc[:,var])))/100.0
    print xvar_names[var],numpy.mean(predacc[:,var]),puncorr[var],pcorr[var]
    
numpy.save('/Users/poldrack/Dropbox/data/selftracking/prediction_results/predacc_wgcna_behav.npy',predacc)
numpy.save('/Users/poldrack/Dropbox/data/selftracking/prediction_results/predacc_null_wgcna_behav.npy',predacc_null)
