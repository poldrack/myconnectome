"""
load an adjacency matrix and reorder by networks
for javascript viewer
"""

import numpy
import os
from load_parcel_data import *



def reorder_adjmtx_by_network(adjmtx_file,outdir,network_order=[0,1,7,3,11,8,9,12,13,5,6,14,10,4,2]):
#adjmtx_file='/Users/poldrack/Dropbox/data/selftracking/rsfmri/behav_adjmtx/tu_th_adjmtx.txt'
#outdir='test'
#network_order=[0,1,7,3,11,8,9,12,13,5,6,14,10,4,2]
#if 1:
    
    try:
        assert os.path.exists(outdir)
    except:
        os.mkdir(outdir)
    
    info_file_unspaced=os.path.join(outdir,'parcel_info_unspaced.txt')
    info_file_spaced=os.path.join(outdir,'parcel_info_spaced.txt')
    data_file_unspaced=os.path.join(outdir,'data_unspaced.txt')
    data_file_spaced=os.path.join(outdir,'data_spaced.txt')
     
    parceldata=load_parcel_data()
        
    adjmtx_orig=numpy.loadtxt(adjmtx_file)
    # fill out other triangle
    adjmtx_orig=adjmtx_orig + adjmtx_orig.T
    
    
    adjmtx_new=numpy.zeros(adjmtx_orig.shape)
    
    netnum=[parceldata[i]['powernum'] for i in range(1,adjmtx_orig.shape[1]+1)]
    netnum_neworder=[numpy.where(numpy.array(network_order)==i)[0][0] for i in netnum]
    netnum=netnum_neworder

    yloc=[parceldata[i]['y'] for i in range(1,adjmtx_orig.shape[1]+1)]
    
    hemis=[int(parceldata[i]['hemis']=='L') for i in range(1,adjmtx_orig.shape[1]+1)]
    
    # sort by network num and then by y location
    idx=numpy.lexsort((yloc,netnum,hemis))
    # reverse indices for left hemisphere so that it travels around the circle
    
    idx[numpy.array(hemis)[idx]==1]=idx[numpy.array(hemis)[idx]==1][::-1]
    parcelinfo_new={}
    
    for i in range(adjmtx_orig.shape[0]):
        parcelinfo_new[i+1]=parceldata[idx[i]+1]
        parcelinfo_new[i+1]['orig_roi']=idx[i]+1
        for j in range(adjmtx_orig.shape[0]):
            adjmtx_new[i,j]=adjmtx_orig[idx[i],idx[j]]
            
    netnum_sorted=numpy.array(netnum)[idx]
    good_nodes=numpy.where(netnum_sorted>0)[0]
    netnum_goodnodes=netnum_sorted[good_nodes]
    
    adjmtx_new=adjmtx_new[netnum_sorted>0,:]
    adjmtx_new=adjmtx_new[:,netnum_sorted>0]
    
    for i in range(adjmtx_orig.shape[0]):
        if netnum_sorted[i]==0:
            parcelinfo_new.pop(i+1)
            
    f=open(info_file_unspaced,'w')
    for i in range(len(good_nodes)):
        p=parcelinfo_new[good_nodes[i]+1]
        if p['powernetwork']=='na':
            p['powernetwork']='Subcortical'
        f.write('%d\t%d\t%0.2f\t%0.2f\t%0.2f\t%s\t%s\t%d\n'%(i+1,p['orig_roi'],p['x'],p['y'],p['z'],p['hemis'],p['powernetwork'],p['powernum']))
    f.close()
    
    numpy.savetxt(data_file_unspaced, adjmtx_new)
    
    # insert dummy nodes between networks
    
    
    f=open(info_file_spaced,'w')
    datactr=[]
    for i in range(len(good_nodes)):
        p=parcelinfo_new[good_nodes[i]+1]
        if p['powernetwork']=='na':
            p['powernetwork']='Subcortical'
        if i>0 and (p['powernum']!=parcelinfo_new[good_nodes[i]]['powernum'] or p['hemis']!=parcelinfo_new[good_nodes[i]]['hemis']):
            f.write('-1\t-1\t0\t0\t0\tdummy\tdummy\t-1\n')
            datactr.append(-1)
        f.write('%d\t%d\t%0.2f\t%0.2f\t%0.2f\t%s\t%s\t%d\n'%(i+1,p['orig_roi'],p['x'],p['y'],p['z'],p['hemis'],p['powernetwork'],p['powernum']))
        datactr.append(i)
    f.close()
    
    adjmtx_new_spaced=numpy.zeros((len(datactr),len(datactr)))
    for i in range(len(datactr)):
        if not datactr[i]<0:
          for j in range(len(datactr)):
            if not datactr[j]<0:
                adjmtx_new_spaced[i,j]=adjmtx_new[datactr[i],datactr[j]]
   
    # reality check
    assert numpy.sum(adjmtx_new_spaced)==numpy.sum(adjmtx_new)
    
    numpy.savetxt(data_file_spaced, adjmtx_new_spaced)
    
