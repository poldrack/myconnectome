"""
mk graph showing relations between differen variables
"""

#import pydot
import networkx as nx
import re
import os,glob
import numpy

basedir=os.environ['MYCONNECTOME_DIR']

filter_negatives=False
exclude_metab=False
exclude_metab_metab=True
exclude_gene_gene=True
filter_gene_modules=False # only include first cluster in each module
thresh=0.05 #0.1000000001
degree_thresh=1

use_infomap=True

exclude_unenriched=False
exclude_classes=['fd','psoriasis','pindex','fullmetab','bwcorr']
exclude_pairs=['metab_metab','wgcna_wgcna']
def load_dataframe(filename,thresh=0.1):
    # return p value, t stat, and correlation
    f=open(filename)
    header=f.readline()
    lines=f.readlines()
    f.close()
    data={}
    for l in lines:
        l_fixed=[]
        in_quotes=False
        for i in range(len(l)):
            if l[i]=='"':
                if in_quotes:
                    in_quotes=False
                else:
                    in_quotes=True
            if l[i]==' ' and not in_quotes:
                l_fixed.append('\t')
            else:
                l_fixed.append(l[i])
        l_fixed=''.join(l_fixed).replace('"','')
        l_s=[i.replace('"','') for i in l_fixed.strip().split('\t')]
        try:
         if float(l_s[-1])<thresh:
            #print l_s
            data[(l_s[1],l_s[2])]=[float(l_s[-1]),float(l_s[4]),float(l_s[3])]
        except:
            pass
    return data

cluster_names=['ME%d'%int(i.strip().split()[0]) for i in open(os.path.join(basedir,'rna-seq/WGCNA/module_descriptions.txt')).readlines()]
cluster_terms=[' '.join(i.strip().split()[1:]) for i in open(os.path.join(basedir,'rna-seq/WGCNA/module_descriptions.txt')).readlines()]
cluster_dict={}
for i in range(len(cluster_names)):
    cluster_dict[cluster_names[i]]=cluster_terms[i]

metab_names=['C%d'%i for i in range(1,16)]
metab_terms=[i.strip() for i in open(os.path.join(basedir,'metabolomics/apclust_descriptions.txt')).readlines()]
metab_dict={}
for i in range(len(metab_names)):
    metab_dict[metab_names[i]]=metab_terms[i]

files_to_load=list(set(glob.glob(os.path.join(basedir,'timeseries/out*.txt'))))

power_network_names={-1:'none',0:'none',1:'DefaultMode',2:'Visual-II',3:'Fronto-parietal',4.5:'Visual-I',
                     5:'DorsalAttn-I',7:'VentralAttn',8:'Salience',9:'Cingulo-opercular',
                     10:'Somatomotor',11.5:'FPOther',15:'MedialParietal',16:'Parieto-occipital'}
node_shapes={'metab':'box','wgcna':'ellipse','food':'triangle','wincorr':'diamond','behav':'hexagon','falff':'invtriangle',
             'netdat':'trapezium'}
node_classes={'metab':1,'wgcna':2,'food':3,'wincorr':4,'behav':5,'falff':6,'netdat':7,'bwcorr':8,'immport':9,'fullmetab':10,
              'fd':11}

behav_terms={'panas.positive':'Positive mood','panas.negative':'Negative mood','panas.fatigue':'Fatigue','afterscan.Anxietyduringscan':'Anxiety during scan',
             'afterscan.diastolic':'Diastolic BP after scan','afterscan.pulse':'Pulse after scan','afterscan.systolic':'Systolic BP after scan',
             'morning.Sleepquality':'Self-rated sleep quality','morning.Soreness':'Soreness','prevevening.Alcohol':'Alcohol intake (previous evening)',
             'prevevening.Guthealth':'Gut health (previous day)','prevevening.Psoriasisseverity':'Psoriasis severity (previous day)',
             'prevevening.Stress':'Stress (previous day)', 'prevevening.Timespentoutdoors':'Time spent outdoors (previous day)',
             'TuesThurs':'Thursday vs. Tuesday', 'temp.mean':'Mean daily temp',"email.LIWCcdi":'Email content-dynamic index',
             "email.LIWCnegemo":'Email negative emotion',"email.LIWCposemo":'Email positive emotion','zeo.zq':'ZEO zq'}

data={}
graph = nx.Graph()
shell=[]
for i in range(1,8):
    shell.append([])

