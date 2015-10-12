
import os,shutil,glob
from flatten_js import flatten_js
import json

def write_json(outfile,js):
        f=open(outfile,'w')
        f.write(json.dumps(js,indent=4))
        f.close()


def load_json(j):
        l=open(j).readlines()
        try:
            js=json.loads(' '.join([i.strip() for i in l]))
        except:
            js=[]
        return js
 
outdir='/scratch/01329/poldrack/selftracking/ds031/sub-01/ses-106'

if not os.path.exists(outdir):
    os.makedirs(outdir)
    
niftidir='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/raw_nifti/20150515_1108_9697'

basedir='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/dicom/20150515_1108'

anatdir=os.path.join(outdir,'anat')
diffdir=os.path.join(outdir,'dwi')
if not os.path.exists(anatdir):
    os.mkdir(anatdir)
if not os.path.exists(diffdir):
    os.mkdir(diffdir)


ext='json'
jsflat=flatten_js(load_json(os.path.join(basedir,'9697_2_1_dicoms/T2w.%s'%ext)))
write_json(os.path.join(anatdir,'sub-01_ses-106_T2w.%s'%ext),jsflat)

jsflat=flatten_js(load_json(os.path.join(basedir,'9697_13_1_dicoms/T1w.%s'%ext)))
write_json(os.path.join(anatdir,'sub-01_ses-106_T1w.%s'%ext),jsflat)


if not os.path.exists( os.path.join(anatdir,'sub-01_ses-106_T1w.nii.gz')):
	shutil.copy(os.path.join(niftidir,'9697_13_1_T1w_1mm_ax/9697_13_1.nii.gz'),os.path.join(anatdir,'sub-01_ses-106_T1w.nii.gz'))
if not os.path.exists(os.path.join(anatdir,'sub-01_ses-106_T2w.nii.gz')):
	shutil.copy(os.path.join(niftidir,'9697_2_1_T2w_CUBE_8mm_sag/9697_2_1.nii.gz'),os.path.join(anatdir,'sub-01_ses-106_T2w.nii.gz'))

dirnames=[5,6,8,9]
directions=['AP','PA','AP','PA']

for i in range(len(dirnames)):
    jsfile=glob.glob(os.path.join(basedir,'9697_%s_1_dicoms/dti*.json'%dirnames[i]))
    jsflat=flatten_js(load_json(jsfile[0]))
    jsflat['GradientEncodingDirection']=directions[i]
    jsflat['EffectiveEchoSpacing']=0.7520/1000.
    write_json(os.path.join(diffdir,'sub-01_ses-106_run-%03d_dwi.json'%int(i+1)),jsflat)

    nifile=glob.glob(os.path.join(niftidir,'9697_%d_*/*.nii.gz'%dirnames[i]))[0]
    shutil.copy(nifile,os.path.join(diffdir,'sub-01_ses-106_run-%03d_dwi.nii.gz'%int(i+1)))

    shutil.copy(nifile.replace("nii.gz",'bval'),os.path.join(diffdir,'sub-01_ses-106_run-%03d_dwi.bval'%int(i+1)))
    shutil.copy(nifile.replace("nii.gz",'bvec'),os.path.join(diffdir,'sub-01_ses-106_run-%03d_dwi.bvec'%int(i+1)))

    
    

