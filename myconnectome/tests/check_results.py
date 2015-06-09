"""
compare results from myconnectome analysis to saved results on S3
"""

import numpy
import os
import urllib
from myconnectome.utils.load_dataframe import load_R_dataframe,load_wgcna_module_assignments

basedir=os.environ['MYCONNECTOME_DIR']
dataurl='http://web.stanford.edu/group/poldracklab/myconnectome-data/cached/'

rtol=atol=1e-08

print 'checking local results against cached data'

files_to_compare={}
rsfmri_files=['modularity_weighted_louvain_bct.txt','PIpos_weighted_louvain_bct.txt',
              'geff_pos.txt','module_between_corr.txt',
              'module_within_corr.txt']
for f  in rsfmri_files:
    files_to_compare['rsfmri/'+f]='rsfmri/'+f

rnaseq_files=['varstab_data_prefiltered_rin_3PC_regressed.txt']
for f  in rnaseq_files:
    files_to_compare['rna-seq/'+f]='rna-seq/'+f

metabolomics_files=['apclust_eigenconcentrations.txt']
for f  in metabolomics_files:
    files_to_compare['metabolomics/'+f]='metabolomics/'+f

logdir=os.path.join(basedir,'logs')
logfile=os.path.join(logdir,'data_downloads.log')

if os.path.exists(logfile):    
    downloaded_files=[i.strip().split('\t')[0] for i in open(logfile).readlines()]
else:
    downloaded_files=[]

for f in files_to_compare.iterkeys():
    try:
        assert os.path.exists(os.path.join(basedir,f))
    except:
        print 'MISSING FILE:',os.path.join(basedir,f)
        continue
    
    if os.path.join(basedir,f) in downloaded_files:
        print 'USING DOWNLOADED FILE:',f
        continue
    
    url=dataurl+files_to_compare[f]
    raw_data = urllib.urlopen(url)
    try:
        repos_data=numpy.loadtxt(raw_data)
    except:
        repos_data,rownames,h=load_R_dataframe(url)
    try:
        local_data=numpy.loadtxt(os.path.join(basedir,f))
    except:
        local_data,rownames,h=load_R_dataframe(os.path.join(basedir,f))
        
    try:
        assert repos_data.shape == local_data.shape
        if numpy.allclose(repos_data,local_data,rtol,atol):
            print 'PASS:',f
        else:
            maxdiff=numpy.max(repos_data - local_data)
            print 'FAIL:',f,'maxdiff =',maxdiff
    except:
        print 'FAIL:',f,'data shapes differ', repos_data.shape,local_data.shape

# the following have to be set up separately because these file formats are funky

try:
    assert os.path.exists(os.path.join(basedir,'rna-seq/WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt'))
    modassn_local=load_wgcna_module_assignments(os.path.join(basedir,'rna-seq/WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt'))
    modassn_repos=load_wgcna_module_assignments(dataurl+'rna-seq/WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt')
    if numpy.allclose(modassn_local[0],modassn_repos[0],rtol,atol):
        print 'PASS: rna-seq/WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt'
    else:
        maxdiff=numpy.max(modassn_local[0] - modassn_repos[0])
        print 'FAIL: rna-seq/WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt','maxdiff =',maxdiff
except:
    print 'MISSING FILE:',os.path.join(basedir,'rna-seq/WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt')
    


url=dataurl+'/rna-seq/WGCNA/MEs-thr8-prefilt-rinPCreg-48sess.txt'
raw_data = urllib.urlopen(url)
f='rna-seq/WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt'
repos_data=numpy.loadtxt(raw_data,skiprows=1)
try:
    assert os.path.exists(os.path.join(basedir,f))
    
    local_data=numpy.loadtxt(os.path.join(basedir,f),skiprows=1)

    if numpy.allclose(repos_data,local_data,rtol,atol):
        print 'PASS:',f
    else:
        maxdiff=numpy.max(repos_data - local_data)
        print 'FAIL:',f,'maxdiff =',maxdiff
except:
    print 'MISSING FILE:',f
    