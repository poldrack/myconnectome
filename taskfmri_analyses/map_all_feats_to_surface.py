import os,glob

featdirs=glob.glob('/corral-repl/utexas/poldracklab/data/selftracking/sub*/model/mode*/task*333.feat')

for f in featdirs:
    fd=f.split('/')[-1].split('.')[0]
    subcode=f.split('/')[-4]
    tasknum=int(fd.split('_')[0].replace('task',''))
    runnum=int(fd.split('_')[1].replace('run',''))
    cmd='python map_feats_to_surface.py %s %d %d'%(subcode,tasknum,runnum)
    print cmd
