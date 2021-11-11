"""
show 3-d state space for resting data
"""

import os,glob,pickle
import numpy,pandas
from sklearn.decomposition import PCA,KernelPCA,FastICA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.collections import LineCollection
from matplotlib.colors import ListedColormap, BoundaryNorm
from mpl_toolkits.mplot3d.art3d import Line3DCollection
from sklearn.manifold import TSNE
from sklearn.preprocessing import scale

pcatype='pca'
plottype='time' # 'state' or 'time'

if plottype=='state':
    cmap=plt.get_cmap('seismic') #red=integrated
else:
    cmap=plt.get_cmap('jet')
stateinfo=pandas.read_csv('russ_states.txt',sep='\t')
datadir='/Users/poldrack/data_unsynced/myconnectome/combined_data_scrubbed'
outdir='/Users/poldrack/data_unsynced/myconnectome/statespace'
if not os.path.exists(outdir):
    os.mkdir(outdir)

datafiles=glob.glob(os.path.join(datadir,'*.txt'))
datafiles.sort()
data=numpy.zeros((518,630,len(datafiles)))

if plottype=='state':
    datafile='longdata_trimmed.npy'
else:
    datafile='longdata.npy'
try:
    data=numpy.load(datafile)
except:
    for i,f in enumerate(datafiles):
        tmp=numpy.loadtxt(f)
        if plottype=='state':
            tmp=tmp[100:,:]
        s=scale(tmp) # standardize each ROI within each session
        if i==0:
            data=s
        else:
            data=numpy.vstack((data,s))
    numpy.save(datafile,data)

if pcatype=='pca':
    dm=PCA(n_components=3)
    t=dm.fit_transform(data)

elif pcatype=='kpca':
    dm = KernelPCA(n_components=3,kernel="poly",degree=2)
    t=dm.fit_transform(data)
elif pcatype=='ica':
    dm = FastICA(n_components=3)
    t=dm.fit_transform(data)

elif pcatype=='tsne':
    try:
        dm=pickle.load(open('tsne_model.pkl','rb'))
        t=numpy.load('3comps_tsne.npy')
        print('loaded existing tSNE fit')
    except:
        pca=PCA(n_components=50)
        tmp=pca.fit_transform(data)
        dm=TSNE(n_components=3,verbose=1)
        t=dm.fit_transform(tmp)

if hasattr(dm,'explained_variance_ratio_'):
    print('variance explained:',dm.explained_variance_ratio_)

numpy.save('3comps_%s_%s.npy'%(pcatype,plottype),t)

tp=t.reshape(-1,1,3)
segments=numpy.concatenate([tp[:-1], tp[1:]], axis=1)
lc = Line3DCollection(segments, cmap=cmap,
        norm=plt.Normalize(0, 1))

if plottype=='time':
    tpoints=numpy.kron(numpy.ones(len(datafiles)),numpy.linspace(0, 1, 518))
    lc.set_array(tpoints)
elif plottype=='state':
    allstateinfo=stateinfo.ix[:,3:].T.stack()
    lc.set_array(allstateinfo/3.)
lc.set_linewidth(0.1)
fig = plt.figure()
#ax = fig.gca(projection = '3d')
ax = fig.add_subplot(111, projection='3d')

ax.axes.set_xlim(numpy.min(t[:,0]),numpy.max(t[:,0]))
ax.axes.set_ylim(numpy.min(t[:,1]),numpy.max(t[:,1]))
ax.axes.set_zlim(numpy.min(t[:,2]),numpy.max(t[:,2]))
p=ax.add_collection3d(lc)
fig.savefig(os.path.join(outdir,'alldata_%s_%s.pdf'%(pcatype,plottype)))
fig.clf()
del fig

if plottype=='state':
    offset=418
else:
    offset=518

for i in range(len(datafiles)):
    start=i*offset
    end=(i+1)*offset
    d=data[start:end,:]
    subcode=os.path.basename(datafiles[i]).replace('.txt','')

    tsub=t[start:end,:]

    tp=tsub.reshape(-1,1,3)
    segments=numpy.concatenate([tp[:-1], tp[1:]], axis=1)
    lc = Line3DCollection(segments, cmap=cmap,
        norm=plt.Normalize(0, 1))
    if plottype=='time':
        tpoints=numpy.linspace(0, 1, 518)
        lc.set_array(tpoints)
    elif plottype=='state':
        lc.set_array(stateinfo.ix[i,3:]/3.)
    lc.set_linewidth(1)
    fig = plt.figure(figsize=(16,16))
    #ax = fig.gca(projection = '3d')
    ax = fig.add_subplot(111, projection='3d')
    ax.axes.set_xlim(numpy.min(t[:,0]),numpy.max(t[:,0]))
    ax.axes.set_ylim(numpy.min(t[:,1]),numpy.max(t[:,1]))
    ax.axes.set_zlim(numpy.min(t[:,2]),numpy.max(t[:,2]))
    p=ax.add_collection3d(lc)
    plt.title(subcode)

    fig.savefig(os.path.join(outdir,'%s_%s_%s.pdf'%(subcode,pcatype,plottype)))
    fig.clf()
    del fig
