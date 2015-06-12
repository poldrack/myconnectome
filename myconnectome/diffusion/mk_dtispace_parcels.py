"""
use inverse warp from nodif to T1 to warp parcels
into diffusion space
- then separate out into a set of individual parcel images
"""

import os,sys
import numpy
import nibabel
import nipype.interfaces.fsl as fsl

parcelfile='/corral-repl/utexas/poldracklab/data/selftracking/parcellation/84sub_all_startpos50_parcels_TRIO_111.nii.gz'

dti2t1_mat='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/combined_eddy_corrected/all_pe1_unwarped_dwi_ec_lowb_reg2t1.mat'

invmat='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/combined_eddy_corrected/all_pe1_unwarped_dwi_ec_lowb_regt12dif.mat'

if not os.path.exists(invmat):
    print 'creating inverse warp'
    invt=fsl.ConvertXFM()
    invt.inputs.in_file=dti2t1_mat
    invt.inputs.out_file=invmat
    invt.inputs.invert_xfm=True
    invt.run()

warped_parcels='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/combined_eddy_corrected/parcels_dtispace.nii.gz'

if not os.path.exists(warped_parcels):
    print 'created warped parcels'
    flirt=fsl.FLIRT()
    flirt.inputs.in_file=parcelfile
    flirt.inputs.out_file=warped_parcels
    flirt.inputs.reference='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/combined_eddy_corrected/all_pe1_unwarped_dwi_ec_lowb_brain.nii.gz'

    flirt.inputs.in_matrix_file=invmat
    flirt.inputs.interp='nearestneighbour'
    flirt.inputs.apply_xfm=True
    flirt.run()

warped_subcortical_parcels='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/combined_eddy_corrected/parcels_subcortical_dtispace.nii.gz'

if not os.path.exists(warped_subcortical_parcels):
    print 'created warped subcortical parcels'
    flirt=fsl.FLIRT()
    flirt.inputs.in_file='/corral-repl/utexas/poldracklab/data/selftracking/freesurfer/mri/aparc+aseg_reg2wasu111.nii.gz'
    flirt.inputs.out_file=warped_subcortical_parcels
    flirt.inputs.reference='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/combined_eddy_corrected/all_pe1_unwarped_dwi_ec_lowb_brain.nii.gz'

    flirt.inputs.in_matrix_file=invmat
    flirt.inputs.interp='nearestneighbour'
    flirt.inputs.apply_xfm=True
    flirt.run()

wmdti='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/combined_eddy_corrected/wm_dtimask'
if not os.path.exists(wmdti):
    print 'making wm_dtimask'
    flirt=fsl.FLIRT()
    flirt.inputs.in_file='/corral-repl/utexas/poldracklab/data/selftracking/freesurfer/mri/aparc+aseg_reg2wasu111.nii.gz'
    flirt.inputs.out_file=warped_subcortical_parcels
    flirt.inputs.reference='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/combined_eddy_corrected/all_pe1_unwarped_dwi_ec_lowb_brain.nii.gz'

    flirt.inputs.in_matrix_file=invmat
    flirt.inputs.interp='nearestneighbour'
    flirt.inputs.apply_xfm=True
    flirt.run()
    
# make separate parcel and termination masks

combined_parcels='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/combined_eddy_corrected/parcels_combined_dtispace.nii.gz'

if not os.path.exists(combined_parcels):
    parcelimg=nibabel.load(warped_parcels)
    parceldata=parcelimg.get_data()

    parceldata[parceldata>616]=0

    asegimg=nibabel.load(warped_subcortical_parcels)
    asegdata=asegimg.get_data()

    f=open('/corral-repl/utexas/poldracklab/data/selftracking/aseg/aseg_fields.txt')
    asegfields={}
    for l in f.readlines():
        l_s=l.strip().split()
        asegfields[int(l_s[0])]=l_s[1]
    f.close()


    asegkeys=asegfields.keys()
    asegkeys.sort()

    for i in range(len(asegkeys)):
        parceldata[numpy.where(asegdata==asegkeys[i])]=i+617

    newimg=nibabel.Nifti1Image(parceldata,affine=asegimg.get_affine())
    newimg.to_filename(combined_parcels)
    
else:
    parcelimg=nibabel.load(combined_parcels)
    parceldata=parcelimg.get_data()

seed_dir='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/combined_eddy_corrected/seed_masks'
term_dir='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/combined_eddy_corrected/termination_masks'

for i in numpy.unique(parceldata):
    if i==0:
        continue
    outfile=os.path.join(seed_dir,'parcel%03d.nii.gz'%i)
    tmp=(parceldata==i).astype('float32')
    newimg=nibabel.Nifti1Image(tmp,affine=parcelimg.get_affine())
    newimg.to_filename(outfile)
    
    outfile=os.path.join(term_dir,'parcel%03d.nii.gz'%i)
    tmp=(parceldata>0).astype('float32')
    tmp[parceldata==i]=0
    newimg=nibabel.Nifti1Image(tmp,affine=parcelimg.get_affine())
    newimg.to_filename(outfile)
    
 
                     
