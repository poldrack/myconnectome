# -*- coding: utf-8 -*-
"""
Utils for network stats

Created on Sun Mar 29 12:44:11 2015

@author: poldrack
"""

import numpy

def participation_index(W,Ci):
    """
    based on participation_coefficient.m from MATLAB
    Brain Connectivity Toolbox
    W: adjacency matrix
    Ci: community labels
    
    """
    

    ## n=length(W);                        %number of vertices
    n=len(Ci)
    ## Ko=sum(W,2);                        %(out)degree
    Ko=numpy.sum(W,1)
    
    ## Gc=(W~=0)*diag(Ci);                 %neighbor community affiliation
    Gc=(W>0).dot(numpy.diag(Ci))
    
    ## Kc2=zeros(n,1);                     %community-specific neighbors
    Kc2=numpy.zeros(n)
    
    ## for i=1:max(Ci);
    ##    Kc2=Kc2+(sum(W.*(Gc==i),2).^2);
    ## end
    for i in numpy.unique(Ci)[1:]:
        Kc2=Kc2 + (numpy.sum(W*(Gc==i),1)**2)
        
    ## P=ones(n,1)-Kc2./(Ko.^2);
    P=numpy.ones(n)-Kc2/(Ko**2)
    P[Ko==0]=0                          #%P=0 if for nodes with no (out)neighbors
    return P


def get_hubs(degree,P):
    """
    hub definition based on:
     http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0001049
    'Considering only high-degree vertices (i.e. vertices with a degree at least one standard deviation above the network mean) we classify vertices with a participation coefficient P<0.3 as provincial hubs, and nodes with P>0.3 as connector hubs.'
    """
    meandeg=numpy.mean(degree)
    stddeg=numpy.std(degree)
    cutoff=meandeg+stddeg
    hubs=numpy.zeros(len(degree))
    hubs[(degree>cutoff)*(P<0.3)]=1  # provincial hub
    hubs[(degree>cutoff)*(P>0.3)]=2  # connector hub
    return hubs

"""
from https://groups.google.com/forum/#!topic/networkx-discuss/ycxtVuEqePQ
"""

import networkx as nx
import numpy as np

def nx_is_weighted(graph):
    #print 'I hope this is an unweighted graph...'
    return False

def dist_inv_wei(graph):
    #DISTANCE_WEI_INV       Distance matrix
    #
    #  mat = distance_wei(graph);
    #
    #   The distance matrix contains lengths of shortest paths between all
    #   pairs of nodes. An entry (u,v) represents the length of shortest path
    #   from node u to node v. The average shortest path length is the 
    #   characteristic path length of the network.
    #
    #   Input:      graph,      Directed/undirected graph.
    #
    #   Output:     mat,      distance (shortest weighted path) matrix 
    #
    #
    #   Modification history:
    #   2007: original
    #   2009-08-04: min() function vectorized
    #   Python Conversion Jean-Christophe KETZINGER, INSERM UMRS678, 2013
    #   
    #   Algorithm: Dijkstra's algorithm.
    #
    #   Reference:
    #   Mika Rubinov, UNSW/U Cambridge, 2007-2012.
    #   Rick Betzel and Andrea Avena, IU, 2012
    path_length=nx.all_pairs_dijkstra_path_length(graph, weight='weight');
    mat=[];
    sortedcol=keysort(path_length);
    zerospos=[];
    for idx,col in enumerate(sortedcol):
        keys=keysort(col);
        line=[];
        for (k,v) in enumerate(keys):
            if (v!=0):
                line.append(1.0/v);
            else:
                line.append(v);
        if (len(line)==1):
            val=np.argmax(sorted(graph.nodes())==col.keys()[0])
            zerospos.append(val);
        else:
            mat.append(line);
    mat=np.array(mat);
    for i,val in enumerate(zerospos):
        mat=np.insert(mat, val, 0, axis=0);
        mat=np.insert(mat, val, 0, axis=1);
    return mat;

