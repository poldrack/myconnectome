"""
compare results from myconnectome analysis to saved results on S3
"""

import numpy
import os
import urllib
from myconnectome.utils.load_dataframe import load_R_dataframe

basedir=os.environ['MYCONNECTOME_DIR']
rtol=atol=1e-08

files_to_compare={}
rsfmri_files=['modularity_weighted_louvain_bct.txt','PIpos_weighted_louvain_bct.txt',
              'geff_pos.txt','module_between_corr.txt',
              'module_within_corr.txt']
for f  in rsfmri_files:
    files_to_compare['rsfmri/'+f]='rsfmri/'+f

rnaseq_files=['varstab_data_prefiltered_rin_3PC_regressed.txt',
              'WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt',
              'WGCNA/MEs-thr8-prefilt-rinPCreg-48sess.txt']
for f  in rnaseq_files:
    files_to_compare['rna-seq/'+f]='RNA-seq/'+f

metabolomics_files=['apclust_eigenconcentrations.txt']
for f  in metabolomics_files:
    files_to_compare['metabolomics/'+f]='metabolomics/'+f

for f in files_to_compare.iterkeys():
    url='https://s3.amazonaws.com/openfmri/ds031/'+files_to_compare[f]
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
