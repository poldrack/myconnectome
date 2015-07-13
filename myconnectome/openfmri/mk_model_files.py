"""
make model.json file for each session
"""

import os,glob,shutil,json
from mvpa2.misc.fsl import read_fsl_design


def get_design_info(d):
    evs=[]
    # this is a hack, assumes no more than 100 evs or cons
    for i in range(100):
        if d.has_key('fmri(custom%d)'%i):
            evs.append(i)
    cons=[]
    for i in range(100):
        if d.has_key('fmri(conname_real.%d)'%i):
            cons.append(i)

    return evs,cons
    
basedir='/Users/poldrack/data_unsynced/myconnectome/selftracking_files' #/corral-repl/utexas/poldracklab/data/selftracking'
outdir='/Users/poldrack/data_unsynced/myconnectome/sub00001' #/scratch/01329/poldrack/selftracking/ds031/sub00001'



indirs=glob.glob(os.path.join(basedir,'sub*/model/model*/*333.feat'))

subcodes=[i.split('/')[6] for i in indirs]
subcodes=list(set(subcodes))
subcodes.sort()

for s in subcodes:
    models={}
    subdirs=[i for i in indirs if i.find(s)>-1]
    for sd in subdirs:
        d=read_fsl_design(os.path.join(sd,'design.fsf'))
        evs,cons=get_design_info(d)
        nevs=len(evs)
        ncons=len(cons)
        
        model_orig=int(sd.split('/')[8].replace('model',''))
        models['task%03d'%int(model_orig+1)]={'model001':{'Variables':{},'Contrasts':{}}}
        
        sesscode=s.replace('sub','ses')
        print sesscode
        od=os.path.join(outdir,'%s/model/task%03d_model001/events'%(sesscode,model_orig+1))
        print od
        if not os.path.exists(od):
            os.makedirs(od)
        onsfiles=glob.glob(os.path.join(sd,'custom_timing_files/*'))
        onsfiles.sort()
        assert nevs==len(onsfiles)
        

        for j in range(nevs):
            evnum=int(os.path.basename(onsfiles[j]).replace('ev','').replace('.txt',''))

            shutil.copy(onsfiles[j],os.path.join(od,'ev%02d.txt'%evnum))
            events=[]
            f=open(onsfiles[j])
            for i in f.readlines():
                events.append([float(x) for x in i.strip().split()])
            
            models['task%03d'%int(model_orig+1)]['model001']['Variables'][evnum]={'VariableName':d['fmri(evtitle%d)'%evnum].replace(' ','_'),
                   'onsets':events}

    
    
        conctr=1
        for c in range(1,ncons+1):
                contrast=[]
                for i in range(nevs):
                    contrast.append(d['fmri(con_orig%d.%d)'%(conctr,i+1)])
                print conctr,contrast
                models['task%03d'%int(model_orig+1)]['model001']['Contrasts'][conctr]={'ContrastVector':contrast}
                models['task%03d'%int(model_orig+1)]['model001']['Contrasts'][conctr]['ContrastName']=d['fmri(conname_orig.%d)'%conctr]
                conctr+=1

    
                
                   
                     
    f=open(os.path.join(outdir,sesscode,'models.json'),'w')
    f.write(json.dumps(models,indent=4))
    f.close()