def efficiency(G,wei_loc=None):
    #GLOBAL_EFFICIENCY     Get the global efficiency value
    #
    #   efficiency_value = efficiency(G)
    #
    #   The global efficiency is the average of inverse shortest path length,
    #   and is inversely related to the characteristic path length.
    #
    #   Inputs: G, The graph on which we want to compute the efficiency
    #
    #   Output: efficiency_value, the value of the efficiency
    #
    #   Algorithm: algebraic path count
    #
    #   Reference: Latora and Marchiori (2001) Phys Rev Lett 87:198701.
    #                Onnela et al. (2005) Phys Rev E 71:065103
    #                Rubinov M, Sporns O (2010) NeuroImage 52:1059-69
    #
    #   Mika Rubinov, UNSW, 2008-2010
    #   Jean-Christophe KETZINGER, INSERM UMRS678 PARIS, 2013
    #
    #   Modification history:
    #   2010: Original version from BCT (Matlab)
    #   Python Conversion Jean-Christophe KETZINGER, INSERM UMRS678, 2013
    avg = 0.0;
    graph=G.copy();
    n = len(graph);
    if nx_is_weighted(graph):#efficiency_wei
        for (u,v,d) in graph.edges(data=True):
            d['weight']=1/(d['weight']*1.0);#Compute the connection-length matrix
        if (wei_loc==None):     
            for node in graph:
                path_length=nx.single_source_dijkstra_path_length(graph, node);
                avg += sum(1.0/v for v in path_length.values() if v !=0);
            avg *= 1.0/(n*(n-1));
        else:
            mat=dist_inv_wei(graph);
            print mat;
            e=np.multiply(mat,wei_loc)**(1/3.0);
            e_all=np.matrix(e).ravel().tolist();
            avg = sum(e_all[0]);
            avg *= 1.0/(n*(n-1));#local efficiency
    else:#efficiency_bin
        for node in graph:
            path_length=nx.single_source_shortest_path_length(graph, node);
            avg += sum(1.0/v for v in path_length.values() if v !=0);
        avg *= 1.0/(n*(n-1));
    return avg;

def local_efficiency(G):
    #LOCAL_EFFICIENCY     Get the local efficiency vector
    #
    #   efficiency_vector = local_efficiency(G)
    #
    #   This function compute for each node the efficiency of its 
    #   immediate neighborhood and is related to the clustering coefficient.
    #
    #   Inputs: G,      The graph on which we want to compute the local efficiency
    #
    #   Output: efficiency_vector,  return as many local efficiency value as there are
    #   nodes in our graph
    #
    #   Algorithm: algebraic path count
    #
    #   Reference: Latora and Marchiori (2001) Phys Rev Lett 87:198701.
    #   Mika Rubinov, UNSW, 2008-2010
    #   Jean-Christophe KETZINGER, INSERM UMRS678 PARIS, 2013
    #
    #   Modification history:
    #   2010: Original version from BCT (Matlab)
    #   Python Conversion Jean-Christophe KETZINGER, INSERM UMRS678, 2013
    
    efficiency_vector = [];
    for node in G:
        neighbors = G.neighbors(node);#Get the neighbors of our interest node
        neighbors = np.sort(neighbors, axis=None);#sort the neighbors list
        SG=nx.subgraph(G, neighbors);#Create the subgraph composed exclusively with neighbors
        if (len(neighbors)>2):#assert that the subragh is not only one edge
            if nx_is_weighted(SG):
                GuV=[];
                GVu=[];
                GWDegree=nx.to_numpy_matrix(G);
                print GWDegree;
                for neighbor in neighbors:
                    GuV.append(GWDegree[node,neighbor]);
                    GVu.append(GWDegree[neighbor,node]);
                GVuGuV=(np.outer(np.array(GVu),np.array(GuV).T));
                node_efficiency=efficiency(SG,GVuGuV);
                efficiency_vector.append(node_efficiency); #compute the global efficiency of this subgraph
            else:
                efficiency_vector.append(efficiency(SG));
        else:
            efficiency_vector.append(0.0);#or set it's efficiency value to 0
    return efficiency_vector;
