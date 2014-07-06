"""
load variance-stabilized count data and combine into pathways
based on Reactome
"""

import numpy

import os,pickle

from  sklearn.decomposition import PCA

# obtain reactome pathways  on July 27, 2014 using:
# wget http://www.reactome.org/download/current/ReactomePathways.gmt.zip

# parse reactome gene lists

f=open('/Users/poldrack/Dropbox/code/selftracking/rna-seq/ReactomePathways.gmt')
genesets={}
for l in f.readlines():
	l_s=l.strip().split('\t')
	pathname=l_s[0].replace(' ','_')
	genesets[pathname]=l_s[3:]
# use cleaned and variance-stabilized data from setup_expression_data.R
f.close()

f=open('/Users/poldrack/Dropbox/data/selftracking/rna-seq/varstab_data.txt')
genedata={}
subcodes=f.readline().strip().replace('"','').split()

nsubs=len(subcodes)
for l in f.readlines():
    l_s=l.strip().split()
    genedata[l_s[0].replace('"','')]=[float(i) for i in l_s[1:]]
f.close()

genenames=genedata.keys()
genenames.sort()


setdata={}
corrdata={}
setdata_genes={}

for k in genesets.iterkeys():
        if not setdata.has_key(k):
            setdata[k]=[]
        setgenes=genesets[k]
        #print k, setgenes
        tmp=[]
        tmp_genes=[]
        for g in setgenes:
            try:
                tmp.append(genedata[g])
                tmp_genes.append(g)
            except:
                print g,'missing from data'
                pass
        if not setdata.has_key(k):
            setdata[k]=[]
        setdata[k]=numpy.array(tmp)
        setdata_genes[k]=tmp_genes


# put all together into a single matrix for each set
setcorr={}
setmean={}
seteig={}
setexplained={}
reactometerm=[]
setgmean={}

pca = PCA(n_components=1)
setkeys=setdata.keys()
setkeys.sort()

for k in setkeys:
    if len(setdata[k])==0:
        continue
    reactometerm.append(k)
    #cc=numpy.corrcoef(setdata[k])
    #setcorr[k]=numpy.nanmean(cc[numpy.triu_indices(cc.shape[0],1)])
    seteig[k]=pca.fit_transform(setdata[k].T)
    setmean[k]=numpy.mean(setdata[k],0)
    setgmean[k]=numpy.mean(setdata[k])
    setexplained[k]=pca.explained_variance_ratio_


patheig=numpy.zeros((len(reactometerm),nsubs))
pathcorr=numpy.zeros(len(reactometerm))
pathmean=numpy.zeros((len(reactometerm),nsubs))

ctr=0
pathdesc=[]
pathsubs=[]
pathstd=[]
pathcv=[]
for k in setkeys:
    if not seteig.has_key(k):
        continue
    patheig[ctr,:]=seteig[k][:,0]
    pathmean[ctr,:]=setmean[k]
    #pathcorr[ctr]=setcorr[k]
    pathstd.append(numpy.std(setmean[k]))
    pathcv.append(numpy.std(setmean[k])/numpy.mean(setmean[k]))
    #pathdesc.append(p['GO:%07d'%k].name.replace(' ','_').replace("'",""))
    ctr+=1

    #cc=numpy.corrcoef(alldata)

f=open('/Users/poldrack/Dropbox/data/selftracking/rna-seq/reactome_analysis/reactometerms.txt','w')
for i in reactometerm:
    f.write('%s\n'%i)
f.close()
f=open('/Users/poldrack/Dropbox/data/selftracking/rna-seq/reactome_analysis/reactomesubs.txt','w')
for i in subcodes:
    f.write('%s\n'%i)
f.close()

numpy.savetxt('/Users/poldrack/Dropbox/data/selftracking/rna-seq/reactome_analysis/patheig.txt',patheig.T)
numpy.savetxt('/Users/poldrack/Dropbox/data/selftracking/rna-seq/reactome_analysis/pathmean.txt',pathmean.T)
numpy.savetxt('/Users/poldrack/Dropbox/data/selftracking/rna-seq/reactome_analysis/pathcv.txt',pathcv)
#numpy.savetxt('/Users/poldrack/Dropbox/data/selftracking/rna-seq/reactome_analysis/pathcorr.txt',pathcorr)
numpy.save('/Users/poldrack/Dropbox/data/selftracking/rna-seq/reactome_analysis/all_setdata.npy',setdata)
pickle.dump(setdata_genes,open('/Users/poldrack/Dropbox/data/selftracking/rna-seq/reactome_analysis/all_setdata_genes.pkl','wb'))