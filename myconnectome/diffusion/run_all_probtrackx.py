"""
run probtrackx from each ROI to all others
"""

import os

distcorr=''  # 'no' or set to '' for distcorr

outdir='/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/DTI/probtrackx_outputs_%sdistcorr_term'%distcorr
pathdir='/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/DTI/tracking_pathfiles'
termdir='/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/DTI/termination_masks'
bpxdir='/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/DTI/merged.bedpostX'
roidir='/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/DTI/parcels_dtispace'
nodif='/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/DTI/merged/nodif_brain_mask.nii.gz'

f=open("roipaths.txt")
roipaths=f.readlines()
f.close()

# make target mask files
if 0:
  for i in range(len(roipaths)):
    roinum=i+1
    f=open(os.path.join(pathdir,'paths_roi%03d'%roinum),'w')
    for j in range(len(roipaths)):
        if not i==j:
            f.write(roipaths[j])
    f.close()

  
f=open('run_all_ptx_%sdistcorr_term.sh'%distcorr,'w')
for i in range(len(roipaths)):
    if i<310:
        hemis='L'
    elif i>619:
        hemis='S'
    else:
        hemis='R'
    
    cmd='probtrackx2 -s %s/merged -m %s -x %s/parcels.%s.bin.clean.%03d.nii.gz -o roi%03d --opd --os2t --dir=%s/probtrackx_%sdistcorr_roi%03d --targetmasks=%s/paths_roi%03d --waypoints=wm_dtimask.nii.gz --avoid=csf_dtimask.nii.gz -P 20000  --stop=%s/roi%03d.nii.gz'%(bpxdir,nodif,roidir,hemis,i+1,i+1,outdir,distcorr,i+1,pathdir,i+1,termdir,i+1)  # --stop=%s/roi%03d.nii.gz 
    if distcorr=='':
        cmd=cmd+' --pd'
    f.write(cmd+'\n')
f.close()
