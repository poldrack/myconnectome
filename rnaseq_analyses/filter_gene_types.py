# -*- coding: utf-8 -*-
"""
filter genes from RNA-seq data
Created on Thu Apr 30 15:18:26 2015

@author: poldrack
"""

import os,glob
import numpy
from load_counts import *
import gtf_to_genes
import logging
import pandas as pd

def get_genes():
    logger = logging.getLogger("test")
    species_id, gtf_path, genes = gtf_to_genes.get_indexed_genes_for_identifier(
        '/Users/poldrack/data_unsynced/selftracking/vega/gtf.index',logger,'Homo_sapiens:59')
    return genes
        
        
def load_genetypes(genes):
    genetype={}
    for k in genes.keys():
        for g in genes[k]:
            for n in g.names:
                genetype[n]=g.gene_type
    # load vega updates
    f=open('/Users/poldrack/data_unsynced/selftracking/vega/vega_update.csv')
    header=f.readline()
    for l in f.readlines():
        l_s=l.strip().split(',')
        genename=l_s[0].replace('"','')
        genetype[genename]=l_s[1].replace('"','')
    return genetype

# load full dataset
counts,gene_names=load_counts('/Users/poldrack/data/selftracking/rna-seq/all_counts.txt')
c=numpy.array(counts)

try:
    genes
except:
    genes=get_genes()

try:
    genetype
except:
    genetype=load_genetypes(genes)
        


type_list={}
for t in list(set(genetype.values())):
    type_list[t]=[]

for g in gene_names:
    try:
        type_list[genetype[g]].append(g)
    except:
        print 'no',g


coding_gene_nums=[]      
coding_genes={} 
missing_genes=[] 

filter_types=['KNOWN_snoRNA',]
for i in range(len(gene_names)):
    if genetype.has_key(gene_names[i]):
        if genetype[gene_names[i]] in filter_types:
            continue
        else:
            coding_gene_nums.append(i)
            coding_genes[gene_names[i]]=counts[gene_names[i]]
#    else:
#        missing_genes.append(gene_names[i])
        
origdir='/Users/poldrack/data/selftracking/rna-seq/htcount_files'
origfiles=[i.split('/')[-1].replace('.txt','') for i in glob.glob(os.path.join(origdir,'*'))]
origfiles.sort()

coding_gene_df=pd.DataFrame(coding_genes).T
coding_gene_df.columns=origfiles
coding_gene_df.to_csv('/Users/poldrack/data/selftracking/rna-seq/all_coding_genes.txt')

# make new htcount files
outdir='/Users/poldrack/data/selftracking/rna-seq/htcount_files_filtered'
if not os.path.exists(outdir):
    os.mkdir(outdir)

meanexpr=coding_gene_df.mean(1)
lowexpr=[]
highexpr=[]
for k in meanexpr.keys():
    if meanexpr[k]<4:
        lowexpr.append(k)
        coding_gene_df=coding_gene_df.drop(k)
    elif meanexpr[k]>10000:
        highexpr.append(k)
        coding_gene_df=coding_gene_df.drop(k)
        
for f in origfiles:
    outfile=open(os.path.join(outdir,'%s.txt'%f),'w')
    data=coding_gene_df[f]
    for k in data.keys():
        outfile.write('%s\t%d\n'%(k,data[k]))
    outfile.close()
    

