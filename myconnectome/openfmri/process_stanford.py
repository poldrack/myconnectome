
import os,shutil,glob

outdir='/scratch/01329/poldrack/selftracking/ds031/sub00001/ses106'

if not os.path.exists(outdir):
    os.mkdir(outdir)
    
niftidir='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/raw_nifti/20150515_1108_9697'

basedir='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/dicom/20150515_1108'

anatdir=os.path.join(outdir,'anatomy')
diffdir=os.path.join(outdir,'diffusion')
if not os.path.exists(anatdir):
    os.mkdir(anatdir)
if not os.path.exists(diffdir):
    os.mkdir(diffdir)


ext='json'
shutil.copy(os.path.join(basedir,'9697_2_1_dicoms/T2w.%s'%ext),os.path.join(outdir,'anatomy/T2w.%s'%ext))
shutil.copy(os.path.join(basedir,'9697_13_1_dicoms/T1w.%s'%ext),os.path.join(outdir,'anatomy/T1w.%s'%ext))

shutil.copy(os.path.join(niftidir,'9697_13_1_T1w_1mm_ax/9697_13_1.nii.gz'),
            os.path.join(outdir,'anatomy/T1w.nii.gz'))
shutil.copy(os.path.join(niftidir,'9697_2_1_T2w_CUBE_8mm_sag/9697_2_1.nii.gz'),
            os.path.join(outdir,'anatomy/T2w.nii.gz'))

dirnames=[5,6,8,9]
for i in range(len(dirnames)):
    jsfile=glob.glob(os.path.join(basedir,'9697_%s_1_dicoms/dti*.json'%dirnames[i]))

    shutil.copy(jsfile[0],os.path.join(outdir,'diffusion/sub00001_ses106_dwi_%03d.json'%int(i+1)))

    nifile=glob.glob(os.path.join(niftidir,'9697_%d_*/*.nii.gz'%dirnames[i]))[0]
    shutil.copy(nifile,os.path.join(outdir,'diffusion/sub00001_ses106_dwi_%03d.nii.gz'%int(i+1)))

    shutil.copy(nifile.replace("nii.gz",'bval'),os.path.join(outdir,'diffusion/sub00001_ses106_dwi_%03d.bval'%int(i+1)))
    shutil.copy(nifile.replace("nii.gz",'bvec'),os.path.join(outdir,'diffusion/sub00001_ses106_dwi_%03d.bvec'%int(i+1)))

    
    

