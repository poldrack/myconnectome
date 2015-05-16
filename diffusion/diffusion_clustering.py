"""
cluster parcels based on diffusion
"""

import numpy
import igraph
import os
import scipy.stats
import sklearn.cluster
import nibabel.gifti.giftiio
from consensus_cluster import pair_consensus
from run_shell_cmd import run_shell_cmd

basedir='/Users/poldrack/Dropbox/data/selftracking/DTI'
data=numpy.loadtxt('/Users/poldrack/Dropbox/data/selftracking/DTI/tracksumm_distcorr.txt')
data=data[:620,:620]
    


method='infomap'

size_thresh=8
densities=numpy.arange(0.00005,0.03,0.005)
assignments=numpy.zeros((620,len(densities)))

for dens in range(len(densities)):   
    edge_density=densities[dens]
    cc=data.copy()
    cc[numpy.tril_indices(620)]=0
    edlabel='_%0.2f'%edge_density
    pct=scipy.stats.scoreatpercentile(cc[numpy.triu_indices(620,1)],100.0 - 100.0*edge_density)
    
    cc[cc<pct]=0
    cc[cc>0]=1
    gg=igraph.Graph.Adjacency(cc.tolist(),mode='UNDIRECTED')
    modclust_infomap=gg.community_infomap() #edge_weights='weight')
    print modclust_infomap.modularity
    assgn=numpy.array([i+1 for i in modclust_infomap.membership])  # zero treated as unclustered
    # exclude small modules by setting to zero
    for c in numpy.unique(assgn):
        if numpy.sum(assgn==c)<size_thresh:
            assgn[assgn==c]=0
    print 'density %0.3f (%0.3f): %d clusters'%(densities[dens],pct,len(numpy.unique(assgn)))
    assignments[:,dens]=assgn
    
numpy.savetxt('assignments.txt',assignments)


#cons=pair_consensus(assignments.T.astype('int'))
run_shell_cmd('/Applications/MATLAB_R2015a.app/bin/matlab -nosplash -nodesktop < Consensus_infomap_simple.m')


# modules start at zero
# relabel all single-node modules as zero and ignore them

labels=numpy.loadtxt('assignments_minsize5_regularized_consensus.txt')

SHUFFLE=False
if SHUFFLE:
    numpy.random.shuffle(labels)
# load parcel info
lines=open('/Users/poldrack/Dropbox/data/selftracking/rsfmri/module_assignments.txt').readlines()
modules=numpy.array([float(l.strip().split()[3]) for l in lines])
unique_modules=numpy.append(numpy.unique(modules)[1:],100)  # drop the zeros
module_hist_cutoffs=unique_modules-0.01


# get task distribution for each module

network_names=['1 Default','2 Second Visual','3 Frontal-Parietal','4.5 First Visual (V1+)','5 First Dorsal Attention','6 Second Dorsal Attention','7 Ventral Attention/Language','8 Salience','9 Cingulo-opercular','10 Somatomotor','11.5 Frontal-Parietal Other','15 Parietal Episodic Retrieval','16 Parieto-Occipital']

for l in numpy.unique(labels):
    if l < 1:
        continue
    members=labels==l
    networks=modules[members]
    networks=networks[networks>0]
    h=numpy.histogram(networks,bins=module_hist_cutoffs)[0]
    maxnet=numpy.where(h==numpy.max(h))[0][0]
    print 'Module',l,numpy.sum(members),'members'
    meanzstat=numpy.mean(data[:,members],1)
    idx=numpy.argsort(meanzstat)[::-1]
    #print 'Top contrasts:'
    #for i in idx[:5]:
    #    print copenames[i]
    hg=scipy.stats.hypergeom.sf(h[maxnet]-1,620,numpy.sum(modules==unique_modules[maxnet]),numpy.sum(members))
    if numpy.isnan(hg):
        asdf
    print 'Top network match: %s (pct match=%0.2f, dice = %0.3f, p < %0.3f)'%(network_names[maxnet],
        h[maxnet]/float(numpy.sum(members)), 
        2*numpy.sum(modules==unique_modules[maxnet] * members)/float(numpy.sum(modules==unique_modules[maxnet]) + numpy.sum(members)), 
        hg)

    
    print ''



# make gii files showing all modules

import nibabel.gifti.giftiio

lh=nibabel.gifti.giftiio.read('/Users/poldrack/Dropbox/data/selftracking/parcellation/all_selected_L_parcel_renumbered.func.gii')
rh=nibabel.gifti.giftiio.read('/Users/poldrack/Dropbox/data/selftracking/parcellation/all_selected_R_parcel_renumbered.func.gii')

lh_labels=lh.darrays[0].data.copy()
rh_labels=rh.darrays[0].data.copy()
labeled_regions_lh=numpy.unique(lh_labels)
labeled_regions_rh=numpy.unique(rh_labels)

lhimg=nibabel.gifti.GiftiImage()

rhimg=nibabel.gifti.GiftiImage()

labelvals=numpy.unique(labels)
modules_lh=labels[:310]
modules_rh=labels[310:]

for i in labelvals:
    if i < 1:
        continue
    darray=numpy.zeros(lh.darrays[0].data.shape,dtype=numpy.float32)
    matches=numpy.where(modules_lh==i)[0]+1
    for m in matches:
        darray[lh_labels==m]=1
    
    lhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray,intent=lh.darrays[0].intent,datatype=lh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'module%02d'%i}))

    darray=numpy.zeros(rh.darrays[0].data.shape,dtype=numpy.float32)
    matches=numpy.where(modules_rh==i)[0]+311
    for m in matches:
        darray[rh_labels==m]=1
    
    rhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray,intent=rh.darrays[0].intent,datatype=rh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexRight','Name':'module%02d'%i}))

if not SHUFFLE:
    nibabel.gifti.giftiio.write(lhimg,os.path.join(basedir,'lh_%s_consensus.func.gii'%method))
    nibabel.gifti.giftiio.write(rhimg,os.path.join(basedir,'rh_%s_consensus.func.gii'%method))
