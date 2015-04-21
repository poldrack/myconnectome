# -*- coding: utf-8 -*-
"""
Object analysis for myconnectome - 
- first, find maximal response for each voxel
Created on Sat Apr 18 16:26:43 2015

@author: poldrack
"""

import nibabel.gifti.giftiio
import numpy
import os
from GiniCoef import GRLC
import pandas as pd
import scipy.stats

thresh=2.0  # t thresh for max response

datadir='/Users/poldrack/data/selftracking/surface_stats_333'
outdir='/Users/poldrack/data/selftracking/object_selectivity'
parceldir='/Users/poldrack/data/selftracking/parcellation'

hems=['L','R']
data={}
parcels={}
parceldata={}
matrixdata={}

for h in hems:
    datafile=os.path.join(datadir,'stats.%s.func.gii'%h)
    data[h]=nibabel.gifti.giftiio.read(datafile)
    parcelfile=os.path.join(parceldir,'all_selected_%s_parcel_renumbered.func.gii'%h)
    parcels[h]=nibabel.gifti.giftiio.read(parcelfile)
    parceldata[h]=parcels[h].darrays[0].data
    matrixdata[h]=numpy.zeros((parcels[h].darrays[0].data.shape[0],
                    len(data[h].darrays)))
    for k in range(len(data[h].darrays)):
        matrixdata[h][:,k]=data[h].darrays[k].data

# make a matrix will all of the voxel data
  
tasknames=[]    

for da in data['L'].darrays:
    tasknames.append(da.get_metadata()['Name'])

object_tasks=[]    
for i in range(len(tasknames)):
    if tasknames[i].find('object')==0 and tasknames[i].find('response')<0:
        object_tasks.append(i)

maxcat_object={}
for h in hems:
    maxcat_object[h]=numpy.argmax(matrixdata[h][:,object_tasks],1)

maxcat_alltasks={}
for h in hems:
    maxcat_alltasks[h]=numpy.argmax(matrixdata[h],1)

# make maps for each category    
# mask out voxels that are below threshold

print 'making maxcat maps'

combodata={}
combodata_objects={}

for h in hems:
    newimg=nibabel.gifti.GiftiImage()

    for i in range(len(object_tasks)):
        darray=numpy.array(((maxcat_object[h]==i) * 
            (data[h].darrays[object_tasks[i]].data>thresh))*data[h].darrays[object_tasks[i]].data,
            dtype=numpy.float32)
        newimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray,
            intent=data[h].darrays[0].intent,
            datatype=data[h].darrays[0].datatype,
            ordering='F',
            meta={'AnatomicalStructurePrimary':'CortexLeft',
            'Name':tasknames[object_tasks[i]]}))
        
    nibabel.gifti.giftiio.write(newimg,os.path.join(outdir,'maxcat_objects.%s.func.gii'%h))
    
    newimg=nibabel.gifti.GiftiImage()

    for i in range(matrixdata[h].shape[1]):
        darray=numpy.array(((maxcat_alltasks[h]==i) * 
            (data[h].darrays[i].data>thresh))*data[h].darrays[i].data,
            dtype=numpy.float32)
        newimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray,
            intent=data[h].darrays[0].intent,
            datatype=data[h].darrays[0].datatype,
            ordering='F',
            meta={'AnatomicalStructurePrimary':'CortexLeft',
            'Name':tasknames[i]}))
        
    nibabel.gifti.giftiio.write(newimg,os.path.join(outdir,'maxcat_alltasks.%s.func.gii'%h))

    # write combined map
    newimg=nibabel.gifti.GiftiImage()
    combodata_objects[h]=numpy.zeros(data[h].darrays[0].data.shape,dtype=numpy.float32)
    for c in range(len(maxcat_object[h])):
        combodata_objects[h][c]=data[h].darrays[object_tasks[maxcat_object[h][c]]].data[c]
        
    darray=numpy.array(maxcat_object[h]+1,dtype=numpy.float32)
    darray[combodata_objects[h]<thresh]=0
    newimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray,
            intent=data[h].darrays[0].intent,
            datatype=data[h].darrays[0].datatype,
            ordering='F',
            meta={'AnatomicalStructurePrimary':'CortexLeft',
            'Name':'maxcat-objects'}))
        
    nibabel.gifti.giftiio.write(newimg,os.path.join(outdir,'maxcat_objects_combined.%s.func.gii'%h))

    # write combined map
    newimg=nibabel.gifti.GiftiImage()
    combodata[h]=numpy.zeros(data[h].darrays[0].data.shape,dtype=numpy.float32)
    for c in range(len(maxcat_alltasks[h])):
        combodata[h][c]=data[h].darrays[maxcat_alltasks[h][c]].data[c]
        
    darray=numpy.array(maxcat_alltasks[h]+1,dtype=numpy.float32)
    darray[combodata[h]<thresh]=0
    newimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray,
            intent=data[h].darrays[0].intent,
            datatype=data[h].darrays[0].datatype,
            ordering='F',
            meta={'AnatomicalStructurePrimary':'CortexLeft',
            'Name':'maxcat-alltasks'}))
        
    nibabel.gifti.giftiio.write(newimg,os.path.join(outdir,'maxcat_alltasks_combined.%s.func.gii'%h))
    
    
