# -*- coding: utf-8 -*-
"""
analysis for task002 - stop signal (now called task003)

Created on Wed Jun 17 13:51:20 2015

@author: poldrack
"""

import os,glob
import numpy

datadir=os.path.join('/corral-repl/utexas/poldracklab/data/selftracking/task_behavior/task002')
origfilesdir=os.path.join(datadir,'origfiles')
outdir=os.path.join('/scratch/01329/poldrack/selftracking/ds031')


if not os.path.exists(outdir):
    os.mkdir(outdir)
   
subcode='sub-01'

sesscodes=['ses-083','ses-084','ses-085','ses-086','ses-088','ses-089','ses-091','ses-092','ses-093']

loghdr=['SesNo','Trial','BlockAncher','PrepOn','StimOn','StimOff']
datahdr=['onset','duration','TrialType','Coherence','Response','ResponseTime','Correct','CorrStop','SSD']

for sess in range(len(sesscodes)):
    logdata=numpy.loadtxt(os.path.join(origfilesdir,'stopSigRDM_log_ses_%d.txt'%int(sess+1)),
                          skiprows=2,usecols=range(6))
    data=numpy.loadtxt(os.path.join(origfilesdir,'stopSigRDM_ses_%d.txt'%int(sess+1)),
                       usecols=range(2,9),skiprows=2)
    
    datavars=[]
    onsets=logdata[:,4] - logdata[:,2]
    duration=logdata[:,5]-logdata[:,3]
    data=numpy.hstack((onsets[:,None],duration[:,None],data))  
    outfile=os.path.join(outdir,'%s/%s/%s/func/%s_%s_task-dotstop_run001_events.tsv'%(outdir,subcode,
                                            sesscodes[sess],subcode,sesscodes[sess]))
    if not os.path.exists(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))
    numpy.savetxt(outfile,data,header='\t'.join(datahdr),delimiter='\t',comments='')
        
