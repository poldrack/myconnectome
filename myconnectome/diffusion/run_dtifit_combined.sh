BASEDIR='/corral-repl/utexas/poldracklab/data/selftracking/stanford_diffusion/combined_eddy_corrected'


dtifit -k $BASEDIR/all_pe1_unwarped_dwi_ec.nii.gz -o $BASEDIR/dtifit -m $BASEDIR/all_pe1_unwarped_dwi_ec_lowb_brain_mask.nii.gz -r $BASEDIR/all_pe1_unwarped_dwi_ec.bvec -b $BASEDIR/all_pe1_unwarped_dwi_ec.bval -w 