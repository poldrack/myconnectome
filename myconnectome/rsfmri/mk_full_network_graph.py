# -*- coding: utf-8 -*-
"""
make full network graph file for cytoscape
Created on Sun May  3 09:18:46 2015

@author: poldrack
"""

import numpy
import networkx
import scipy.stats
import sys,os
from myconnectome.utils.get_hubs import get_hubs
from myconnectome.utils.r2z import r_to_z,z_to_r
from myconnectome.utils.load_parcel_data import load_parcel_data

basedir=os.environ['MYCONNECTOME_DIR']

def get_full_network_file(days='all',density=0.01):   
    print 'generating network file for',days
    assert days in ['mon','tues','thurs','all']
    
    parceldata=load_parcel_data()
    
    modinfofile=os.path.join(basedir,'rsfmri/module_assignments.txt')
    f=open(modinfofile)
    module_assignment=[]
    lines=f.readlines()
    f.close()
    for i in range(len(lines)):
        l_s=lines[i].strip().split('\t')
        module_assignment.append(float(l_s[3]))
        
    participation=numpy.loadtxt(os.path.join(basedir,'rsfmri/PIpos_weighted_louvain_bct.txt'))
    
    # tues =2, thurs=4
    daycodes=numpy.loadtxt(os.path.join(basedir,'daycodes.txt'))
    
    datafile=os.path.join(basedir,'rsfmri/corrdata.npy')
    data=numpy.load(datafile)
    
    if days=='thurs':
        meandata=z_to_r(numpy.mean(r_to_z(data[daycodes==4,:]),0))
        participation=numpy.mean(participation[:,daycodes==4],1)
    elif days=='mon':
        meandata=z_to_r(numpy.mean(r_to_z(data[daycodes==1,:]),0))
        participation=numpy.mean(participation[:,daycodes==1],1)
    elif days=='tues':
        meandata=z_to_r(numpy.mean(r_to_z(data[daycodes==2,:]),0))
        participation=numpy.mean(participation[:,daycodes==2],1)
    else:
      meandata=z_to_r(numpy.mean(r_to_z(data),0))
      participation=numpy.mean(participation,1)
    
    
    cutoff=scipy.stats.scoreatpercentile(meandata,100-100*density)
    meandata_thr=(meandata>cutoff).astype('int')
    utr=numpy.triu_indices(630,1)
    adj=numpy.zeros((630,630))
    adj[utr]=meandata_thr
    
    
    G=networkx.from_numpy_matrix(adj)
    nodes=G.nodes()
    nodes.sort()
    degree=[G.degree()[i] for i in nodes]
    hubs=get_hubs(degree,participation)
    for node in nodes:
        try:
            G.node[node]['module']=module_assignment[node]
        except:
            G.node[node]['module']=-1
        G.node[node]['degree']=G.degree()[node]
        G.node[node]['hub']=int(hubs[node])
        G.node[node]['PI']=float(participation[node])

    # filter out unconnected nodes
    G.remove_nodes_from((n for n,d in G.degree_iter() if d<2))
     
    networkx.write_graphml(G,os.path.join(basedir,'rsfmri/network_graph_%s_%0.3f.graphml'%(days,density)))

if __name__ == '__main__':
    for day in ['mon','tues','thurs','all']:
        get_full_network_file(day)