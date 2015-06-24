"""
convert data from washu
"""

import os,glob,shutil
from run_shell_cmd import run_shell_cmd

basedir='/scratch/01329/poldrack/selftracking/washu'
outbase='/scratch/01329/poldrack/selftracking/ds031/sub00001/ses105/functional'



infiles=glob.glob(os.path.join(basedir,'part*nii.gz'))
infiles.sort()

for i in range(len(infiles)):
    infile=infiles[i]
    outfile=os.path.join(outbase,'sub00001_ses105_task001_run%03d_bold.nii.gz'%int(i+1))
    if not os.path.exists(outfile):
        shutil.copy(infile,outfile)
    jsonfile=outfile.replace('.nii.gz','.json')
    if not os.path.exists(jsonfile):
        shutil.copy(infile.replace('.nii.gz','.json'),jsonfile)
