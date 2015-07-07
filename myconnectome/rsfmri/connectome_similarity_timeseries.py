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
import scipy.stats

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

def connectome_similarity_timeseries(use_spearman=False):
    behavdata=load_behav_data()
    dates=behavdata[2]
    if use_spearman:
        spearman_flag='_spearman'
    else:
        spearman_flag=''
    try:
        corrsim_all=numpy.loadtxt(os.path.join(basedir,'rsfmri/corrsim_all%s.txt'%spearman_flag))
        corrsim_mean=numpy.loadtxt(os.path.join(basedir,'rsfmri/corrsim_mean%s.txt'%spearman_flag))
    except:
        corrdata,subcodes=load_fullcorr_data()
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
            if use_spearman:
                corrsim_mean[sess]=scipy.stats.spearmanr(meancorrdata,corrdata[sess,:])[0]
                corrsim_l2_mean[sess]=scipy.stats.spearmanr(meanl2data,l2data[sess,:])[0]
                
            else:
                corrsim_mean[sess]=numpy.corrcoef(meancorrdata,corrdata[sess,:])[0,1]
                corrsim_l2_mean[sess]=numpy.corrcoef(meanl2data,l2data[sess,:])[0,1]
            for s2 in range(corrdata.shape[0]):
                if sess==s2:
                    continue
                if use_spearman:
                    corrsim_all[sess,s2]=scipy.stats.spearmanr(corrdata[sess,:],corrdata[s2,:])[0]
                    corrsim_l2_all[sess,s2]=scipy.stats.spearmanr(l2data[sess,:],l2data[s2,:])[0]
                    
                else:
                    corrsim_all[sess,s2]=numpy.corrcoef(corrdata[sess,:],corrdata[s2,:])[0,1]
                    corrsim_l2_all[sess,s2]=numpy.corrcoef(l2data[sess,:],l2data[s2,:])[0,1]
            
        numpy.savetxt(os.path.join(basedir,'rsfmri/corrsim_all%s.txt'%spearman_flag),corrsim_all)
        numpy.savetxt(os.path.join(basedir,'rsfmri/corrsim_mean%s.txt'%spearman_flag),corrsim_mean)
        numpy.savetxt(os.path.join(basedir,'rsfmri/l2sim_all%s.txt'%spearman_flag),corrsim_l2_all)
        numpy.savetxt(os.path.join(basedir,'rsfmri/l2sim_mean%s.txt'%spearman_flag),corrsim_l2_mean)
    
    corrsim_all[numpy.diag_indices(corrsim_all.shape[0])]=corrsim_mean
    
    plt.figure(figsize=[12,4])
    
    plt.plot(corrsim_mean,linewidth=2)
    #plt.ylabel('Correlation with mean connectivity',fontsize=18)
    plt.xticks(range(0,84,9),[dates[i] for i in range(0,84,9)],rotation=45)
    plt.axis([0,83,0.65,0.9])
    plt.savefig(os.path.join(basedir,'rsfmri/mean_similarity_plot%s.pdf'%spearman_flag),bbox_inches='tight')

    
    plt.figure(figsize=[12,12])
    plt.imshow(corrsim_all,interpolation='nearest',origin='upper')
    plt.yticks(range(0,84,9),[dates[i] for i in range(0,84,9)])
    plt.colorbar(shrink=0.6)
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off') # labels along the bottom edge are off
    plt.savefig(os.path.join(basedir,'rsfmri/session_corr_similarity_heatmap%s.pdf'%spearman_flag))

if __name__ == "__main__":
    connectome_similarity_timeseries()
    connectome_similarity_timeseries(True)
