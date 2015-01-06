"""
get eigengene for each cluster
use GOBS data with clusters derived from myconnectome

"""

import os,sys
import numpy
from  sklearn.decomposition import PCA
import sklearn.linear_model

pcs_to_regress=5

basedir='/Users/poldrack/Dropbox/data/selftracking/rna-seq/WGCNA'

genelists={}

f=open(os.path.join(basedir,'module_assignments.txt'))
for l in f.readlines():
    l_s=l.strip().split(' ')
    modnum=int(l_s[1])
    gene=l_s[0]
    if modnum==0:
    	continue
    if not genelists.has_key(modnum):
    	genelists[modnum]=[]
    genelists[modnum].append(gene)
    
f.close()

gene_names=[i.strip() for i in open('/Users/poldrack/Dropbox/data/connectome-genome/transcripts/gene_names.txt').readlines()]
varstabfile='/Users/poldrack/Dropbox/data/connectome-genome/transcripts/expr_common.txt'

f=open(varstabfile)
exprdata={}
ctr=0
for l in f.readlines():
    l_s=[float(i) for i in l.strip().split()]
    assert len(l_s)==len(gene_names)
    for g in range(len(gene_names)):
        if exprdata.has_key(gene_names[g]):
            exprdata[gene_names[g]].append(l_s[g])
        else:
            exprdata[gene_names[g]]=[l_s[g]]
f.close()

# do PCA across all genes
all_exprdata=numpy.zeros((len(exprdata['DRD4']),len(exprdata)))
ctr=0
for k in gene_names:
    all_exprdata[:,ctr]=exprdata[k]
    ctr+=1

pca_allexprdata = PCA(n_components=pcs_to_regress)
global_pcs=pca_allexprdata.fit_transform(all_exprdata)

# load SNP PCs
snppcfile='/Users/poldrack/Dropbox/data/connectome-genome/transcripts/safs_pc1-10.csv'
f=open(snppcfile)
header=f.readline()
lines=f.readlines()
f.close()
snpdata={}

for l in lines:
    l_s=l.strip().split(',')
    snpdata[l_s[0]]=[float(l_s[i]) for i in range(4,14)]

# snp data missing for one subject - fill with zeros
snpdata['EJ2303']=numpy.mean(snp_pcs,0)

subcodes=[i.strip() for i in open('/Users/poldrack/Dropbox/data/connectome-genome/transcripts/subcodes_common.txt').readlines()]

snp_pcs=numpy.zeros((len(subcodes),10))

for i in range(len(subcodes)):
    snp_pcs[i,:]=snpdata[subcodes[i]]

all_pcs=numpy.hstack((global_pcs,snp_pcs))
linreg=sklearn.linear_model.LinearRegression(fit_intercept=True)

if pcs_to_regress > 0:
    linreg.fit(all_pcs,all_exprdata)
    all_exprdata=all_exprdata - linreg.predict(all_pcs)

gene_indices={}
ctr=0
for g in gene_names:
    gene_indices[g]=ctr
    ctr+=1


setdata={}
setdata_genes={}

for k in genelists.iterkeys():
        if not setdata.has_key(k):
            setdata[k]=[]
        setgenes=genelists[k]
        #print k, setgenes
        tmp=[]
        tmp_genes=[]
        for g in setgenes:
            try:
                tmp.append(exprdata[g])
                tmp_genes.append(g)
            except:
                print g,'missing from data'
                pass
        if not setdata.has_key(k):
            setdata[k]=[]
        setdata[k]=numpy.array(tmp)
        setdata_genes[k]=tmp_genes

nsubs=591
seteig=numpy.zeros((nsubs,len(genelists)))
setmean=numpy.zeros((nsubs,len(genelists)))
setexplained=numpy.zeros(len(genelists))
genelistkeys=genelists.keys()
genelistkeys.sort()

pca = PCA(n_components=1)

for i in range(len(genelists)):
    k=genelistkeys[i]
    setmean[:,i]=numpy.mean(setdata[k],0)
    seteig[:,i]=pca.fit_transform(setdata[k].T)[:,0]
    print numpy.corrcoef(seteig[:,i],setdata[k].T[:,0])[0,1]
    if numpy.corrcoef(seteig[:,i],setdata[k].T[:,0])[0,1] < 0:
        #print 'flippping sign of PC to match data'
        seteig[:,i]=-1.0*seteig[:,i]
    setexplained[i]=pca.explained_variance_ratio_
    #print numpy.corrcoef(seteig_rinreg[:,i],setdata[k].T[:,0])[0,1]
    print k,setdata[k].shape,setexplained[i]
    
f=open(os.path.join(basedir,'cluster_eigengenes_GOBS_reg%dPCs_regSNP.txt'%pcs_to_regress),'w')
for i in range(len(genelists)):
    f.write('%s\t%s\n'%(genelistkeys[i],'\t'.join(['%f'%j for j in seteig[:,i]])))
f.close()

f=open(os.path.join(basedir,'cluster_means_GOBS_reg%dPCs_regSNP.txt'%pcs_to_regress),'w')
for i in range(len(genelists)):
    f.write('%s\t%s\n'%(genelistkeys[i],'\t'.join(['%f'%j for j in setmean[:,i]])))
f.close()
  
numpy.savetxt(os.path.join(basedir,'cluster_eigengenes_GOBS_explainedvariance_reg%dPCs_regSNP.txt'%pcs_to_regress),setexplained)
  