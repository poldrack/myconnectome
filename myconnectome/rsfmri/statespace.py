"""
show 3-d state space for resting data
"""

import os,glob
import numpy
from sklearn.decomposition import PCA,KernelPCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


datadir='/Users/poldrack/data_unsynced/myconnectome/combined_data_scrubbed'
outdir='/Users/poldrack/data_unsynced/myconnectome/statespace'
if not os.path.exists(outdir):
    os.mkdir(outdir)

datafiles=glob.glob(os.path.join(datadir,'*.txt'))
datafiles.sort()
pcatype='pca'

for f in datafiles:
    d=numpy.loadtxt(f)
    
    subcode=os.path.basename(f).replace('.txt','')
    if pcatype=='pca':
        pca=PCA(n_components=3)
    elif pcatype=='kpca':
        pca = KernelPCA(n_components=3,kernel="poly",degree=3)

    t=pca.fit_transform(d)
    if hasattr(pca,'explained_variance_ratio_'):
        print('variance explained:',pca.explained_variance_ratio_)

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.plot(t[:,0],t[:,1],t[:,2],linewidth=0.5)
    plt.title(subcode)
    fig.savefig(os.path.join(outdir,'%s_%s.pdf'%(subcode,pcatype)))
    plt.clf()
