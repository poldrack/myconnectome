"""
get onsets for grid data - now called atsk006

REGULAR timing:

300		pre-trial fixation
4200	presentation of the materials (350 ms x 12 words)
1000	probe presentation
500		post-trial fixation (subjects can respond to the probe as soon as it appears and until the end of the post-trial fixation)
TOTAL: 6000 ms (i.e., there will be 3 trials in each block)

fixations last 18 seconds

"""

import os,sys,glob
import numpy

datadir=os.path.join('/corral-repl/utexas/poldracklab/data/selftracking/task_behavior/task005')
origfilesdir=os.path.join(datadir,'origfiles')
outdir=os.path.join('/scratch/01329/poldrack/selftracking/ds031')


if not os.path.exists(outdir):
    os.mkdir(outdir)
   
subcode='sub-01'

origfiles=glob.glob(os.path.join(origfilesdir,'*csv'))


for datafile in origfiles:
    subnum=int(datafile.split('_')[-3])
    sesscode='ses-%03d'%subnum
    onsets=[]

    f=open(datafile)
    hdr=f.readline()
    for l in f.readlines():
        l_s=l.strip().split(',')
        onstime=float(l_s[6])
        probetime=float(l_s[7])
        try:
            resptime='%f'%float(l_s[-1])
            accuracy='%d'%int(l_s[-2])
        except:
            resptime='n/a'
            accuracy='n/a'
        onsets.append(['%f'%onstime,'4.5',l_s[8],'n/a','n/a'])
        onsets.append(['%f'%probetime,'1',l_s[8]+'-probe',resptime,accuracy])
        #onsets.append(['%f'%probetime,])
    
  
    outfile=os.path.join(outdir,'%s/%s/func/%s_%s_task-spatialwm_run-001_events.tsv'%(subcode,sesscode,subcode,sesscode))

    f=open(outfile,'w')
    f.write('onset\tduration\tcondition\trt\taccuracy\n')
    for i in onsets:
        f.write('%s\n'%'\t'.join(i))
    f.close()
    
