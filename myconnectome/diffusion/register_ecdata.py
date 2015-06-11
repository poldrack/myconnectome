"""
run bedpostx on eddy-corrected data


"""

import os,sys,shutil
import glob
import numpy

import nipype.interfaces.fsl as fsl
import nibabel as nib
from nipype.workflows.dmri.fsl.dti import create_bedpostx_pipeline


basedir=os.path.abspath('/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/')
codedir='/scratch/projects/UT/poldracklab/poldrack/selftracking/myconnectome/myconnectome/diffusion'

f=open(os.path.join(codedir,'run_all_individual_bedpost.sh'),'w')

datafiles=glob.glob(os.path.join(basedir,'stanford_diffusion/9697/*ec.nii.gz'))

for ecdata in datafiles:
    ecpath=os.path.basename(ecdata)
    mean_eclowb=ecdata.replace('_ec.nii.gz','_ec_lowb.nii.gz')

    if not os.path.exists(mean_eclowb):
        ecimg=nib.load(ecdata)
        eddy_data=ecimg.get_data()
        bvals=numpy.loadtxt(ecdata.replace('.nii.gz','.bval'))
        lowb=numpy.where(bvals==0)
        lowb=eddy_data[:,:,:,lowb]
        mean_lowb=numpy.mean(lowb,3)
        lowb_img=nib.Nifti1Image(mean_lowb,affine=ecimg.get_affine())
        lowb_img.to_filename(mean_eclowb)

    mean_eclowb_mask=ecdata.replace('_ec.nii.gz','_ec_lowb_brain.nii.gz')
    if not os.path.exists(mean_eclowb_mask):
        bet=fsl.BET()
        bet.inputs.in_file=mean_eclowb
        bet.inputs.out_file=mean_eclowb_mask
        bet.inputs.mask=True
        bet.inputs.frac=0.2
        if not os.path.exists(bet.inputs.out_file):
            print 'running',bet.cmdline
            bet.run()
    else:
        print 'using existing mean_lowb_brain'

        
    

if 1:
    bpx=create_bedpostx_pipeline("nipype_bedpostx")

    bpx.inputs.inputnode.dwi=ecdata
    bpx.inputs.inputnode.mask=mean_eclowb.replace('_brain','_brain_mask')
    bpx.inputs.inputnode.bvecs=ecdata.replace('.nii.gz','.bvec')
    bpx.inputs.inputnode.bvals=ecdata.replace('.nii.gz','.bval')
    bpx.inputs.xfibres.n_fibres=2
    bpx.inputs.xfibres.use_gpu=True

