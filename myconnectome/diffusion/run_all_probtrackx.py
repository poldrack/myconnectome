"""
run probtrackx from each ROI to all others
"""

import os,glob

distcorr=''  # 'no' or set to '' for distcorr

basedir='/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/stanford_diffusion/combined_eddy_corrected'
outdir=os.path.join(basedir,'probtrackx_outputs_%sdistcorr_term'%distcorr)
if not os.path.exists(outdir):
  os.mkdir(outdir)
                    
pathdir=os.path.join(basedir,'tracking_pathfiles')
if not os.path.exists(pathdir):
  os.mkdir(pathdir)

termdir=os.path.join(basedir,'termination_masks')

bpxdir=os.path.join(basedir,'bedpostx_combined.bedpostX')

roidir=os.path.join(basedir,'seed_masks')

nodif=os.path.join(basedir,'bedpostx_combined/nodif_brain_mask.nii.gz')


roipaths=glob.glob(os.path.join(roidir,'parce*'))
roipaths.sort()

                   

# make target mask files

for i in range(len(roipaths)):
    roinum=i+1
    f=open(os.path.join(pathdir,'paths_roi%03d'%roinum),'w')
    for j in range(len(roipaths)):
        if not i==j:
            f.write(roipaths[j]+'\n')
    f.close()


f1=open('run_all_ptx_%sdistcorr_term_set1.sh'%distcorr,'w')
#f2=open('run_all_ptx_%sdistcorr_term_set2.sh'%distcorr,'w')

for i in range(len(roipaths)):

  cmd='probtrackx2 -s %s/merged -m %s -x %s/parcel%03d.nii.gz -o roi%03d --opd --os2t --dir=%s/probtrackx_%sdistcorr_roi%03d --targetmasks=%s/paths_roi%03d --waypoints=%s/wm_dtimask.nii.gz --avoid=%s/csf_dtimask.nii.gz -P 50000  --stop=%s/parcel%03d.nii.gz'%(bpxdir,nodif,roidir,i+1,i+1,outdir,distcorr,i+1,pathdir,i+1,basedir,basedir,termdir,i+1)  # --stop=%s/roi%03d.nii.gz 
  if distcorr=='':
        cmd=cmd+' --pd'
        if i<100000: # (len(roipaths)/2):
          f1.write(cmd+'\n')
        else:
          f2.write(cmd+'\n')
f1.close()
#f2.close()
