"""
get eigengene for each cluster
use GOBS data with clusters derived from myconnectome

"""

import os
import numpy
from  sklearn.decomposition import PCA

stdir=os.environ['MYCONNECTOME_DIR']
rnaseqdir=os.path.join(stdir,'rna-seq')
wgcnadir=os.path.join(rnaseqdir,'WGCNA')

gobsdir='/Users/poldrack/data/GOBS-expression/rsfmri'
genelists={}

f=open(os.path.join(rnaseqdir,'WGCNA/module_assignments_thr8_prefilt_rinPCreg.txt'))
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

gene_names=[i.strip() for i in open(os.path.join(gobsdir,'gene_names.txt')).readlines()]
varstabfile=os.path.join(gobsdir,'exprdata_common_snp_exprPC_reg.txt')

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
    
f=open(os.path.join(gobsdir,'cluster_eigengenes_mycmodules.txt'),'w')
for i in range(len(genelists)):
    f.write('%s\t%s\n'%(genelistkeys[i],'\t'.join(['%f'%j for j in seteig[:,i]])))
f.close()

f=open(os.path.join(gobsdir,'cluster_means_mycmodules.txt'),'w')
for i in range(len(genelists)):
    f.write('%s\t%s\n'%(genelistkeys[i],'\t'.join(['%f'%j for j in setmean[:,i]])))
f.close()
  
numpy.savetxt(os.path.join(gobsdir,'cluster_eigengenes_GOBS_explainedvariance.txt'),setexplained)
  