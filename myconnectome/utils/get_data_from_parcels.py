"""
map nifti image images to surface and extract parcels
"""

import os,sys,glob,shutil
from run_shell_cmd import run_shell_cmd
import tempfile
import nibabel.gifti.giftiio
import numpy

basedir=os.path.abspath('/Users/poldrack/data_unsynced/myconnectome')

save_gii=True

surfaces={}
surfaces['midthickness']={'L':os.path.join(basedir,'fsaverage_LR32k/sub013.L.midthickness.32k_fs_LR.surf.gii'),
    'R':os.path.join(basedir,'fsaverage_LR32k/sub013.R.midthickness.32k_fs_LR.surf.gii')}
surfaces['white']={'L':os.path.join(basedir,'fsaverage_LR32k/sub013.L.white.32k_fs_LR.surf.gii'),
    'R':os.path.join(basedir,'fsaverage_LR32k/sub013.R.white.32k_fs_LR.surf.gii')}
surfaces['pial']={'L':os.path.join(basedir,'fsaverage_LR32k/sub013.L.pial.32k_fs_LR.surf.gii'),
    'R':os.path.join(basedir,'fsaverage_LR32k/sub013.R.pial.32k_fs_LR.surf.gii')}

parcellations={'L':os.path.join(basedir,'parcellation/all_selected_L_new_parcel_renumbered.func.gii'),
                'R':os.path.join(basedir,'parcellation/all_selected_R_new_parcel_renumbered.func.gii')}

volfile=os.path.join(basedir,'parcellation/84sub_all_startpos50_parcels_TRIO_111.nii.gz')


parcels={}
parceldata={}
  
for hemis in ['L','R']:
    tmpfile=tempfile.mkstemp(suffix='.%s.func.gii'%hemis)
    os.close(tmpfile[0])
    outfile=tmpfile[1]
    print outfile
    
    wb_command='wb_command -volume-to-surface-mapping %s %s %s -ribbon-constrained %s %s'%(volfile,
            surfaces['midthickness'][hemis],outfile,surfaces['white'][hemis],surfaces['pial'][hemis])
    print wb_command
    run_shell_cmd(wb_command)
    if hemis=='L':
            structure='CORTEX_LEFT'
    else:
            structure='CORTEX_RIGHT'
    wb_command='wb_command -set-structure %s %s'%(outfile,structure)
    print wb_command
    run_shell_cmd(wb_command)
    
    surfdata=nibabel.gifti.giftiio.read(outfile)
    parcels[hemis]=nibabel.gifti.giftiio.read(parcellations[hemis])
    

    for i in numpy.unique(parcels[hemis].darrays[0].data):
        if i==0:
            continue
        parcelvertices=parcels[hemis].darrays[0].data==i
        parceldata[i]=[]
        for da in range(len(surfdata.darrays)):
            parceldata[i].append(numpy.mean(surfdata.darrays[da].data[parcelvertices]))
    
    if save_gii:
        shutil.move(outfile,volfile.replace('nii.gz','%s.func.gii'%hemis))
    else:
        os.remove(outfile)
    
nparcs=len(parceldata)
ntp=len(parceldata[parceldata.keys()[0]])
parcs=numpy.unique(parceldata.keys())
parcs.sort()

parcmtx=numpy.zeros((nparcs,ntp))
for p in range(len(parcs)):
    parcmtx[p]=parceldata[parcs[p]]
    
   
