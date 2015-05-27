"""
map example func and stats images to surface
"""

import os,sys,glob
from run_shell_cmd import run_shell_cmd
import tempfile

sys.path.insert(0,'/home1/01329/poldrack/code/nipype')
sys.path.append('/corral-repl/utexas/poldracklab/code/poldrack/selftracking')
scriptdir='/corral-repl/utexas/poldracklab/data/selftracking/code'
base_dir=os.path.abspath('/corral-repl/utexas/poldracklab/data/selftracking/')

try:
    subcode=sys.argv[1]

    taskcode=int(sys.argv[2])
    runcode=int(sys.argv[3])
    assert os.path.exists(os.path.join(base_dir,subcode,'model/model%03d/task%03d_run%03d.feat'%(taskcode,taskcode,runcode)))
    
except:
    subcode='sub091'
    taskcode=2
    runcode=1

import nipype.interfaces.fsl as fsl

featdir=os.path.join(base_dir,subcode,'model/model%03d/task%03d_run%03d_333.feat'%(taskcode,taskcode,runcode))

exfunc=os.path.join(featdir,'example_func.nii.gz')

surfaces={}
surfaces['midthickness']={'L':'/corral-repl/utexas/poldracklab/data/selftracking/FREESURFER_fs_LR/7112b_fs_LR/fsaverage_LR32k/sub013.L.midthickness.32k_fs_LR.surf.gii','R':'/corral-repl/utexas/poldracklab/data/selftracking/FREESURFER_fs_LR/7112b_fs_LR/fsaverage_LR32k/sub013.R.midthickness.32k_fs_LR.surf.gii'}
surfaces['white']={'L':'/corral-repl/utexas/poldracklab/data/selftracking/FREESURFER_fs_LR/7112b_fs_LR/fsaverage_LR32k/sub013.L.white.32k_fs_LR.surf.gii','R':'/corral-repl/utexas/poldracklab/data/selftracking/FREESURFER_fs_LR/7112b_fs_LR/fsaverage_LR32k/sub013.R.white.32k_fs_LR.surf.gii'}
surfaces['pial']={'L':'/corral-repl/utexas/poldracklab/data/selftracking/FREESURFER_fs_LR/7112b_fs_LR/fsaverage_LR32k/sub013.L.pial.32k_fs_LR.surf.gii','R':'/corral-repl/utexas/poldracklab/data/selftracking/FREESURFER_fs_LR/7112b_fs_LR/fsaverage_LR32k/sub013.R.pial.32k_fs_LR.surf.gii'}

tasknames={1:{1:'nback',2:'dotmotion',3:'faceloc1',4:'superloc',5:'grid'},2:{1:'nback',2:'dotmotion',3:'faceloc2',4:'superloc',5:'grid'}}

newstatsdir=os.path.join(featdir,'stats_pipeline')
if not os.path.exists(newstatsdir):
    os.mkdir(newstatsdir)

for filetype in ['cope','varcope','zstat']:
  copefiles=glob.glob(os.path.join(featdir,'stats/%s*.nii.gz'%filetype))
  for c in copefiles:
    copenum=int(c.split('/')[-1].split('.')[0].replace(filetype,''))
    for hemis in ['L','R']:
        outfile=os.path.join(newstatsdir,'%s%03d.%s.func.gii'%(filetype,copenum,hemis))
        goodvoxmask=os.path.join('/corral-repl/utexas/poldracklab/data/selftracking/volume_goodvoxels','%s_%s_goodvoxels_333.nii.gz'%(subcode,tasknames[runcode][taskcode]))
        assert os.path.exists(goodvoxmask)
                                 
        wb_command='wb_command -volume-to-surface-mapping %s %s %s -ribbon-constrained %s %s  -volume-roi %s'%(c,surfaces['midthickness'][hemis],outfile,surfaces['white'][hemis],surfaces['pial'][hemis],goodvoxmask)
        if not os.path.exists(outfile):
            print wb_command
            run_shell_cmd(wb_command)
        if hemis=='L':
            structure='CORTEX_LEFT'
        else:
            structure='CORTEX_RIGHT'
        wb_command='wb_command -set-structure %s %s'%(outfile,structure)
        print wb_command
        run_shell_cmd(wb_command)
        wb_command= 'wb_command -metric-smoothing %s %s 1.5 %s'%(surfaces['midthickness'][hemis],outfile,outfile.replace('func.','smoothed.func.'))
        print wb_command
        run_shell_cmd(wb_command)

        
    

    
