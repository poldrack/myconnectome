"""
set up behavioral files for task002 - working memory (originally called task001 - but now rest is 001)
"""

import os,glob,pickle
import numpy


datadir=os.path.join('/corral-repl/utexas/poldracklab/data/selftracking/task_behavior/task001')
origfilesdir=os.path.join(datadir,'origfiles')
outdir=os.path.join('/scratch/01329/poldrack/selftracking/ds031')
if not os.path.exists(outdir):
    os.mkdir(outdir)
   
subcode='sub-01'

origfiles=glob.glob(os.path.join(origfilesdir,'*pkl'))

origfiles.sort()

header='onset\tduration\tstim_type\tnback\ttarget_type\tresponse\tcorrect\tResponseTime\n'
hvars=['onset','duration','stim_type','nback','match','response','correct','rt']
hvartypes=['%f','%f','%s','%d','%d','%s','%d','%f']

for infile in origfiles:
    data=pickle.load(open(infile,'rb'))
    infile=infile.replace('elf-tracking','elf_tracking')
    sessnum=int(os.path.basename(infile).split('_')[2])

    sesscode='ses-%03d'%sessnum
    
    outfile=os.path.join(outdir,'%s/%s/%s/func/%s_%s_task-nback_run-001_events.tsv'%(outdir,subcode,sesscode,subcode,sesscode))
    if not os.path.exists(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))
    f=open(outfile,'w')
    f.write(header+'\n')
    td=data['trialdata']
    try:
        assert len(td)==180
    except:
        continue
    for i in range(len(td)):
        hit=td[i]['match']==td[i]['nback']
        if not (td[i].has_key('response')):
            td[i]['response']='n/a'
        if not (td[i].has_key('rt')):
            td[i]['rt']=0.0
        if (hit and td[i]['response']=='4') or ((not hit) and td[i]['response']=='1'):
            td[i]['correct']=1
        else:
            td[i]['correct']=0
        datalist=[]
        for j in range(len(hvars)):
            if hvartypes[j]=='%s':
                datalist.append(td[i][hvars[j]])
            elif hvartypes[j]=='%f':
                datalist.append('%f'%td[i][hvars[j]])
            elif hvartypes[j]=='%d':
                datalist.append('%d'%td[i][hvars[j]])
            
                
        f.write('%s\n'%('\t'.join(datalist)))
            
    f.close()   
