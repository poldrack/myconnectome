"""
do encoding model across sessions
"""

import os,glob,sys,ctypes
import nibabel.gifti.giftiio
import numpy
import sklearn.linear_model
from myconnectome.utils.array_to_gifti import array_to_gifti_32k

print sklearn.linear_model.__file__

def get_codes():
    f=open('contrast_annotation.txt')
    header=f.readline().strip().split('\t')
    nvars=len(header)-3

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
    desmtx=desmtx-numpy.mean(desmtx,0)
    df = desmtx.shape[0] - desmtx.shape[1]
    
    tstat=numpy.zeros((desmtx.shape[1],32492*2))
    lrand_scores=numpy.zeros((desmtx.shape[1],32492*2))
    betahat=numpy.zeros((desmtx.shape[1],32492*2))
    badctr=0
    lrand=sklearn.linear_model.RandomizedLasso(n_jobs=11)
    lr=sklearn.linear_model.Lasso(alpha=0.01)

    for i in range(contrastdata.shape[1]):
        y=contrastdata[:,i]-numpy.mean(contrastdata[:,i])
        lrand.fit(desmtx,y)
        lr.fit(desmtx,y)
        resid=y-desmtx.dot(lr.coef_)
        sse=numpy.dot(resid,resid)/float(df)
        tstat[:,i]=lr.coef_/sse
        betahat[:,i]=lr.coef_
        lrand_scores[:,i]=lrand.scores_


tstat[numpy.isnan(tstat)]=0

lh=nibabel.gifti.GiftiImage()
rh=nibabel.gifti.GiftiImage()
nvert=32492

array_to_gifti_32k(tstat,'/corral-repl/utexas/poldracklab/data/selftracking/analyses/task_analyses/encoding_tstat_lasso',names)
array_to_gifti_32k(lrand_scores,'/corral-repl/utexas/poldracklab/data/selftracking/analyses/task_analyses/encoding_randlasso_scores',names)


