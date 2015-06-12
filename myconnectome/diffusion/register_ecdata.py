"""
make low-b images
register them to T1
make inverse warps
warp parcellation to dti space for each 


"""

import os,sys,shutil
import glob
import numpy

import nipype.interfaces.fsl as fsl
import nibabel as nib



basedir=os.path.abspath('/corral-repl/utexas/poldracklab/data/selftracking')


fsdir='/corral-repl/utexas/poldracklab/data/selftracking/FREESURFER_fs_LR/7112b_fs_LR'
anatfile=os.path.join(fsdir,'sub013_mpr1_on_TRIO_Y_NDC_111.nii.gz')
anatfile_brain=os.path.join(fsdir,'sub013_mpr1_on_TRIO_Y_NDC_111_brain.nii.gz')
wmsegfile=anatfile_brain.replace('.nii.gz','_wmseg.nii.gz')

if not os.path.exists(wmsegfile):
    print 'segmenting anat file'
    fast=fsl.FAST()
    fast.inputs.in_files=anatfile_brain
    fast.run()
    os.rename(anatfile_brain.replace('.nii.gz','_pve_2.nii.gz'),anatfile_brain.replace('.nii.gz','_wmseg.nii.gz'))

if 1:
    ecdata=os.path.join(basedir,'stanford_diffusion/combined_eddy_corrected/all_pe1_unwarped_dwi_ec.nii.gz')

    ecpath=os.path.basename(ecdata)
    mean_eclowb=ecdata.replace('_ec.nii.gz','_ec_lowb.nii.gz')

    if not os.path.exists(mean_eclowb):
        print 'making mean lowb'
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

    # register to 1mm anatomy

    flirt=fsl.FLIRT()
    flirt.inputs.in_file=mean_eclowb
    flirt.inputs.out_matrix_file=mean_eclowb.replace(".nii.gz","_reg2t1.mat")
    flirt.inputs.reference=anatfile_brain
    flirt.inputs.wm_seg=anatfile_brain.replace('.nii.gz','_wmseg.nii.gz')
    flirt.inputs.cost_func='bbr'
    flirt.inputs.verbose=9
    flirt.inputs.out_file=mean_eclowb.replace(".nii.gz","_reg2t1.nii.gz")
    if not os.path.exists(flirt.inputs.out_matrix_file):
        flirt.run()
        
