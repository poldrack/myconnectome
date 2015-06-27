
import os,glob

datadir='/scratch/01329/poldrack/selftracking/ds031/sub00001'

subcodes=[i.strip().replace('sub','ses') for i in open('/corral-repl/utexas/poldracklab/data/myconnectome/subcodes.txt').readlines()]

sesdirs=glob.glob(os.path.join(datadir,'ses*'))
sesdirs.sort()

print 'found %d sessions'%len(sesdirs)

seslist={}


for s in sesdirs:
    sescode=s.split('/')[-1]
    seslist[sescode]={'T1w':[],'T2w':[],'PDT2':[],'diffusion':[],'fieldmap':[],'task001':[],'task002':[],'task003':[],'task004':[],'task005':[],'task006':[],'task007':[]}
    #print sescode
    for t in range(1,8):
        
        funcfiles=glob.glob(os.path.join(s,'functional/sub00001_%s_task%03d_run*_bold.nii.gz'%(sescode,t)))
        if len(funcfiles)>0:
            for f in funcfiles:
                seslist[sescode]['task%03d'%t].append(f)
        elif sescode in subcodes and t==1:
            print 'functional missing for',sescode
    for anatcode in ['T1w','T2w','PDT2']:
        anatfiles=glob.glob(os.path.join(s,'anatomy/sub00001_%s_%s*.nii.gz'%(sescode,anatcode)))
        for f in anatfiles:
            seslist[sescode][anatcode].append(f)
    fieldmapfiles=glob.glob(os.path.join(s,'fieldmap/sub00001_%s_*_magnitude.nii.gz'%sescode))
    for f in fieldmapfiles:
            seslist[sescode]['fieldmap'].append(f)
    diffusion_files=glob.glob(os.path.join(s,'diffusion/sub00001_%s_dwi_*.nii.gz'%sescode))
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
