"""
get network stats
"""


import numpy
import os,sys
import scipy.stats
import igraph
import efficiency
import networkx
import powerlaw

from participation_index import *

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
    sess=0
    edge_density=0.05

infile='/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/corrdata.npy'
outfile='/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/netstats_corr/netstats_%02d_%0.3f.txt'%(sess,edge_density)

data=numpy.load(infile)

data[numpy.isnan(data)]=0
adjsize=634
nsess=data.shape[0]

utr=numpy.triu_indices(adjsize,1)
alldata=[]

#for sess in range(data.shape[0]):
if 1:
    print 'processing session',sess+1
    thresh=scipy.stats.scoreatpercentile(data[sess,:],100.0 - 100.0*edge_density)

    adj=numpy.zeros((adjsize,adjsize))
    adj[utr]=data[sess,:] > thresh

    graph=networkx.from_numpy_matrix(adj)
    # get giant component
    G=networkx.connected_component_subgraphs(graph)[0]

    # fit power law to entire graph degree distribution
    results=powerlaw.Fit(graph.degree().values())
    power_exp= results.power_law.alpha
    
    clust=networkx.average_clustering(graph)

    eff = efficiency.efficiency(graph)
    localeff=efficiency.local_efficiency(graph)
    
    degree=[graph.degree(j) for j in graph.nodes()]
    cc=numpy.mean(networkx.closeness_centrality(graph).values())

    bc=numpy.mean(networkx.betweenness_centrality(graph).values())
    gg=igraph.Graph.Adjacency(adj.tolist()).as_undirected()
    gg_G= gg.clusters().giant()
    
    modclust=gg_G.community_multilevel() #gg.community_infomap()
    modularity_multi=modclust.modularity

    sizethresh=2
    labels=numpy.array(modclust.membership)
    for x in numpy.unique(labels):
        if numpy.sum(labels==x)<sizethresh:
            labels[labels==x]=0

    #pi=participation_index(adj,labels)
    #mean_pi=numpy.mean(pi)
    
    try:
        rcc=networkx.rich_club_coefficient(G,normalized=True)
        rcc_cutoff=int(numpy.ceil(numpy.mean(degree) + numpy.std(degree)))
        rcc_at_cutoff=rcc[rcc_cutoff]
    except:
        rcc_at_cutoff=0.0

    # get small world coefficient
    #from the clustering coefficient (CC) and the average path length (PL) =
    # CC(actual network)/CC(random graph) divided by PL(actual network)/PL(random graph)
    # use just the largest connected component

    gcsize=G.number_of_nodes()
    apl=networkx.average_shortest_path_length(G)
    Gclust=networkx.average_clustering(G)



    sw=[]

    for i in range(36):
        try:
            rand=networkx.random_degree_sequence_graph(G.degree().values(),tries=10)
            Grand=networkx.connected_component_subgraphs(rand)[0]

        except:
            print 'problem on round',i
            continue
        print i
        sw.append((Gclust/networkx.average_clustering(Grand))/(apl/networkx.average_shortest_path_length(Grand)))

    if len(sw)>0:
        meansw=numpy.mean(sw)
    else:
        meansw=0


    alldata=numpy.array([modularity_multi,eff,cc,bc,clust,rcc_at_cutoff,apl,power_exp,meansw])
    numpy.savetxt(outfile,alldata)
