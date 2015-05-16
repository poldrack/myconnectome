"""
do encoding model across sessions
"""

import os,glob
import nibabel.gifti.giftiio
import numpy
import statsmodels.api as sm

def get_codes():
    f=open('contrast_annotation.txt')
    header=f.readline().strip().split('\t')
    nvars=len(header)-3
    names={}
    coding={}

    lines=f.readlines()
    for l in lines:
        l_s=l.strip().split('\t')
        tasknum=int(l_s[0])
        contrastnum=int(l_s[1])
        taskname=l_s[2]
        codes=[]
        for i in range(nvars):
            try:
                codes.append(int(l_s[i+3]))
            except:
                codes.append(0)
        if not coding.has_key(tasknum):
            coding[tasknum]={}
        coding[tasknum][contrastnum]=codes
    return coding,header[3:]

def get_files(coding):

    files=[]
    taskcodes=[]
    for t in coding.keys():
        for c in coding[t].keys():
            
            tcfiles=glob.glob('/corral-repl/utexas/poldracklab/data/selftracking/sub*/model/model%03d/task%03d*333.feat/stats_pipeline/zstat%03d.R.smoothed.func.gii'%(t,t,c))

            for f in tcfiles:
                files.append(f)
                taskcodes.append([t,c])
    return files,taskcodes

def load_data(files):
    contrastdata=numpy.zeros((len(files),32492*2))

    for i in range(len(files)):
        f=files[i]
        rh=nibabel.gifti.giftiio.read(f).darrays[0].data
        lh=nibabel.gifti.giftiio.read(f.replace('.R.','.L.')).darrays[0].data
        contrastdata[i,:]=numpy.hstack((lh,rh))
    return contrastdata                      


def get_design_matrix(coding,taskcodes):
    desmtx=[]
    for t in taskcodes:
        desmtx.append(coding[t[0]][t[1]])
    desmtx=numpy.array(desmtx)
    return desmtx

try:
    beta_hat=numpy.load('/Users/poldrack/data/selftracking/task_encoding_model/encoding_beta.npy')
    names=['face',
 'place',
 'manmade_objects',
 'words',
 'characters',
 'body_parts',
 'novel_characters',
 'response',
 'responsetime',
 'motion',
 'number',
 'maintenance',
 'manipulation',
 'inhibition',
 'error_detection']
 
except:
    coding,names=get_codes()

    files,taskcodes=get_files(coding)

    contrastdata=load_data(files)

    desmtx=get_design_matrix(coding,taskcodes)
    desmtx=sm.add_constant(desmtx)
    
    tstat=numpy.zeros(contrastdata.shape[1])
    for i in range(contrastdata.shape[1]):
        reg=sm.OLS(contrastdata[:,i],desmtx)
        results=reg.fit()
        tstat=results
    
lh=nibabel.gifti.GiftiImage()
rh=nibabel.gifti.GiftiImage()
nvert=32492

for i in range(beta_hat.shape[0]):
    darray_lh=beta_hat[i,:nvert].astype(numpy.float32)
    lh.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_lh,
            intent=11,
            datatype=16,
            ordering='F',
            meta={'AnatomicalStructurePrimary':'CortexLeft',
            'Name':'tstat%d'%int(i+1)}))
        
    darray_rh=beta_hat[i,nvert:].astype(numpy.float32)
    rh.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_rh,
            intent=11,
            datatype=16,
            ordering='F',
            meta={'AnatomicalStructurePrimary':'CortexRight',
            'Name':'tstat%d-%s'%(int(i+1),names[i])}))
nibabel.gifti.giftiio.write(lh,'/Users/poldrack/Dropbox/data/selftracking/task_encoding_model/encoding_beta.LH.func.gii')
nibabel.gifti.giftiio.write(rh,'/Users/poldrack/Dropbox/data/selftracking/task_encoding_model/encoding_beta.RH.func.gii')
