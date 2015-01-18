"""
run quality assurance measures on functional data
"""

import sys,glob
sys.path.append('/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/qatest/quality-assessment-protocol')
import os
import numpy
from run_shell_cmd import run_shell_cmd
from compute_fd import compute_fd

from qap import load_func,load_image, load_mask, summary_mask, cnr,efc,fber,fwhm,artifacts,ghost_all,calc_mean_func,calc_dvars,mean_outlier_timepoints,mean_quality_timepoints,snr,temporal_qc
from qap.temporal_qc import summarize_fd

basedir='/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI'

#funcfiles=glob.glob(os.path.join(basedir,'sub*/BOLD/resting_run001/bold.nii.gz'))
#funcfiles.sort()

funcdata={'subcode':[],'func_efc':[],'func_fber':[],'func_fwhm':[],'func_gsr':[],'func_dvars':[],'func_outlier':[],'func_quality':[],'func_mean_fd':[],'func_num_fd':[],'func_perc_fd':[]}
	  
#for funcfile in funcfiles:
try:
	subcode=sys.argv[1]
	assert os.path.exists(os.path.join(basedir,subcode,'BOLD/resting_run001/bold.nii.gz'))
except:
	subcode='sub004'
	print 'using default...'
	
func_file=os.path.join(basedir,subcode,'BOLD/resting_run001/bold.nii.gz')
if 1:
	#subcode=func_file.split('/')[8]
	print 'processing',subcode
	funcdata['subcode'].append(subcode)
	mask_file=func_file.replace('.nii.gz','_brain_mask.nii.gz')
	if not os.path.exists(mask_file):
		cmd='bet %s %s -m -F'%(func_file,func_file.replace('.nii.gz','_brain'))
		print cmd
		run_shell_cmd(cmd)
	
	func_data                       = load_func(func_file,mask_file)
	mean_func_data 		= calc_mean_func(func_file)
	func_mask = load_mask(mask_file)
	bg_mask=1 - func_mask
	mean_inmask,_,_=summary_mask(mean_func_data,func_mask)
	_,std_bg,_=summary_mask(mean_func_data,bg_mask)
	func_snr=snr(mean_inmask,std_bg)
        func_efc		= efc(func_data)
        func_fber 	= fber(mean_func_data, func_mask)
	meanfile=func_file.replace('bold','bold_mcf_mean_reg')
	assert os.path.exists(meanfile)
        func_fwhm 	= fwhm(meanfile, mask_file, out_vox=True)

	print 'running ghost_all'
	_,func_gsr,_=ghost_all(mean_func_data,func_mask)
	print 'running calc_dvars'
	try:
		func_dvars	= calc_dvars(func_data, output_all=False)
	except:
		func_dvars=[]
	print 'running mean_outlier_timepoints'
	func_outlier	= mean_outlier_timepoints(func_file, mask_file, out_fraction=True)
	print 'running mean_quality_timepoints'
	func_quality	= mean_quality_timepoints(func_file, automask=True)
	
	print 'running summarize_fd'

	if not os.path.exists(func_file.replace('bold.nii.gz','bold.out.aff12.1D')):
		cmd='3dvolreg -prefix NULL -1Dmatrix_save %s/%s/BOLD/resting_run001/bold.out %s'%(basedir,subcode,func_file)
		print 'running',cmd
		run_shell_cmd(cmd)
	mean_fd,num_fd,perc_fd=summarize_fd(func_file.replace('bold.nii.gz','bold.out.aff12.1D'),threshold=0.2)
	funcdata={'subcode':subcode,'snr':func_snr,'efc':func_efc,'fber':func_fber,'fwhm':func_fwhm,'gsr':func_gsr,'dvars':func_dvars,'outlier':func_outlier,'fd':mean_fd,'num_fd':num_fd,'func_quality':func_quality}
	
	import pickle
	pickle.dump(funcdata,open('/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/qatest/qadata/%s_func_qa.pkl'%subcode,'wb'))
	

