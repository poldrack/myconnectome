"""
compare results from myconnectome analysis to saved results on S3
"""

import numpy
import os,glob,sys
import urllib
import argparse
from myconnectome.utils.load_dataframe import load_dataframe,load_wgcna_module_assignments

rtol=atol=1e-04

# from http://stackoverflow.com/questions/3462143/get-difference-between-two-lists

def diff(list1, list2):
    c = set(list1).union(set(list2))
    d = set(list1).intersection(set(list2))
    return list(c - d)

def load_varstab_data(infile):
    if infile.find('http')==0:
            f=urllib.urlopen(infile)
    else:
            f=open(infile)
    header=f.readline()
    data=[]
    genes=[]
    for l in f.readlines():
        ls=l.strip().split()
        genes.append(ls[0])
        data.append([float(x) for x in ls[1:]])
    return numpy.array(data),genes

def compare_matrices(localdata,remotedata,infile,atol=1e-04,rtol=1e-04):
    if numpy.allclose(localdata,remotedata,rtol,atol):
        print 'PASS:',infile
    else:
        maxdiff=numpy.max(localdata - remotedata)
        print 'FAIL:',infile,'maxdiff =',maxdiff
    
def check_text_file(infile):
    local=numpy.loadtxt(os.path.join(basedir,infile))
    remote=load_dataframe('%s/%s'%(dataurl,infile),thresh=1.01)
    if not len(local)==len(remote):
        print 'size mismatch for ',infile
        return
    localdata=numpy.zeros((len(local),4))
    remotedata=numpy.zeros((len(remote),4))
    keys=local.keys()
    for k in range(len(keys)):
        if not remote.has_key(keys[k]):
            print 'remote missing matching key',keys[k]
        localdata[k,:]=local[keys[k]]
        remotedata[k,:]=remote[keys[k]]
    if numpy.allclose(localdata,remotedata,rtol,atol):
        print 'PASS:',infile
    else:
        maxdiff=numpy.max(localdata - remotedata,0)
        print 'FAIL:',infile,'maxdiff =',maxdiff

def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)

def parse_arguments():
    # parse command line arguments
    # setting testing flag to true will turn off required flags
    # to allow manually running without command line flags

    parser = argparse.ArgumentParser(description='check_results')

    parser.add_argument('-b', dest='basedir',
        default=os.environ['MYCONNECTOME_DIR'],help='local base dir')
    parser.add_argument('-r',dest='remotebase',
        default='myconnectome-vm',help='remote base')
    return parser.parse_args()
    
basedir=os.environ['MYCONNECTOME_DIR']

dataurl='https://s3.amazonaws.com/openfmri/ds031/myconnectome-vm'

args=parse_arguments()
basedir=args.basedir
dataurl='https://s3.amazonaws.com/openfmri/ds031/'+args.remotebase

print 'BASEDIR:',basedir
print 'REMOTEBASE:',dataurl

# first load download log and get list of downloaded files
try:
    downloads=[i.strip().split('\t')[0] for i in open(os.path.join(basedir,'logs/data_downloads.log')).readlines()]
except:
    downloads=[]
    
print 'checking local results against benchmark data (computed on Ubuntu VM)'

print '#### Variance stabilized expression data'
if not 'rna-seq/varstab_data_prefiltered_rin_3PC_regressed.txt' in downloads:
    local,local_genes=load_varstab_data(os.path.join(basedir,'rna-seq/varstab_data_prefiltered_rin_3PC_regressed.txt'))
    remote,remote_genes=load_varstab_data('%s/%s'%(dataurl,'rna-seq/varstab_data_prefiltered_rin_3PC_regressed.txt'))
    compare_matrices(local,remote,'rna-seq/varstab_data_prefiltered_rin_3PC_regressed.txt')
else:
    print 'SKIPPING DOWNLOADED FILE: rna-seq/varstab_data_prefiltered_rin_3PC_regressed.txt'
    
print '### WGCNA'
if not'rna-seq/WGCNA/MEs-thr8-prefilt-rinPCreg-48sess.txt' in downloads:
    local=numpy.genfromtxt(os.path.join(basedir,'rna-seq/WGCNA/MEs-thr8-prefilt-rinPCreg-48sess.txt'),skip_header=1)
    remote=numpy.genfromtxt('%s/rna-seq/WGCNA/MEs-thr8-prefilt-rinPCreg-48sess.txt'%dataurl,skip_header=1)
    compare_matrices(local,remote,'rna-seq/WGCNA/MEs-thr8-prefilt-rinPCreg-48sess.txt')
else:
    print 'SKIPPING DOWNLOADED FILE:   rna-seq/WGCNA/MEs-thr8-prefilt-rinPCreg-48sess.txt'  
    
if not 'rna-seq/WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt' in downloads:
    local,local_genes=load_wgcna_module_assignments(os.path.join(basedir,'rna-seq/WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt'))
    remote,remote_genes=load_wgcna_module_assignments('%s/rna-seq/WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt'%dataurl)
    compare_matrices(local,remote,'rna-seq/WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt')
else:
    print 'SKIPPING DOWNLOADED FILE:   rna-seq/WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt'  

print '#### Metabolomics data'
if not 'metabolomics/apclust_eigenconcentrations.txt' in downloads:
    local,local_subs=load_varstab_data(os.path.join(basedir,'metabolomics/apclust_eigenconcentrations.txt'))
    remote,remote_subs=load_varstab_data('%s/metabolomics/apclust_eigenconcentrations.txt'%dataurl)
    compare_matrices(local,remote,'metabolomics/apclust_eigenconcentrations.txt')
else:
    print 'SKIPPING DOWNLOADED FILE:  metabolomics/apclust_eigenconcentrations.txt'

print '#### BCT analyses'
for f in ['PIpos_weighted_louvain_bct.txt','modularity_weighted_louvain_bct.txt','geff_pos.txt']:
    local=numpy.genfromtxt(os.path.join(basedir,'rsfmri',f))
    remote=numpy.genfromtxt('%s/rsfmri/%s'%(dataurl,f))
    compare_matrices(local,remote,'rsfmri/%s'%f)
    
print '#### Timeseries analysis Results'


tsresults=glob.glob(os.path.join(basedir,'timeseries/out*.txt'))
if len(tsresults)==0:
    print 'no timeseries results found - somethign went wrong'
else:
    for ts in tsresults:
        f=ts.replace(basedir+'/','')
        
        if ts in downloads:
            print 'SKIPPING DOWNLOADED FILE:',f
        else:
            local=load_dataframe(os.path.join(basedir,f),thresh=1.01)
            remote=load_dataframe('%s/%s'%(dataurl,f),thresh=1.01)
            if not len(local)==len(remote):
                print 'size mismatch for ',f,len(local),len(remote)
                continue
            localdata=numpy.zeros((len(local),4))
            remotedata=numpy.zeros((len(remote),4))
            keys=local.keys()
            d=diff(keys,remote.keys())
            if d:
                print 'Key mismatch for',f
                print d
            for k in range(len(keys)):
                if not remote.has_key(keys[k]):
                    print 'remote missing matching key',keys[k]
                else:
                    localdata[k,:]=local[keys[k]]
                    remotedata[k,:]=remote[keys[k]]
            if numpy.allclose(localdata,remotedata,rtol,atol):
                print 'PASS:',f
            else:
                maxdiff=numpy.max(localdata - remotedata,0)
                print 'FAIL:',f,'maxdiff =',maxdiff
                
                
