# -*- coding: utf-8 -*-
"""
make images for connnectivity adjmtx

Created on Sun Jun 21 09:19:06 2015

@author: poldrack
"""

import os
import numpy
import nilearn.plotting
import scipy.stats
from myconnectome.utils.get_parcel_coords import get_parcel_coords
import matplotlib.pyplot as plt

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
use_abs_corr=False

dtidata=numpy.loadtxt(os.path.join(basedir,'diffusion/tracksumm_distcorr.txt'),skiprows=1)
dtidata=dtidata[:,1:]
dtidata=dtidata+dtidata.T
dtibin=dtidata>0

rsfmridata=numpy.load(os.path.join(basedir,'rsfmri/corrdata.npy'))

rsfmridata=r_to_z(rsfmridata)
meancorr_z=numpy.mean(rsfmridata,0)
meancorr=z_to_r(meancorr_z)
if use_abs_corr:
    meancorr=numpy.abs(meancorr)

meancorr[numpy.isnan(meancorr)]=0
adjsize=630
utr=numpy.triu_indices(adjsize,1)
meandti=dtidata[utr]

task_connectome=numpy.loadtxt(os.path.join(basedir,'taskfmri/task_connectome.txt'))
taskdata=task_connectome[utr]

l2data=numpy.load(os.path.join(basedir,'rsfmri/l2_utr_data.npy'))
l2mean=z_to_r(numpy.mean(r_to_z(l2data),0))

l1data=numpy.load(os.path.join(basedir,'rsfmri/quic_utr_data_0.1.npy'))
l1mean=z_to_r(numpy.mean(r_to_z(l1data),0))

thresh=0.0025

rsthresh=meancorr > scipy.stats.scoreatpercentile(meancorr,100-100*thresh)
dtithresh=meandti > scipy.stats.scoreatpercentile(meandti,100-100*thresh)
taskthresh=taskdata > scipy.stats.scoreatpercentile(taskdata,100-100*thresh)
l2thresh=l2mean > scipy.stats.scoreatpercentile(l2mean,100-100*thresh)
l1thresh=l1mean > scipy.stats.scoreatpercentile(l1mean,100-100*thresh)

rsadj=numpy.zeros((adjsize,adjsize))
l2adj=numpy.zeros((adjsize,adjsize))
l1adj=numpy.zeros((adjsize,adjsize))
dtiadj=numpy.zeros((adjsize,adjsize))
taskadj=numpy.zeros((adjsize,adjsize))

rsadj[utr]=rsthresh
l2adj[utr]=l2thresh
l1adj[utr]=l1thresh
dtiadj[utr]=dtithresh
taskadj[utr]=taskthresh

rsadj=rsadj+rsadj.T
l2adj=l2adj+l2adj.T
l1adj=l1adj+l1adj.T
dtiadj=dtiadj+dtiadj.T
taskadj=taskadj+taskadj.T

coords=get_parcel_coords()

def get_mean_connection_distance(input):
    from scipy.spatial.distance import euclidean
    adj=input.copy()
    adj[numpy.tril_indices(adj.shape[0])]=0
    coords=get_parcel_coords()
    dist=[]
    hits=numpy.where(adj>0)
    for h in range(hits[0].shape[0]):
        dist.append(euclidean(coords[hits[0][h]],coords[hits[1][h]]))
    return numpy.mean(dist)
    
print 'mean connection distances (%0.04f density)'%thresh
print 'fullcorr:',get_mean_connection_distance(rsadj)
print 'l1 pcorr:',get_mean_connection_distance(l1adj)
print 'l2 pcorr:',get_mean_connection_distance(l2adj)
print 'task corr:',get_mean_connection_distance(taskadj)
print 'dti:',get_mean_connection_distance(dtiadj)

dti_sum=numpy.sum(dtiadj,0)
tmp=dtiadj[dti_sum>0,:]
dtiadj_reduced=tmp[:,dti_sum>0]
#dtiadj_reduced=dtiadj_reduced+dtiadj_reduced.T
nilearn.plotting.plot_connectome(dtiadj_reduced,coords[dti_sum>0,:],node_size=2,
                                 output_file=os.path.join(basedir,'diffusion/dti_connectome.pdf'))
rs_sum=numpy.sum(rsadj,0)
rsadj_match=rsadj*0.01 + rsadj*dtibin*0.8 # add one to matches to change edge color
tmp=rsadj_match[rs_sum>0,:]
rsadj_reduced=tmp[:,rs_sum>0]
#rsadj_reduced=rsadj_reduced+rsadj_reduced.T
nilearn.plotting.plot_connectome(rsadj_reduced,coords[rs_sum>0,:],node_size=2,
                                 edge_vmin=0,edge_vmax=1,edge_cmap='seismic',edge_kwargs={'linewidth':1},
                                 output_file=os.path.join(basedir,'rsfmri/rsfmri_corr_connectome.pdf'))


l2_sum=numpy.sum(l2adj,0)
l2adj_match=l2adj*0.01 +  l2adj*dtibin*0.8 # add one to matches to change edge color
tmp=l2adj_match[l2_sum>0,:]
l2adj_reduced=tmp[:,l2_sum>0]
#l2adj_reduced=l2adj_reduced+l2adj_reduced.T
nilearn.plotting.plot_connectome(l2adj_reduced,coords[l2_sum>0,:],node_size=2,
                                 edge_vmin=0,edge_vmax=1,edge_cmap='seismic',edge_kwargs={'linewidth':1},
                                 output_file=os.path.join(basedir,'rsfmri/rsfmri_l2_connectome.pdf'))

task_sum=numpy.sum(taskadj,0)
taskadj_match=taskadj*0.01 +  taskadj*dtibin*0.8 # add one to matches to change edge color
tmp=taskadj_match[task_sum>0,:]
taskadj_reduced=tmp[:,task_sum>0]
#taskadj_reduced=taskadj_reduced+taskadj_reduced.T
nilearn.plotting.plot_connectome(taskadj_reduced,coords[task_sum>0,:],node_size=2,
                                 edge_vmin=0,edge_vmax=1,edge_cmap='seismic',edge_kwargs={'linewidth':1},
                                 output_file=os.path.join(basedir,'taskfmri/task_connectome.pdf'))
