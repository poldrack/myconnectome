"""
compute network statistics for each session
"""

import os,sys
import numpy
import scipy.stats
import igraph
import efficiency
import networkx
import nibabel.gifti.giftiio
import nibabel
import powerlaw

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

     
edge_density=float(sys.argv[1])
basedir='/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses'

outdir=basedir

adjsize=634
utr=numpy.triu_indices(adjsize,1)
datafile='/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/corrdata.npy'
data=numpy.load(datafile)
threshdata=numpy.zeros(data.shape)

localeff=numpy.zeros((data.shape[0],adjsize))
nodaleff=numpy.zeros((data.shape[0],adjsize))
degree=numpy.zeros((data.shape[0],adjsize))
gcsize=numpy.zeros(data.shape[0])
hubs=numpy.zeros((data.shape[0],adjsize))
eff=numpy.zeros(data.shape[0])
clust=numpy.zeros(data.shape[0])
Gclust=numpy.zeros(data.shape[0])
modularity_multi=numpy.zeros(data.shape[0])
modularity_infomap=numpy.zeros(data.shape[0])
power_exp=numpy.zeros(data.shape[0])
meansw=numpy.zeros(data.shape[0])
apl=numpy.zeros(data.shape[0])

pi=numpy.zeros((data.shape[0],adjsize))
bc=numpy.zeros((data.shape[0],adjsize))
cc=numpy.zeros((data.shape[0],adjsize))
rcc_at_cutoff=numpy.zeros(data.shape[0])

for i in range(data.shape[0]):
    thresh=scipy.stats.scoreatpercentile(data[i,:],100.0 - 100.0*edge_density)
    threshdata[i,:]=data[i,:]>thresh
    adj=numpy.zeros((adjsize,adjsize))
    adj[utr]=threshdata[i,:]
    graph=networkx.from_numpy_matrix(adj)
    clust[i]=networkx.average_clustering(graph)
    eff[i] = efficiency.efficiency(graph)
    localeff[i,:]=efficiency.local_efficiency(graph)
    degree[i,:]=[graph.degree(j) for j in range(adjsize)]
    
    cc[i,:]=[networkx.closeness_centrality(graph,j) for j in range(adjsize)]
    bc[i,:]=networkx.betweenness_centrality(graph,j).values()
    G=networkx.connected_component_subgraphs(graph)[0]
    results=powerlaw.Fit(G.degree().values())
    power_exp[i]= results.power_law.alpha
    
    gg=igraph.Graph.Adjacency(adj.tolist()).as_undirected()
    #networkx.write_pajek(graph,'/Users/poldrack/data/selftracking/rsfmri/graphs/sess%03d.net'%i)
    modclust_multi=gg.community_multilevel() #gg.community_infomap()
    modularity_multi[i]=modclust_multi.modularity
    modclust_infomap=gg.community_infomap()
    modularity_infomap[i]=modclust_infomap.modularity
    
    sizethresh=2
    labels=numpy.array(modclust_infomap.membership)
    for x in numpy.unique(labels):
        if numpy.sum(labels==x)<sizethresh:
            labels[labels==x]=0
    pi[i,:]=participation_index(adj,labels)
    rcc=networkx.rich_club_coefficient(graph,normalized=True)
    rcc_cutoff=int(numpy.ceil(numpy.mean(degree[i,:]) + numpy.std(degree[i,:])))
    rcc_at_cutoff[i]=rcc[rcc_cutoff]
    hubs[i,:]=get_hubs(degree[i,:],pi[i,:])
    print i,modularity_infomap[i],eff[i]

    # get small world coefficient
    #from the clustering coefficient (CC) and the average path length (PL) =
    # CC(actual network)/CC(random graph) divided by PL(actual network)/PL(random graph)
    # use just the largest connected component
    gcsize[i]=G.number_of_nodes()
    apl[i]=networkx.average_shortest_path_length(G)
    Gclust[i]=networkx.average_clustering(G)
    if 0:
        
        
        sw=[]

        for k in range(36):
            try:
                rand=networkx.random_degree_sequence_graph(G.degree().values(),tries=10)
                Grand=networkx.connected_component_subgraphs(rand)[0]

            except:
                print 'problem on round',k
                continue
            print k
            sw.append((Gclust[i]/networkx.average_clustering(Grand))/(apl[i]/networkx.average_shortest_path_length(Grand)))

        if len(sw)>0:
            meansw[i]=numpy.mean(sw)

# save data to text file

mean_cc=numpy.mean(cc,1)
mean_bc=numpy.mean(bc,1)
mean_pi=numpy.mean(pi,1)
mean_localeff=numpy.mean(localeff,1)

sessdata=numpy.vstack((eff,mean_localeff,clust,modularity_infomap,modularity_multi,power_exp,rcc_at_cutoff,mean_cc,mean_bc,mean_pi,gcsize,apl))
varnames=['eff','mean_localeff','clust','modularity_infomap','modularity_multi','power_exp','rcc_at_cutoff','mean_cc','mean_bc','mean_pi','gcsize','apl']
vnames=[i+'_%0.3f'%edge_density for i in varnames]

numpy.savetxt(os.path.join(outdir,'netstats_%0.3f.txt'%edge_density),sessdata.T,header=' '.join(vnames))


# save some data to gii files

lh=nibabel.gifti.giftiio.read('/corral-repl/utexas/poldracklab/data/selftracking/parcellation/L_84_parcellation.func.gii')
rh=nibabel.gifti.giftiio.read('/corral-repl/utexas/poldracklab/data/selftracking/parcellation/R_84_parcellation.func.gii')
lh_labels=lh.darrays[0].data.copy()
rh_labels=rh.darrays[0].data.copy()
labeled_regions_lh=numpy.unique(lh_labels)
labeled_regions_rh=numpy.unique(rh_labels)

