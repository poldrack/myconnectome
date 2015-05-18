"""
mk adjmtx files for bct analysis
"""


import numpy
import os,sys
import networkx

import scipy.stats
import time

def r_to_z(r):
    # fisher transform
    z=0.5*numpy.log((1.0+r)/(1.0-r))
    z[numpy.where(numpy.isinf(z))]=0
    z[numpy.where(numpy.isnan(z))]=0
    
    return z


def z_to_r(z):
    # inverse transform
    return (numpy.exp(2.0*z) - 1)/(numpy.exp(2.0*z) + 1)



def get_apl(G):
    """
    compute average path length for a disconnected graph
    """
    
    apls=[]
    for g in networkx.connected_component_subgraphs(G):
        apls.append(networkx.average_shortest_path_length(g))
    return numpy.mean(apls)

try:
    sess=int(sys.argv[1])
    edge_density=float(sys.argv[2])
except:
    sess=83
    edge_density=0.005

infile='/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/corrdata.npy'
outfile='/scratch/01329/poldrack/selftracking/adjmtx_files/adjmtx_%02d_%.04f.txt'%(sess,edge_density)
corrfile='/scratch/01329/poldrack/selftracking/corrdata_files/corrdata_sess%02d.txt'%sess


data=numpy.load(infile)

data[numpy.isnan(data)]=0
adjsize=630
nsess=data.shape[0]

utr=numpy.triu_indices(adjsize,1)
alldata=[]

#for sess in range(data.shape[0]):
if 1:
    print 'processing session',sess+1
    thresh=scipy.stats.scoreatpercentile(data[sess,:],100.0 - 100.0*edge_density)

    corr=numpy.zeros((adjsize,adjsize))
    corr[utr]=data[sess,:]
    corr=corr+corr.T

    adj=numpy.zeros((adjsize,adjsize))
    subthresh=data[sess,:] < thresh
    thrdata=data[sess,:]
    thrdata[subthresh]=0
    adj[utr]=thrdata
    adj=adj+adj.T


    numpy.savetxt(outfile,adj)
    numpy.savetxt(corrfile,corr)
    
    graph=networkx.from_numpy_matrix(adj)
    gfile='/scratch/01329/poldrack/selftracking/graph_files/sess%03d_%.04f.net'%(sess,edge_density)
    networkx.write_pajek(graph,gfile)
    time.sleep(0.1)
    
    # need to remove first line with NetworkX comment
    l=open(gfile).readlines()
    f=open(gfile,'w')
    for i in l:
        if i.find('NetworkX')<0:
            f.write(i)
    f.close()
    
