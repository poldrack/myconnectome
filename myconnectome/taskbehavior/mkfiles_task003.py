# -*- coding: utf-8 -*-
"""
set up behavioral files for task003 (object localizer)
Created on Wed Jun 17 16:52:44 2015

@author: poldrack
"""

import os,glob
import numpy

basedir=os.environ['MYCONNECTOME_DIR']
datadir=os.path.join(basedir,'task_behavior/task003')
origfilesdir=os.path.join(datadir,'origfiles')
outdir=os.path.join(basedir,'taskbehav')
if not os.path.exists(outdir):
    os.mkdir(outdir)
   
origdirs=glob.glob(os.path.join(origfilesdir,'sess*'))
origdirs.sort()

subcode='sub00001'


for o in origdirs:
        for r in range(1,3):
            rundata=[]
            rundir=os.path.join(o,'run%d'%r)
            infiles=glob.glob(os.path.join(rundir,'*txt'))
            cond=[]
            for i in infiles:
                condition=os.path.basename(i).replace('.txt','')
                for l in open(i).readlines():
                    l_s=[float(j) for j in l.strip().split('\t')]
                    rundata.append(l_s[:2])
                    cond.append(condition)
            rundata_array=numpy.array(rundata)
            idx=numpy.argsort(rundata_array[:,0])
            sesscode=os.path.basename(o)
            odir=os.path.join(outdir,'%s/%s/%s/functional'%(outdir,subcode,
                                            sesscode))
            if not os.path.exists(odir):
                os.makedirs(odir)
            outfile=os.path.join(odir,'%s_task002_run%03d_events.tsv'%(subcode,r))

            f=open(outfile,'w')
            f.write('onset\tduration\tcondition\n')
            for i in idx:
                f.write('%s\t%s\n'%('\t'.join(['%f'%j for j in rundata[i]]),cond[i]))
            f.close()
            
                
                
        