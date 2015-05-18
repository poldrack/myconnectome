"""
make gifti images for participation index and correlations with behav variables
"""

import os,sys
import numpy
import nibabel.gifti.giftiio
from myconnectome.utils import labels_to_gii,load_dataframe

basedir=os.environ['MYCONNECTOME_DIR']
rsfmridir=os.path.join(basedir,'rsfmri')

def mk_participation_index_giftis():
    pidata=numpy.loadtxt(os.path.join(rsfmridir,'PIpos_weighted_louvain_bct.txt'))
    
    df=load_dataframe.load_dataframe(os.path.join(basedir,'timeseries/out.dat.pindex_behav.txt'),thresh=0.05)
    
    associations={}
    for v in df.iterkeys():
        if not associations.has_key(v[1]):
            associations[v[1]]=numpy.zeros(634)
        vertexnum=int(v[0].replace('V',''))-1
        associations[v[1]][vertexnum]=df[v][2]
        
    vars=associations.keys()
    vars.sort()
    
    data=numpy.zeros((634,len(vars)))
    
    for i in range(len(vars)):
        data[:,i]=associations[vars[i]]
    data=data[:620,:]
    meanpi=numpy.mean(pidata,1)
    data=numpy.hstack((meanpi[:620,None],data))
    vars=['meanPI']+vars
    labels_to_gii.labels_to_gii(data,vars,'PI',basedir=basedir,outdir=rsfmridir)
    
if __name__ == "__main__":
    mk_participation_index_giftis()