"""
make table describing clusters
automatically grab DAVID annotations for each module

"""

import os
import glob
import numpy
from get_DAVID_annotation import *
import time

fdr_thresh=0.1  # include everything

basedir='/Users/poldrack/Dropbox/data/selftracking/rna-seq/WGCNA'
f=open(os.path.join(basedir,'hubgenes.txt'))
lines=[i.strip().split() for i in f.readlines()]
f.close()

genefiles=glob.glob(os.path.join(basedir,'MEs-thr8-rinreg-mod*-genes.txt'))
modules={}

do_annot=False
if do_annot:
    david_annot={}

max_num_annot=10

path_cats='KEGG_PATHWAY,REACTOME_PATHWAY,BIOCARTA,PANTHER_PATHWAY'
go_cats='GOTERM_BP_FAT'

for m in genefiles:
    modnum=int(os.path.basename(m).split('-')[3].replace('mod',''))
    if modnum==0:
        continue
    modules[modnum]={'go':[],'path':[]}
    f=open(m)
    genes=[i.strip() for i in f.readlines()]
    f.close()
    if do_annot:
        if not david_annot.has_key(modnum):
            david_annot[modnum]={}
        annot_go=get_DAVID_annotation(genes=genes,fdr_thresh=fdr_thresh,cats=go_cats)
        time.sleep(10)
        if len(annot_go)<max_num_annot:
             david_annot[modnum]['go']=annot_go
        else:
             david_annot[modnum]['go']=annot_go[:max_num_annot]
        annot_path=get_DAVID_annotation(genes=genes,fdr_thresh=fdr_thresh,cats=path_cats)
        time.sleep(10)
        if len(annot_path)<max_num_annot:
             david_annot[modnum]['path']=annot_path
        else:
             david_annot[modnum]['path']=annot_path[:max_num_annot]

david_annot_dict={}
for m in genefiles:
    modnum=int(os.path.basename(m).split('-')[3].replace('mod',''))
    if modnum==0:
        continue
    # convert simpleChartRecords into dict
    david_annot_dict[modnum]={'go':[],'path':[]}
    for type in ['go','path']:
      for a in david_annot[modnum][type]:
        david_annot_dict[modnum][type].append(dict(a))
        ngenes=a['listHits']
        fdr=a['benjamini']
        fe=a['foldEnrichment']
        
        if fdr<fdr_thresh:
            termname=a['termName']
            if termname.find('~')>-1:
                term_split=termname.split('~')
                annot='%s (%s)'%(term_split[1],term_split[0])

            elif termname.find(':')>-1:
                term_split=termname.split(':')
                if termname.find('REACT')>-1:
                	annot='%s (Reactome:%s)'%(term_split[1],term_split[0].replace('REACT_',''))
                elif termname.find('hsa')>-1:
                	annot='%s (KEGG:%s)'%(term_split[1],term_split[0])
                else:
                	annot='%s (%s)'%(term_split[1],term_split[0])
                
            else:
                annot=termname
                
            modules[modnum][type].append([annot,fdr,ngenes,fe])



# sort enriched pathways by FDR
modules_sorted={}
for m in modules.keys():
  modules_sorted[m]={'go':[],'path':[]}
  for type in ['go','path']:
    module_fdr=[]
    for i in modules[m][type]:
        module_fdr.append(i[1])
    idx=numpy.argsort(module_fdr)
    for i in idx:
        modules_sorted[m][type].append(modules[m][type][i])

    
modules=modules_sorted

f=open(os.path.join(basedir,'module_assignments.txt'))
lines=[i.strip() for i in f.readlines()]
f.close()
gene_assignments={}
for l in lines:
    l_s=l.strip().split()
    gene_assignments[l_s[0]]=int(l_s[1])
    
f=open(os.path.join(basedir,'hubgenes.txt'))
lines=[i.strip() for i in f.readlines()]
f.close()
hubgenes={}
ngenes={}
for l in lines:
    l_s=l.split(' ')
    if modules.has_key(int(l_s[0])):
        hubgenes[int(l_s[0])]=l_s[2:]
        ngenes[int(l_s[0])]=numpy.sum(numpy.array(gene_assignments.values())==int(l_s[0]))
  
      
f=open('/Users/poldrack/Dropbox/Documents/Papers/SelfTracking/automatic-tables/module_table_combined.txt','w')

    
modkeys=modules.keys()
modkeys.sort()

for m in modkeys:
    maxlen=numpy.min([3,numpy.max([len(modules[m]['go']),len(modules[m]['path'])])])+5
    for i in range(maxlen):
        if i==0:
            f.write('%d\t%d\t'%(m,ngenes[m]))
        else:
            f.write('\t\t')
        if len(modules[m]['path'])>i:
            f.write('%s\t%0.3f\t%0.1f\t'%(modules[m]['path'][i][0],modules[m]['path'][i][1],modules[m]['path'][i][3]))
        else:
            if i>0:
                f.write('\t\t\t')
            else:
                f.write('no pathways enriched\t\t\t')
                
        
        try:
            h=hubgenes[m][i]
        except:
            h=''

        if len(modules[m]['go'])>i:
            f.write('%s\t%0.3f\t%0.1f\t%s\n'%(modules[m]['go'][i][0],modules[m]['go'][i][1],modules[m]['go'][i][3],h))
        else:
            if i>0:
                f.write('\t\t\t%s\n'%h)
            else:
                f.write('no GO terms enriched\t\t\t%s\n'%h)
    f.write('\n')
f.close()


import cPickle

cPickle.dump(david_annot_dict,open('/Users/poldrack/Dropbox/data/selftracking/rna-seq/WGCNA/david_annot_combined.pkl','wb'))

