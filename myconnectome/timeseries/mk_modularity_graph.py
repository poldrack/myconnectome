# -*- coding: utf-8 -*-
"""
Make graph file for Tues/Thurs effects on within and between module connectivity

Created on Sun May  3 06:55:17 2015

@author: poldrack
"""


import os,sys
import numpy
import networkx
from myconnectome.utils.load_dataframe import load_dataframe

basedir=os.environ['MYCONNECTOME_DIR']

thresh=0.1

winmod=load_dataframe(os.path.join(basedir,'timeseries/out.dat.wincorr_netdat.txt'),thresh=1.0)
bwmod=load_dataframe(os.path.join(basedir,'timeseries/out.dat.bwcorr_netdat.txt'),thresh=1.0)

nicenames={'16_Parieto_Occipital':'ParietoOccip',
 '4.5_Visual_1':'V1',
 '9_Cingulo_opercular':'CingOperc',
 '2_Visual_2':'V2',
 '8_Salience':'Salience',
 '1_Default':'Default',
 '11.5_Fronto_Parietal_2':'FPother',
 '7_Ventral_Attention':'VentAttn',
 '5_Dorsal_Attention':'DorsAttn',
 '10_Somatomotor':'Somatomotor',
 '15_Medial_Parietal':'MedParietal',
 '3_Fronto_Parietal':'FrontoParietal'
}

G=networkx.Graph()
for w in winmod.iterkeys():
    key=w[0].replace(':','_').replace('-Other','_Other').replace('Frontal-Parietal','Frontal_Parietal').replace('Parieto-Occipital','Parieto_Occipital').replace('Cingulo-opercular','Cingulo_opercular')
    if not G.has_node(key):
        if winmod.has_key((w[0],'modularity_weighted')):
            G.add_node(key, weight=abs(winmod[(w[0],'modularity_weighted')][2]))
        else:
            G.add_node(key)
        G.node[key]['posneg']=int(winmod[(w[0],'modularity_weighted')][2]>0)
        G.node[key]['nicename']=nicenames[key]



for b in bwmod.iterkeys():
    if not b[1]=='modularity_weighted' or bwmod[b][0]>thresh:
        continue
    key=b[0].replace('Parieto_occipital','Parieto_Occipital').replace('Frontoparietal','Fronto_Parietal').replace('Fronto_Parietal_1','Fronto_Parietal').replace('Frontal-Parietal','Frontal_Parietal').replace('-Other','_Other').replace('Parieto-Occipital','Parieto_Occipital').replace('Cingulo-opercular','Cingulo_opercular')
    key_s=key.split('-')
    G.add_edge(key_s[0],key_s[1],weight=abs(bwmod[b][2]))
    G.edge[key_s[0]][key_s[1]]['posneg']=int(bwmod[b][2]>0)
    
networkx.write_graphml(G,os.path.join(basedir,'timeseries/modularity_winbw.graphml'))

G=networkx.Graph()
for w in winmod.iterkeys():
    key=w[0].replace(':','_').replace('-Other','_Other').replace('Frontal-Parietal','Frontal_Parietal').replace('Parieto-Occipital','Parieto_Occipital').replace('Cingulo-opercular','Cingulo_opercular')
    if not G.has_node(key):
        if winmod.has_key((w[0],'efficiency_weighted')):
            G.add_node(key, weight=abs(winmod[(w[0],'efficiency_weighted')][2]))
        else:
            G.add_node(key)
        G.node[key]['posneg']=int(winmod[(w[0],'efficiency_weighted')][2]>0)
        G.node[key]['nicename']=nicenames[key]



for b in bwmod.iterkeys():
    if not b[1]=='efficiency_weighted' or bwmod[b][0]>thresh:
        continue
    key=b[0].replace('Parieto_occipital','Parieto_Occipital').replace('Frontoparietal','Fronto_Parietal').replace('Fronto_Parietal_1','Fronto_Parietal').replace('Frontal-Parietal','Frontal_Parietal').replace('-Other','_Other').replace('Parieto-Occipital','Parieto_Occipital').replace('Cingulo-opercular','Cingulo_opercular')
    key_s=key.split('-')
    G.add_edge(key_s[0],key_s[1],weight=abs(bwmod[b][2]))
    G.edge[key_s[0]][key_s[1]]['posneg']=int(bwmod[b][2]>0)
    
networkx.write_graphml(G,os.path.join(basedir,'timeseries/efficiency_winbw.graphml'))