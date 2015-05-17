"""
run quality assurance measures on anatomical data
"""

import sys,glob
sys.path.append('/corral-repl/utexas/poldracklab/software_lonestar/build/quality-assessment-protocol')
import os

from qap import load_image, load_mask, summary_mask, cnr,efc,fber,fwhm,artifacts,snr

basedir='/corral-repl/utexas/poldracklab/data/selftracking/shared_dataset'
subcodes=glob.glob('/corral-repl/utexas/poldracklab/data/selftracking/freesurfer_sessions/sub*')
subcodes = [i.split('/')[-1] for i in subcodes if not i.find('.long')>0]

anatdata={'subcode':[],'mean_gm':[],'mean_wm':[],'std_bg':[],'anat_cnr':[],'anat_efc':[],'anat_fber':[],'anat_fwhm':[],'anat_qi1':[],'anat_snr':[]}
for subcode in subcodes:
	print 'processing',subcode
	anatdata['subcode'].append(subcode)
	anat_file                       = os.path.join(basedir,subcode,'anatomy/t1w_001.nii.gz')
	anat_mask_file  = os.path.join(basedir,subcode,'anatomy/t1w_001_bet_outskin_mask.nii.gz')
	anat_data                       = load_image(anat_file)
	
	gm_mask_file  = os.path.join(basedir,subcode,'anatomy/t1w_001_gray_mask.nii.gz')
	wm_mask_file  = os.path.join(basedir,subcode,'anatomy/t1w_001_white_mask.nii.gz')

	
	# Load the different masks
	anat_mask_data                       = load_mask(anat_mask_file, anat_file)

	bg_mask_data = 1 - anat_mask_data
	bg_mask_data[:,:,0:80]=0  # zero out regions at bottom that have artifact
	gm_mask_data = load_mask(gm_mask_file, anat_mask_file)
	wm_mask_data = load_mask(wm_mask_file, anat_mask_file)

	
	# Calculate mean grey-matter, mean white-matter 
	# and standard deviation air
	mean_gm,_,_	= summary_mask(anat_data, gm_mask_data)
	mean_wm,_,_	= summary_mask(anat_data, wm_mask_data)
	_,std_bg,_	= summary_mask(anat_data, bg_mask_data)
	
	# SNR
	anat_cnr 		= cnr(mean_gm, mean_wm, std_bg)
	anat_snr 		= snr(mean_gm, std_bg)

        anat_efc		= efc(anat_data)
        anat_fber 	= fber(anat_data, anat_mask_data)
        anat_fwhm 	= fwhm(anat_file, anat_mask_file, out_vox=False)
        anat_qi1		= artifacts(anat_data, anat_mask_data, calculate_qi2=False)


	anatdata['mean_gm'].append(mean_gm)
	anatdata['mean_wm'].append(mean_wm)
	anatdata['std_bg'].append(std_bg)
	anatdata['anat_cnr'].append(anat_cnr)
	anatdata['anat_snr'].append(anat_snr)
	anatdata['anat_efc'].append(anat_efc)
	anatdata['anat_fber'].append(anat_fber)
	anatdata['anat_fwhm'].append(anat_fwhm[3])
	anatdata['anat_qi1'].append(anat_qi1[0])
	
	

import pickle
pickle.dump(anatdata,open('/corral-repl/utexas/poldracklab/data/selftracking/shared_dataset/anat_qa.pkl','wb'))