# compute voxelwise Gini coefficient
print 'computing voxelwise Gini...'

ginicoeff={}
ginicoeff_objects={}
for h in hems:
    ginicoeff_objects[h]=numpy.zeros(data[h].darrays[0].data.shape,dtype=numpy.float32)
    ginicoeff[h]=numpy.zeros(data[h].darrays[0].data.shape,dtype=numpy.float32)
    
    for v in range(data[h].darrays[0].data.shape[0]):
        try:
            # normalize data to 0-1
            d=matrixdata[h][v,object_tasks]
            dn=(d-numpy.min(d))/(numpy.max(d)-numpy.min(d))
            g=GRLC(dn)
            if not numpy.isnan(g[1]):
                ginicoeff_objects[h][v]=g[1]
        except:
            pass
        try:
            # normalize data to 0-1
            d=matrixdata[h][v,:]
            dn=(d-numpy.min(d))/(numpy.max(d)-numpy.min(d))
            g=GRLC(dn)
            if not numpy.isnan(g[1]):
                ginicoeff[h][v]=g[1]
        except:
            pass
    ginicoeff_objects[h][combodata[h]<thresh]=0
    newimg=nibabel.gifti.GiftiImage()
    newimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(ginicoeff[h],
            intent=data[h].darrays[0].intent,
            datatype=data[h].darrays[0].datatype,
            ordering='F',
            meta={'AnatomicalStructurePrimary':'CortexLeft',
            'Name':'gini-alltasks'}))
    nibabel.gifti.giftiio.write(newimg,os.path.join(outdir,'gini_alltasks.%s.func.gii'%h))
    newimg=nibabel.gifti.GiftiImage()
    newimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(ginicoeff_objects[h],
            intent=data[h].darrays[0].intent,
            datatype=data[h].darrays[0].datatype,
            ordering='F',
            meta={'AnatomicalStructurePrimary':'CortexLeft',
            'Name':'gini-objects'}))
    nibabel.gifti.giftiio.write(newimg,os.path.join(outdir,'gini_objects.%s.func.gii'%h))

# # get measures for each parcel
# take maxtask for each voxel in the parcel
# compute gini across voxels

parcel_selectivity_objects=numpy.zeros(620)
parcel_selectivity_alltasks=numpy.zeros(620)
parcel_ginicoeff=numpy.zeros(620)
parcel_object_ginicoeff=numpy.zeros(620)

parcel_mean_response=numpy.zeros((620,27))
parcel_max_response=numpy.zeros((620,27))
parcel_mean_object_response=numpy.zeros((620,9))
parcel_max_object_response=numpy.zeros((620,9))

parcel_ginicoeff_darray={'L':numpy.zeros(data[h].darrays[0].data.shape,dtype=numpy.float32),'R':numpy.zeros(data[h].darrays[0].data.shape,dtype=numpy.float32)}
parcel_max_darray={'L':numpy.zeros(data[h].darrays[0].data.shape,dtype=numpy.float32),'R':numpy.zeros(data[h].darrays[0].data.shape,dtype=numpy.float32)}
parcel_object_ginicoeff_darray={'L':numpy.zeros(data[h].darrays[0].data.shape,dtype=numpy.float32),'R':numpy.zeros(data[h].darrays[0].data.shape,dtype=numpy.float32)}
parcel_object_max_darray={'L':numpy.zeros(data[h].darrays[0].data.shape,dtype=numpy.float32),'R':numpy.zeros(data[h].darrays[0].data.shape,dtype=numpy.float32)}

