"""
get onsets for superloc data - now called task005

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

datadir=os.path.join('/corral-repl/utexas/poldracklab/data/selftracking/task_behavior/task004')
origfilesdir=os.path.join(datadir,'origfiles')
outdir=os.path.join('/scratch/01329/poldrack/selftracking/ds031')

if not os.path.exists(outdir):
    os.mkdir(outdir)
   
subcode='sub-01'

origfiles=glob.glob(os.path.join(origfilesdir,'*csv'))

for datafile in origfiles:
    subnum=int(datafile.split('_')[-2])
    sesscode='ses-%03d'%subnum
    onsets=[]
    
    ons_counter=0.0
    f=open(datafile)
    hdr=f.readline()
    for l in f.readlines():
        l_s=l.strip().split(',')
        
        if l_s[1]=='fixation':
            ons_counter+=18
            continue
        try:
            rt='%f'%float(l_s[-1])
            acc='%d'%int(l_s[-2])
        except:
            rt='n/a'
            acc='n/a'
            
        onsets.append(['%f'%float(ons_counter+0.3),'4.2',l_s[1],'n/a','n/a'])
        onsets.append(['%f'%float(ons_counter+4.5),'1.0',l_s[1]+'-probe','%s'%rt,'%s'%acc])
        ons_counter+=6

    events=[]
  
    outfile=os.path.join(outdir,'%s/%s/func/%s_%s_task-languagewm_run-001_events.tsv'%(subcode,sesscode,subcode,sesscode))
    print outfile

    
    f=open(outfile,'w')
    f.write('onset\tduration\tcondition\trt\taccuracy\n')
    for i in onsets:
        f.write('%s\n'%'\t'.join(i))
    f.close()
    
