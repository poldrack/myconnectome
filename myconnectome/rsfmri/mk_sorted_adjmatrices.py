# -*- coding: utf-8 -*-
"""
make connectome matrices for each measure, sorted by infomap modules
Created on Sun Jun 21 15:58:15 2015

@author: poldrack
"""

import os
import numpy
import nilearn.plotting
import scipy.stats
from myconnectome.utils.load_parcel_data import load_parcel_data
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

def mk_sorted_adjmatrices(dtidensity=None):
    utr=numpy.triu_indices(630,1)

    parceldata=load_parcel_data(os.path.join(basedir,'parcellation/parcel_data.txt'))
    modules=numpy.zeros(len(parceldata))
    for i in range(len(parceldata)):
        modules[i]=parceldata[i+1]['powernum']

    module_idx=numpy.argsort(modules)
    breakpoints=[]
    netnames=[]
    for i in range(1,len(module_idx)):
        if not modules[module_idx[i]] == modules[module_idx[i-1]]:
            breakpoints.append(i)
    breakpoints.append(630)

    netnames=['none','DMN','V2','FP1','V1','DA','VA','Sal','CO','SM','FP2','MPar','ParOcc','subcort']

    dtidata=numpy.loadtxt(os.path.join(basedir,'diffusion/tracksumm_distcorr.txt'),skiprows=1)
    dtidata=dtidata[:,1:]
    dtidata=dtidata+dtidata.T
    tmp=dtidata[module_idx,:]
    dtidata_sorted=tmp[:,module_idx]
    if not dtidensity:
        dtithresh=0
    else:
        dtithresh=scipy.stats.scoreatpercentile(dtidata[utr],dtidensity)

    dtibin=dtidata>dtithresh

    dtidata_skyra=numpy.loadtxt(os.path.join(basedir,'diffusion/tracksumm_distcorr_skyra.txt'),skiprows=1)
    dtidata_skyra=dtidata_skyra[:,1:]
    dtidata_skyra=dtidata_skyra+dtidata_skyra.T
    tmp=dtidata_skyra[module_idx,:]
    dtidata_skyra_sorted=tmp[:,module_idx]
    if not dtidensity:
        dtithresh_skyra=0
    else:
        dtithresh_skyra=scipy.stats.scoreatpercentile(dtidata_skyra[utr],dtidensity)
    dtibin_skyra=dtidata_skyra>0

    bp=numpy.array(breakpoints)
    textlocs=numpy.mean(numpy.vstack((bp,numpy.hstack(([0],bp[:-1])))),0)

    plt.figure(figsize=[12,12])
    plt.imshow(dtidata_sorted,origin='upper',cmap='gray',vmin=0,vmax=scipy.stats.scoreatpercentile(dtidata,90))
    for b in breakpoints:
        plt.plot([0,630],[b,b],'r',linewidth=1.5)
        plt.plot([b,b],[0,630],'r',linewidth=1.5)
    plt.yticks(textlocs,netnames,fontsize=14)
    plt.xticks(textlocs,netnames,fontsize=14,rotation=90)
    plt.axis('image')
    plt.title('Diffusion tractography - HARDI',fontsize=18)

    plt.savefig(os.path.join(basedir,'diffusion/adjmtx_binarized_sorted_modules_HARDI.pdf'))


    plt.figure(figsize=[12,12])
    plt.imshow(dtidata_skyra_sorted,origin='upper',cmap='gray',vmin=0,vmax=scipy.stats.scoreatpercentile(dtidata_skyra,90))
    for b in breakpoints:
        plt.plot([0,630],[b,b],'r',linewidth=1.5)
        plt.plot([b,b],[0,630],'r',linewidth=1.5)
    plt.yticks(textlocs,netnames,fontsize=14)
    plt.xticks(textlocs,netnames,fontsize=14,rotation=90)
    plt.axis('image')
    plt.title('Diffusion tractography - Skyra',fontsize=18)

    plt.savefig(os.path.join(basedir,'diffusion/adjmtx_binarized_sorted_modules_Skyra.pdf'))

    dice=(2.0*numpy.sum(dtibin_skyra*dtibin))/float(numpy.sum(dtibin_skyra)+numpy.sum(dtibin))
    print 'dice(HARDI,skyra)=',dice

    rsfmridata=numpy.load(os.path.join(basedir,'rsfmri/corrdata.npy'))

    rsfmridata=r_to_z(rsfmridata)
    meancorr_z=numpy.mean(rsfmridata,0)
    meancorr=z_to_r(meancorr_z)
    rsadj=numpy.zeros((630,630))
    rsadj[utr]=meancorr
    rsadj=rsadj+rsadj.T
    tmp=rsadj[module_idx,:]
    rsadj_sorted=tmp[:,module_idx]

    plt.figure(figsize=[12,12])
    plt.imshow(rsadj_sorted,origin='upper',cmap='seismic',vmin=-.8,vmax=0.8)
    for b in breakpoints:
        plt.plot([0,630],[b,b],'r',linewidth=1.5)
        plt.plot([b,b],[0,630],'r',linewidth=1.5)
    plt.yticks(textlocs,netnames,fontsize=14)
    plt.xticks(textlocs,netnames,fontsize=14,rotation=90)
    plt.axis('image')
    plt.title('Full correlation',fontsize=18)
    plt.colorbar(shrink=0.5)

    plt.savefig(os.path.join(basedir,'rsfmri/adjmtx_sorted_modules.pdf'))


    l2data=numpy.load(os.path.join(basedir,'rsfmri/l2_utr_data.npy'))
    l2data=r_to_z(l2data)
    meanl2data=numpy.mean(l2data,0)
    meanl2data=z_to_r(meanl2data)

    l2adj=numpy.zeros((630,630))
    l2adj[utr]=meanl2data
    l2adj=l2adj+l2adj.T
    tmp=l2adj[module_idx,:]
    l2adj_sorted=tmp[:,module_idx]

    plt.figure(figsize=[12,12])
    plt.imshow(l2adj_sorted,origin='upper',cmap='seismic',vmin=-.025,vmax=0.025)
    for b in breakpoints:
        plt.plot([0,630],[b,b],'r',linewidth=1.5)
        plt.plot([b,b],[0,630],'r',linewidth=1.5)
    plt.yticks(textlocs,netnames,fontsize=14)
    plt.xticks(textlocs,netnames,fontsize=14,rotation=90)
    plt.axis('image')
    plt.title('L2-regularized partial correlation',fontsize=18)
    plt.colorbar(shrink=0.5)
    plt.savefig(os.path.join(basedir,'rsfmri/pcorr_l2_adjmtx_sorted_modules.pdf'))



    taskdata=numpy.loadtxt(os.path.join(basedir,'taskfmri/task_connectome.txt'))
    tmp=taskdata[module_idx,:]
    taskdata_sorted=tmp[:,module_idx]

    plt.figure(figsize=[12,12])
    plt.imshow(taskdata_sorted,origin='upper',cmap='seismic',vmin=-.8,vmax=0.8)
    for b in breakpoints:
        plt.plot([0,630],[b,b],'r',linewidth=1.5)
        plt.plot([b,b],[0,630],'r',linewidth=1.5)
    plt.yticks(textlocs,netnames,fontsize=14)
    plt.xticks(textlocs,netnames,fontsize=14,rotation=90)
    plt.axis('image')
    plt.title('Task correlation',fontsize=18)
    plt.colorbar(shrink=0.5)
    plt.savefig(os.path.join(basedir,'taskfmri/taskcorr_adjmtx_sorted_modules.pdf'))

if __name__ == "__main__":
    mk_sorted_adjmatrices()
