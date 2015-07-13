"""
copy onset files
"""

import os,glob,shutil,json
from mvpa2.misc.fsl import read_fsl_design

basedir='/corral-repl/utexas/poldracklab/data/selftracking'
outdir='/scratch/01329/poldrack/selftracking/ds031/sub00001'

models={}


for model in range(1,6):
    models['task%03d'%int(model+1)]={'model001':{'Variables':{},'Contrasts':{}}}
    indirs=glob.glob(os.path.join(basedir,'sub*/model/model%03d/*333.feat'%model))
    print indirs
    for i in indirs:
        sesscode=i.split('/')[6].replace('sub','ses')
        print sesscode
        od=os.path.join(outdir,'%s/model/task%03d_model001/events'%(sesscode,model+1))
        print od
        if not os.path.exists(od):
            os.makedirs(od)
        onsfiles=glob.glob(os.path.join(i,'custom_timing_files/*'))
        nevs=0
        for j in range(len(onsfiles)):
            evnum=int(os.path.basename(onsfiles[j]).replace('ev','').replace('.txt',''))
            shutil.copy(onsfiles[j],os.path.join(od,'ev%02d.txt'%evnum))
            events=[]
            f=open(onsfiles[j])
            for i in f.readlines():
                events.append([float(x) for x in i.strip().split()])
            nevs+=1
            
            models['task%03d'%int(model+1)]['model001']['Variables'][d['fmri(evtitle%d)'%ctr].replace(' ','_')]={'onsets':events}

    d=read_fsl_design(os.path.join(indirs[0],'design.fsf'))


    conctr=1
    while 1:
        try:
            contrast=[]
            for i in range(nevs):
                contrast.append(d['fmri(con_orig%d.%d)'%(conctr,i+1)])
            print conctr,contrast
            models['task%03d'%int(model+1)]['model001']['Contrasts'][conctr]={'vector':contrast}
            models['task%03d'%int(model+1)]['model001']['Contrasts'][conctr]['name']=d['fmri(conname_orig.%d)'%conctr]
            conctr+=1
        except:
            break
        #asdf
            
                      
                     
f=open(os.path.join(os.path.dirname(outdir),'models.json'),'w')
f.write(json.dumps(models,indent=4))
f.close()


