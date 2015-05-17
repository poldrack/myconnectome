"""
get eigengene for each cluster
"""

import os,sys
import numpy
from  sklearn.decomposition import PCA
import sklearn.linear_model

stdir=os.environ['MYCONNECTOME_DIR']
rnaseqdir=os.path.join(stdir,'rna-seq')
immportdir=os.path.join(rnaseqdir,'ImmPort')

def get_ImmPort_eigengenes():
    if not os.path.exists(immportdir):
        os.mkdir(immportdir)
    
    genelists={}
    
    f=open(os.path.join(immportdir,'all_ImmPort_pathways.txt'))
    for l in f.readlines():
        l_s=l.strip().split('\t')
        genelists[l_s[0]]=l_s[1:]
        
    f.close()
    
    varstabfile=os.path.join(rnaseqdir,'varstab_data_prefiltered_rin_3PC_regressed.txt')
    
    pca = PCA(n_components=1)
    
    f=open(varstabfile)
    header=f.readline()
    exprdata={}
    gene_names=[]
    for l in f.readlines():
        l_s=l.strip().split()
        gene_name=l_s[0].replace('"','')
        gene_names.append(gene_name)
        exprdata[gene_name]=[float(i) for i in l_s[1:]]
    
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
    
    rin=numpy.loadtxt(os.path.join(rnaseqdir,'rin.txt'))
    seteig=numpy.zeros((48,len(genelists)))
    setexplained=numpy.zeros(len(genelists))
    genelistkeys=genelists.keys()
    genelistkeys.sort()
    
    
    for i in range(len(genelists)):
        k=genelistkeys[i]
        pca.fit(setdata[k].T)
        seteig[:,i]=pca.transform(setdata[k].T)[:,0]
        print numpy.corrcoef(seteig[:,i],numpy.mean(setdata[k],0))[0,1]
        if numpy.corrcoef(seteig[:,i],numpy.mean(setdata[k],0))[0,1] < 0:
            #print 'flippping sign of PC to match data'
            seteig[:,i]=-1.0*seteig[:,i]
        setexplained[i]=pca.explained_variance_ratio_
        print k,setdata[k].shape,setexplained[i],numpy.corrcoef(seteig[:,i],rin)[0,1]
        
      
    f=open(os.path.join(immportdir,'ImmPort_eigengenes_prefilt_rin3PCreg.txt'),'w')
    for i in range(len(genelists)):
        f.write('%s\t%s\n'%(genelistkeys[i],'\t'.join(['%f'%j for j in seteig[:,i]])))
    f.close()
    
    numpy.savetxt(os.path.join(immportdir,'ImmPort_eigengenes_prefilt_rin3PCreg_explainedvariance.txt'),setexplained)
    
if __name__ == "__main__":
    get_ImmPort_eigengenes()