"""
set up behavioral files for task001 - working memory
"""

import os,glob,pickle
import numpy

basedir=os.environ['MYCONNECTOME_DIR']
datadir=os.path.join(basedir,'task_behavior/task001')
origfilesdir=os.path.join(datadir,'origfiles')
outdir=os.path.join(basedir,'taskbehav')
if not os.path.exists(outdir):
    os.mkdir(outdir)
   
subcode='sub00001'

origfiles=glob.glob(os.path.join(origfilesdir,'*pkl'))

origfiles.sort()

header='onset\tduration\tstim_type\tnback\ttarget_type\tresponse\tcorrect\tResponseTime\n'
hvars=['onset','duration','stim_type','nback','match','response','correct','rt']
hvartypes=['%f','%f','%s','%d','%d','%s','%d','%f']

for infile in origfiles:
    data=pickle.load(open(infile,'rb'))
    infile=infile.replace('elf-tracking','elf_tracking')
    sessnum=int(os.path.basename(infile).split('_')[2])
    sesscode='sess%03d'%sessnum
    
    outfile=os.path.join(outdir,'%s/%s/%s/functional/%s_task001_run001_events.tsv'%(outdir,subcode,sesscode,subcode))
    if not os.path.exists(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))
    f=open(outfile,'w')
    td=data['trialdata']
    try:
        assert len(td)==180
    except:
        continue
    for i in range(len(td)):
        hit=td[i]['match']==td[i]['nback']
        if not (td[i].has_key('response')):
            td[i]['response']='0'
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