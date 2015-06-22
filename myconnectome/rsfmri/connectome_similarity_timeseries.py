# -*- coding: utf-8 -*-
"""
create plot of connectome similarity over time - after tim's figure from 
response to reviewers
Created on Fri Jun 19 16:45:01 2015

@author: poldrack
"""

import numpy
import os
import matplotlib.pyplot as plt
from myconnectome.timeseries.load_myconnectome_data import load_behav_data,load_fullcorr_data

def r_to_z(r):
    # fisher transform
    z=0.5*numpy.log((1.0+r)/(1.0-r))
    z[numpy.where(numpy.isinf(z))]=0
    z[numpy.where(numpy.isnan(z))]=0

    return z

def z_to_r(z):
    # inverse transform
    return (numpy.exp(2.0*z) - 1)/(numpy.exp(2.0*z) + 1)

basedir=os.environ['MYCONNECTOME_DIR']

corrdata,subcodes=load_fullcorr_data()
behavdata=load_behav_data()
dates=behavdata[2]
corrdata=r_to_z(corrdata)

l2data=numpy.load(os.path.join(basedir,'rsfmri/l2_utr_data.npy'))
l2data=r_to_z(l2data)

meancorrdata=numpy.mean(corrdata,0)
meanl2data=numpy.mean(l2data,0)

corrsim_mean=numpy.zeros(corrdata.shape[0])
corrsim_all=numpy.zeros((corrdata.shape[0],corrdata.shape[0]))
corrsim_l2_mean=numpy.zeros(corrdata.shape[0])
corrsim_l2_all=numpy.zeros((corrdata.shape[0],corrdata.shape[0]))

for sess in range(corrdata.shape[0]):
    corrsim_mean[sess]=numpy.corrcoef(meancorrdata,corrdata[sess,:])[0,1]
    corrsim_l2_mean[sess]=numpy.corrcoef(meanl2data,l2data[sess,:])[0,1]
    for s2 in range(corrdata.shape[0]):
        if sess==s2:
            continue
        corrsim_all[sess,s2]=numpy.corrcoef(corrdata[sess,:],corrdata[s2,:])[0,1]
        corrsim_l2_all[sess,s2]=numpy.corrcoef(l2data[sess,:],l2data[s2,:])[0,1]
    
numpy.savetxt(os.path.join(basedir,'rsfmri/corrsim_all.txt'),corrsim_all)
numpy.savetxt(os.path.join(basedir,'rsfmri/corrsim_mean.txt'),corrsim_mean)
numpy.savetxt(os.path.join(basedir,'rsfmri/l2sim_all.txt'),corrsim_all)
numpy.savetxt(os.path.join(basedir,'rsfmri/l2sim_mean.txt'),corrsim_mean)

corrsim_all[numpy.diag_indices(corrsim_all.shape[0])]=corrsim_mean
corrsim_l2_all[numpy.diag_indices(corrsim_all.shape[0])]=corrsim_l2_mean

plt.figure(figsize=[16,8])
plt.plot(corrsim_mean,linewidth=2)
#plt.hold(True)
#plt.plot(corrsim_l2_mean,linewidth=2)
plt.ylabel('Correlation with mean connectivity',fontsize=18)
plt.xticks(range(0,84,9),[dates[i] for i in range(0,84,9)],rotation=45)
#plt.legend(['Full correlation','Partial correlation'])
plt.savefig(os.path.join(basedir,'rsfmri/mean_similarity_plot.pdf'))

plt.figure(figsize=[12,12])
plt.imshow(corrsim_all,interpolation='nearest',origin='upper')
plt.yticks(range(0,84,9),[dates[i] for i in range(0,84,9)])
plt.xticks(range(0,84,9),[dates[i] for i in range(0,84,9)],rotation=45)
plt.colorbar(shrink=0.6)

plt.savefig(os.path.join(basedir,'rsfmri/session_corr_similarity_heatmap.pdf'))

plt.figure(figsize=[12,12])
plt.imshow(corrsim_l2_all,interpolation='nearest',origin='upper')
plt.yticks(range(0,84,9),[dates[i] for i in range(0,84,9)])
plt.xticks(range(0,84,9),[dates[i] for i in range(0,84,9)],rotation=45)
plt.colorbar(shrink=0.6)

plt.savefig(os.path.join(basedir,'rsfmri/session_l2_similarity_heatmap.pdf'))

