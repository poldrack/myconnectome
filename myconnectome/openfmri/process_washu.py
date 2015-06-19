"""
convert data from washu
"""

import os,glob
from run_shell_cmd import run_shell_cmd

basedir='/scratch/01329/poldrack/selftracking/ds031/washu'
outbase='/scratch/01329/poldrack/selftracking/ds031/washu/nifti'



inputdirs=['vc39556','vc39556_2']
inputdirs=[os.path.join(basedir,i) for i in inputdirs]

for i in range(len(inputdirs)):
    indir=inputdirs[i]
    subcode='sub%03d'%int(i+200)
    incode=os.path.basename(indir)
    outdir=os.path.join(outbase,subcode)

    if not os.path.exists(outdir):
        os.mkdir(outdir)

    scan_info=[i.strip().split() for i in open(os.path.join(indir,'%s.studies.txt'%incode)).readlines()]

    boldctr=1
    for series in range(len(scan_info)):
        if scan_info[series][2].find('RSFC')==0:
            studydir=os.path.join(indir,'study%d'%int(series+1))
            imafile=glob.glob(os.path.join(studydir,'*.IMA'))[0]
            seriesdir=os.path.join(outdir,'BOLD/rest_run%03d'%boldctr)
            if not os.path.exists(seriesdir):
                os.makedirs(seriesdir)
            outfile=os.path.join(seriesdir,'bold.nii.gz')
            cmd='mri_convert %s %s'%(imafile,outfile)
            print cmd
            run_shell_cmd(cmd)
            boldctr+=1
    
