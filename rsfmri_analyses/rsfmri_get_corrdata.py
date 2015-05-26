"""
load data from tim laumann and process
"""

import numpy
import os,sys,glob
import sklearn.covariance
import scipy.linalg

def pcor_from_precision(P,zero_diagonal=1):
    # given a precision matrix, compute the partial correlation matrix
    # based on wikipedia page: http://en.wikipedia.org/wiki/Partial_correlat
    #Using_matrix_inversion
    pcor=numpy.zeros(P.shape)
    for i in range(P.shape[0]):
        for j in range(P.shape[1]):
            pcor[i,j]=P[i,j]/numpy.sqrt(P[i,i]*P[j,j])
            if zero_diagonal==1 and i==j:
                pcor[i,j]=0
    return pcor

basedir='/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses'
datadir='/corral-repl/utexas/poldracklab/data/selftracking/combined_data_scrubbed'
# first compute correlations

corrfile=os.path.join(basedir,'corrdata.npy')
subcodefile=os.path.join(basedir,'subcodes.txt')


# compute correlations
# drop first 50 timepoints due to startup artifact from noise cancellation

subfiles=glob.glob(os.path.join(datadir,'sub*.txt'))
subfiles.sort()
subcodes=[i.split('/')[-1].replace('.txt','') for i in subfiles]
for s in range(len(subcodes)):
    print 'processing',subcodes[s],subfiles[s]
    data=numpy.loadtxt(subfiles[s])[50:,:]
    
    tmask=numpy.loadtxt('/corral-repl/utexas/poldracklab/data/selftracking/tmasks/%s.txt'%subcodes[s])[50:]
    data=data[tmask==1,:]
    
    if s==0:
        utr=numpy.triu_indices(data.shape[1],1)
        corrdata=numpy.zeros((len(subcodes),len(utr[0])))
        #pcorrdata=numpy.zeros((len(subcodes),len(utr[0])))
        f=open(subcodefile,'w')
        for i in subcodes:
            f.write(i+'\n')
        f.close()

    cc=numpy.corrcoef(data.T)
    corrdata[s,:]=cc[utr]
    


numpy.save(corrfile,corrdata)

        
        
    
