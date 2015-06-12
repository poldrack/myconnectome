#!/bin/bash

BASEDIR=/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/stanford_diffusion/combined_eddy_corrected

cp ${BASEDIR}/all_pe1_unwarped_dwi_ec.nii.gz  ${BASEDIR}/bedpostx_combined/data.nii.gz
cp ${BASEDIR}/all_pe1_unwarped_dwi_ec_lowb_brain_mask.nii.gz ${BASEDIR}/bedpostx_combined/nodif_brain_mask.nii.gz
cp ${BASEDIR}/all_pe1_unwarped_dwi_ec.bval ${BASEDIR}/bedpostx_combined/bvals
cp ${BASEDIR}/all_pe1_unwarped_dwi_ec.bvec ${BASEDIR}/bedpostx_combined/bvecs




