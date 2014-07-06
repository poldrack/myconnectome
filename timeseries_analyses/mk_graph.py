"""
mk graph showing relations between differen variables
"""

import pydot
import networkx as nx
import re

filter_negatives=False
thresh=0.05

def load_dataframe(filename,thresh=0.05):
	# return p value, t stat, and correlation
	f=open(filename)
	header=f.readline()
	lines=f.readlines()
	f.close()
	data={}
	for l in lines:
		l_s=[i.replace('"','') for i in l.strip().split()]
		try:
		 if float(l_s[-1])<thresh:
			#print l_s
			data[(l_s[1],l_s[2])]=[float(l_s[-1]),float(l_s[4]),float(l_s[3])]
		except:
			pass
	return data

files_to_load=['falff_falff','falff_pheno','food_metab','reactome_food','metab_falff',
   'metab_netdat','metab_wincorr','netdat_pheno','netdat_wincorr','pheno_metab','pheno_reactome',
   'reactome_falff','reactome_metab','reactome_netdat','reactome_wincorr','wincorr_falff',
   'wincorr_pheno','wincorr_wincorr']

#files_to_load=['metab_metab']

power_network_names={-1:'none',0:'none',1:'DM',2:'Vis2',3:'FP',4.5:'Vis1',5:'DA1',6:'DA2',7:'VA-Lang',8:'Sal',9:'CO',10:'SOM',11.5:'FPother',15:'PEpisRet',16:'PO'}

node_shapes={'metab':'box','reactome':'ellipse','food':'triangle','wincorr':'diamond','pheno':'hexagon','falff':'invtriangle','netdat':'trapezium'}
node_classes={'metab':1,'reactome':2,'food':3,'wincorr':4,'pheno':5,'falff':6,'netdat':7}

reactome_labels=['Apoptosis',
	'Binding_and_Uptake_of_Ligands_by_Scavenger_Receptors',
	'Cell_Cycle',
	'CellCell_communication',
	'Cellular_responses_to_stress',
	'Chromatin_organization',
	'Circadian_Clock',
	'Developmental_Biology',
	'Disease',
	'DNA_Repair',
	'DNA_Replication',
	'Extracellular_matrix_organization',
	'Gene_Expression',
	'Hemostasis',
	'Immune_System',
	'Meiosis',
	'Membrane_Trafficking',
	'Metabolism',
	'Metabolism_of_proteins',
	'Muscle_contraction',
	'Neuronal_System',
	'Organelle_biogenesis_and_maintenance',
	'Reproduction',
	'Signal_Transduction',
	'Transmembrane_transport_of_small_molecules']
reactome_short_labels={}
for l in reactome_labels:
	reactome_short_labels[l]=l
reactome_short_labels['Binding_and_Uptake_of_Ligands_by_Scavenger_Receptors']='Scavenger_uptake_binding'
reactome_short_labels['Cellular_responses_to_stress']='Cellular_stress'
reactome_short_labels['Extracellular_matrix_organization']='Extracellular_matrix'
reactome_short_labels['Organelle_biogenesis_and_maintenance']='Organelle function'
reactome_short_labels['Transmembrane_transport_of_small_molecules']='Transmembrane_transport'
reactome_short_labels['Neuronal_System']='Nervous_system'
reactome_short_labels['CellCell_communication']='Cell-cell_communication'
data={}
graph = nx.Graph()
shell=[]
for i in range(1,8):
	shell.append([])

for f in files_to_load:

	filename='/Users/poldrack/Dropbox/data/selftracking/timeseries_analyses/%s.out'%f
	data[f]=load_dataframe(filename,thresh)

	datatypes=f.split('_')
	if len(data[f])<1:
		print 'no significant results for',f
		continue
	for k in data[f].keys():
		if data[f][k][1]<0 and filter_negatives:
			continue
		ktuple=k
		k=[i.replace(',','').replace('"','') for i in list(k)]
		#print k
		#print k
		## if datatypes[0] in ['wincorr','falff']:
		## 	k[0]=power_network_names[float(k[0])]
		## if datatypes[1] in ['wincorr','falff']:
		## 	k[1]=power_network_names[float(k[1])]
		
		nodenames=[datatypes[0]+'-'+k[0],datatypes[1]+'-'+k[1]]
		badlevel=False
		for i in range(2):
			for level in ['0.025','0.075']:
				if nodenames[i].find(level)>-1:
					badlevel=True
		if badlevel:
			continue
		for x in range(2):
			name=u'%s'%re.sub(r'[^\x00-\x7F]+',' ', nodenames[x]).replace('"','').replace('&','')
			nodelabel=''.join(name.split('-')[1:]).replace('"','').replace('mean_pi','PI').replace('power_exp','EXP').replace('mean_','').replace('modularity_','MOD').replace('rcc_at_cutoff','RCC')
			if datatypes[x]=='wincorr':
				modnum=float(nodelabel.split('_')[0])
				nodelabel=power_network_names[modnum]+'-c'
			if datatypes[x]=='falff':
				modnum=float(nodelabel.split('_')[0])
				nodelabel=power_network_names[modnum]+'-f'
			if datatypes[x]=='reactome':
				nodelabel=reactome_short_labels[nodelabel]

			if not graph.has_node(name):
				graph.add_node(name)
				graph.node[name]['label']=nodelabel
				graph.node[name]['nodeclass']=node_classes[datatypes[x]]
				print name,graph.node[name]
				shell[node_classes[datatypes[x]]-1].append(name)
			nodenames[x]=name
		graph.add_edge(nodenames[0],nodenames[1],attr_dict={'pval':data[f][ktuple][0],'tval':data[f][ktuple][1],'rval':data[f][ktuple][2]})


sg=nx.connected_component_subgraphs(graph)
for g in sg:
	if g.number_of_nodes()<3:
			graph.remove_nodes_from(g.nodes())

nx.write_graphml(graph,'tmp.graphml')

import igraph
G=igraph.read('tmp.graphml')
c=G.community_infomap()
labels=c.membership

for i in range(len(G.vs)):
	graph.node[G.vs[i]['id']]['module']=labels[i]
	
#for k in graph.obj_dict['nodes'].iterkeys():
#	print graph.obj_dict['nodes'][k]
print 'writing graph...'
#graph.write_pdf('graph.pdf')
nx.write_gexf(graph,'graph__thresh%.02f.gexf'%thresh)