def compute_gini_for_parcels(matrixdata,parceldata,h,p,limit=None):
    if limit:
        data=matrixdata[h][:,limit]
    else:
        data=matrixdata[h]
    parcelvox=numpy.where(parceldata[h]==p)[0]
    parcel_mean_response=numpy.mean(data[parcelvox,:],0)
    parcel_max_response=numpy.argsort(parcel_mean_response)[::-1]+1
    dn=(parcel_mean_response-numpy.min(parcel_mean_response))/(numpy.max(parcel_mean_response)-numpy.min(parcel_mean_response))
    g=GRLC(dn)
    if not numpy.isnan(g[1]):
        return g[1],parcel_mean_response,parcel_max_response,parcelvox
    else:
        return 0,parcel_mean_response,parcel_max_response,parcelvox
    
print 'computing parcelwise gini'
for p in range(1,621):
    if p>310:
        h='R'
    else:
        h='L'
    g=compute_gini_for_parcels(matrixdata,parceldata,h,p)
    parcelvox=g[3]
    parcel_ginicoeff[p]=g[0]
    parcel_ginicoeff_darray[h][parcelvox]=g[0]
    parcel_mean_response[p-1,:]=g[1]
    parcel_max_response[p-1,:]=g[2]
    parcel_max_darray[h][parcelvox]=g[2][0]

    g_o=compute_gini_for_parcels(matrixdata,parceldata,h,p,object_tasks)
    parcelvox=g[3]    
    parcel_mean_object_response[p-1,:]=g_o[1]
    parcel_max_object_response[p-1,:]=g_o[2]
    parcel_object_ginicoeff_darray[h][parcelvox]=g[0]
    parcel_object_max_darray[h][parcelvox]=g_o[2][0]

for h in hems:
    newimg=nibabel.gifti.GiftiImage()
    newimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(parcel_ginicoeff_darray[h],
                intent=data[h].darrays[0].intent,
                datatype=data[h].darrays[0].datatype,
                ordering='F',
                meta={'AnatomicalStructurePrimary':'CortexLeft',
                'Name':'parcel-gini-alltasks'}))
    newimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(parcel_max_darray[h],
                intent=data[h].darrays[0].intent,
                datatype=data[h].darrays[0].datatype,
                ordering='F',
                meta={'AnatomicalStructurePrimary':'CortexLeft',
                'Name':'parcel-max-alltasks'}))
    nibabel.gifti.giftiio.write(newimg,os.path.join(outdir,'parcelgini_alltasks.%s.func.gii'%h))
     
    newimg=nibabel.gifti.GiftiImage()
    newimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(parcel_object_ginicoeff_darray[h],
                intent=data[h].darrays[0].intent,
                datatype=data[h].darrays[0].datatype,
                ordering='F',
                meta={'AnatomicalStructurePrimary':'CortexLeft',
                'Name':'parcel-gini-objects'}))
    newimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(parcel_object_max_darray[h],
                intent=data[h].darrays[0].intent,
                datatype=data[h].darrays[0].datatype,
                ordering='F',
                meta={'AnatomicalStructurePrimary':'CortexLeft',
                'Name':'parcel-max-objects'}))
    nibabel.gifti.giftiio.write(newimg,os.path.join(outdir,'parcelgini_objects.%s.func.gii'%h))
       
       
resp_df=pd.DataFrame(parcel_mean_response,columns=tasknames)
resp_df.to_csv(os.path.join(outdir,'parcel_mean_response.txt'),index=False,sep='\t')
numpy.savetxt(os.path.join(outdir,'parcel_gini_alltasks.txt'),parcel_ginicoeff)
# simulate Gini 
# use parametric bootstrap approach
# generate data with same marginal distributions as matrixdata


print 'running gini simulation for null distribution'
nruns=5000
g_rand=numpy.zeros((nruns,620))


for run in range(nruns):
    randdata={}
    sd={'L':numpy.std(matrixdata['L'],1),'R':numpy.std(matrixdata['R'],1)}
    
    randdata['L']=numpy.random.randn(matrixdata['L'].shape[0],matrixdata['L'].shape[1])*sd['L'][:,numpy.newaxis]
    randdata['R']=numpy.random.randn(matrixdata['R'].shape[0],matrixdata['R'].shape[1])*sd['R'][:,numpy.newaxis]
    for p in range(1,621):
        g=compute_gini_for_parcels(randdata,parceldata,h,p)
        g_rand[run,p-1]=g[0]

maxgini=numpy.max(g_rand,1)
cutoff=scipy.stats.scoreatpercentile(maxgini,[90,95])
print cutoff

# [ 0.4721185   0.48350519]