for filename in files_to_load:
    f=os.path.basename(filename).replace('out.dat.','').replace('.txt','')
    data[f]=load_dataframe(filename,thresh)

    if f in exclude_pairs:
        print 'excluding',f
        continue
    datatypes=f.split('_')
    if len(data[f])<1:
        print 'no significant results for',f
        continue
    
    if 'netdat' in datatypes:
        continue
    
    for k in data[f].keys():
        print k
        if data[f][k][1]<0 and filter_negatives:
            continue
        ktuple=k
        if datatypes[0] in exclude_classes or datatypes[1] in exclude_classes:
            print 'excluding',f
            continue
        
        if filter_gene_modules and 'wgcna' in datatypes:
            dt=[False,False]
            if datatypes[0]=='wgcna':
                dt[0]=True
            if datatypes[1]=='wgcna':
                dt[1]=True
        
        k=[i.replace(',','').replace('"','') for i in list(k)]
        print k
        nodenames=[datatypes[0]+'-'+k[0],datatypes[1]+'-'+k[1]]

        exclude=False
        for x in range(2):
            name=u'%s'%re.sub(r'[^\x00-\x7F]+',' ', nodenames[x]).replace('"','').replace('&','')
            print name
            if name.find('no enrichment')>-1 and exclude_unenriched:
                    exclude=True
            nodelabel=''.join(name.split('-')[1:]).replace('"','').replace('_NIST','').split(':')[0]
            print name,nodelabel
            if datatypes[x]=='wincorr':
                nodelabel=power_network_names[float(nodelabel)]
                print 'wincorr:',nodelabel
            if datatypes[x]=='wgcna':
                nodelabel=cluster_dict[nodelabel]+' ('+nodelabel.replace('mod','').replace('clust','')+')'
            if datatypes[x]=='metab':
                nodelabel=metab_dict[nodelabel]+' ('+nodelabel+')'
            if datatypes[x]=='behav':
                nodelabel=behav_terms[nodelabel].replace(' (previous evening)','').replace(' (previous day)','')
                
            if not graph.has_node(name):
                graph.add_node(name)
                graph.node[name]['label']=nodelabel
                graph.node[name]['nodeclass']=node_classes[datatypes[x]]
                print name,graph.node[name]
                #shell[node_classes[datatypes[x]]-1].append(name)
            nodenames[x]=name
        if not exclude:
                graph.add_edge(nodenames[0],nodenames[1],attr_dict={'pval':data[f][ktuple][0],'tval':data[f][ktuple][1],'rval':data[f][ktuple][2]})
                print 'edge:',nodenames[0],nodenames[1]


degree=graph.degree()
for i in degree.iterkeys():
    if degree[i]<1:
        graph.remove_node(i)


#h=nx.hits(graph)[0]
#for k in h.iterkeys():
#    graph.node[k]['hub']=h[k]
    
#for k in graph.obj_dict['nodes'].iterkeys():
#    print graph.obj_dict['nodes'][k]
print 'writing graph...'
#graph.write_pdf('graph.pdf')
if filter_negatives:
    filt='_posonly'
else:
    filt=''
if exclude_metab:
    filt=filt+'_nometab'
if degree_thresh>1:
    filt=filt+'degree%d'%degree_thresh
    for n in graph.nodes():
        if graph.degree(n)<degree_thresh:
            graph.remove_node(n)

cc=nx.connected_components(graph)
nodes_to_remove=[]
for component in cc:
    if len(component)<3:
        for node in component:
            nodes_to_remove.append(node)
for node in nodes_to_remove:
            graph.remove_node(node)

nx.write_graphml(graph,'/tmp/tmp.graphml')

import igraph
G=igraph.read('/tmp/tmp.graphml')

if use_infomap:
    c=G.community_infomap()
    infomap_ext='_infomap'
else:
    c=G.community_multilevel()
    infomap_ext='multilevel'

labels=c.membership
print 'modularity:',c.modularity

for i in range(len(G.vs)):
    graph.node[G.vs[i]['id']]['module']=labels[i]


nx.write_gexf(graph,os.path.join(basedir,'timeseries/graph_thresh%.02f%s%s.gexf'%(thresh,filt,infomap_ext)))
nx.write_gml(graph,os.path.join(basedir,'timeseries/graph_thresh%.02f%s%s.gml'%(thresh,filt,infomap_ext)))
nx.write_graphml(graph,os.path.join(basedir,'timeseries/graph_thresh%.02f%s%s.graphml'%(thresh,filt,infomap_ext)))

for i in numpy.unique(labels):
    print ''
    print 'module',i
    for n in graph.nodes():
        if graph.node[n]['module']==i:
            print n