lhimg=nibabel.gifti.GiftiImage()
rhimg=nibabel.gifti.GiftiImage()

darray_degree=numpy.zeros(lh.darrays[0].data.shape,dtype=numpy.float32)
darray_bc=numpy.zeros(lh.darrays[0].data.shape,dtype=numpy.float32)
darray_cc=numpy.zeros(lh.darrays[0].data.shape,dtype=numpy.float32)
darray_pi=numpy.zeros(lh.darrays[0].data.shape,dtype=numpy.float32)
darray_eff=numpy.zeros(lh.darrays[0].data.shape,dtype=numpy.float32)
darray_provhubs=numpy.zeros(lh.darrays[0].data.shape,dtype=numpy.float32)
darray_connhubs=numpy.zeros(lh.darrays[0].data.shape,dtype=numpy.float32)

for j in range(1,len(labeled_regions_lh)):
            darray_degree[lh_labels==labeled_regions_lh[j]]=numpy.mean(degree[:,j])
            darray_bc[lh_labels==labeled_regions_lh[j]]=numpy.mean(bc[:,j])
            darray_cc[lh_labels==labeled_regions_lh[j]]=numpy.mean(cc[:,j])
            darray_pi[lh_labels==labeled_regions_lh[j]]=numpy.mean(pi[:,j])
            darray_eff[lh_labels==labeled_regions_lh[j]]=numpy.mean(localeff[:,j])
            darray_provhubs[lh_labels==labeled_regions_lh[j]]=numpy.mean(hubs[:,j]==1)
            darray_connhubs[lh_labels==labeled_regions_lh[j]]=numpy.mean(hubs[:,j]==2)

lhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_degree,intent=lh.darrays[0].intent,datatype=lh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'mean_degree'}))

lhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_bc,intent=lh.darrays[0].intent,datatype=lh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'mean_betweenness_centrality'}))

lhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_cc,intent=lh.darrays[0].intent,datatype=lh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'mean_closeness_centrality'}))

lhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_pi,intent=lh.darrays[0].intent,datatype=lh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'mean_participation_index'}))

lhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_eff,intent=lh.darrays[0].intent,datatype=lh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'mean_local_efficiency'}))

lhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_provhubs,intent=lh.darrays[0].intent,datatype=lh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'P_provincial_hub'}))

lhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_connhubs,intent=lh.darrays[0].intent,datatype=lh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'P_connector_hub'}))


nibabel.gifti.giftiio.write(lhimg,os.path.join(outdir,'lh_netstats_%0.3f.func.gii'%edge_density))



# do right hemisphere
darray_degree=numpy.zeros(rh.darrays[0].data.shape,dtype=numpy.float32)
darray_bc=numpy.zeros(rh.darrays[0].data.shape,dtype=numpy.float32)
darray_cc=numpy.zeros(rh.darrays[0].data.shape,dtype=numpy.float32)
darray_pi=numpy.zeros(rh.darrays[0].data.shape,dtype=numpy.float32)
darray_eff=numpy.zeros(rh.darrays[0].data.shape,dtype=numpy.float32)
darray_provhubs=numpy.zeros(rh.darrays[0].data.shape,dtype=numpy.float32)
darray_connhubs=numpy.zeros(rh.darrays[0].data.shape,dtype=numpy.float32)

# include offset for LH regions
for j in range(1,len(labeled_regions_rh)):
            darray_degree[rh_labels==labeled_regions_rh[j]]=numpy.mean(degree[:,j+len(labeled_regions_lh)])
            darray_bc[rh_labels==labeled_regions_rh[j]]=numpy.mean(bc[:,j+len(labeled_regions_lh)])
            darray_cc[rh_labels==labeled_regions_rh[j]]=numpy.mean(cc[:,j+len(labeled_regions_lh)])
            darray_pi[rh_labels==labeled_regions_rh[j]]=numpy.mean(pi[:,j+len(labeled_regions_lh)])
            darray_eff[rh_labels==labeled_regions_rh[j]]=numpy.mean(localeff[:,j+len(labeled_regions_lh)])
            darray_provhubs[rh_labels==labeled_regions_rh[j]]=numpy.mean(hubs[:,j+len(labeled_regions_lh)]==1)
            darray_connhubs[rh_labels==labeled_regions_rh[j]]=numpy.mean(hubs[:,j+len(labeled_regions_lh)]==2)

rhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_degree,intent=rh.darrays[0].intent,datatype=rh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'mean_degree'}))

rhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_bc,intent=rh.darrays[0].intent,datatype=rh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'mean_betweenness_centrality'}))

rhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_cc,intent=rh.darrays[0].intent,datatype=rh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'mean_closeness_centrality'}))

rhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_pi,intent=rh.darrays[0].intent,datatype=rh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'mean_participation_index'}))

rhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_eff,intent=rh.darrays[0].intent,datatype=rh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'mean_local_efficiency'}))

rhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_provhubs,intent=rh.darrays[0].intent,datatype=rh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'P_provincial_hub'}))

rhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_connhubs,intent=rh.darrays[0].intent,datatype=rh.darrays[0].datatype,ordering='F',meta={'AnatomicalStructurePrimary':'CortexLeft','Name':'P_connector_hub'}))


nibabel.gifti.giftiio.write(rhimg,os.path.join(outdir,'rh_netstats_%03f.func.gii'%edge_density))

