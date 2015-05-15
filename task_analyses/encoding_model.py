"""
do encoding model across sessions
"""

import os,glob
import nibabel.gifti.giftiio
import numpy

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
        codes=[]
        for i in range(nvars):
            try:
                codes.append(int(l_s[i+3]))
            except:
                codes.append(0)
        if not coding.has_key(tasknum):
            coding[tasknum]={}
        coding[tasknum][contrastnum]=codes
    return coding

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

coding=get_codes()

files,taskcodes=get_files(coding)

contrastdata=load_data(files)

desmtx=get_design_matrix(coding,taskcodes)

beta_hat=numpy.linalg.inv(desmtx.T.dot(desmtx)).dot(desmtx.T.dot(contrastdata))

