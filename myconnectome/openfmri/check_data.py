
import os,glob

datadir='/scratch/01329/poldrack/selftracking/ds031/sub-01'

subcodes=[i.strip().replace('sub','ses') for i in open('/corral-repl/utexas/poldracklab/data/selftracking/sub-01_good_sessions.tsv').readlines()]

sesdirs=glob.glob(os.path.join(datadir,'ses*'))
sesdirs.sort()

print 'found %d sessions'%len(sesdirs)

seslist={}
task_codes=['rest','nback','dotstop','objects','languagewm','spatialwm','breathhold','retinotopy']


for s in sesdirs:
    sescode=s.split('/')[-1]
    seslist[sescode]={'T1w':[],'T2w':[],'PDT2':[],'diffusion':[],'fieldmap':[]}
    for t in task_codes:
        seslist[sescode][t]=[]

    found_func=0
    for t in range(len(task_codes)):
        funcfiles=glob.glob(os.path.join(s,'func/sub-01_%s_task-%s_acq-MB_run*_bold.nii.gz'%(sescode,task_codes[t])))
        if len(funcfiles)>0:
            found_func=1
            for f in funcfiles:
                seslist[sescode][task_codes[t]].append(f)
    if found_func==0:
            print 'functional missing for',sescode

    for anatcode in ['T1w','T2w','PDT2']:
        anatfiles=glob.glob(os.path.join(s,'anat/sub-01_%s_run*_%s.nii.gz'%(sescode,anatcode)))
        for f in anatfiles:
            seslist[sescode][anatcode].append(f)
    fieldmapfiles=glob.glob(os.path.join(s,'fmap/sub-01_%s_magnitude.nii.gz'%sescode))
    for f in fieldmapfiles:
            seslist[sescode]['fieldmap'].append(f)
    diffusion_files=glob.glob(os.path.join(s,'dwi/sub-01_%s_run*_dwi.nii.gz'%sescode))
    for f in diffusion_files:
            seslist[sescode]['diffusion'].append(f)

runs={}
sessions={}
for k in seslist[sescode].iterkeys():
    runs[k]=0
    sessions[k]=[]
    for s in seslist.iterkeys():
        runs[k]+=len(seslist[s][k])
        if len(seslist[s][k])>0:
            sessions[k]=sessions[k]+seslist[s][k]
for k in sessions.iterkeys():
    print k,len(sessions[k])
