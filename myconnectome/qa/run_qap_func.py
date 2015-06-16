"""
run quality assurance measures on functional data
"""

import sys,glob
sys.path.append('/corral-repl/utexas/poldracklab/software_lonestar/quality-assessment-protocol')
import os
import numpy
from run_shell_cmd import run_shell_cmd
from compute_fd import compute_fd

from qap import load_func,load_image, load_mask, summary_mask, cnr,efc,fber,fwhm,artifacts,ghost_all,calc_mean_func,calc_dvars,mean_outlier_timepoints,mean_quality_timepoints

basedir='/corral-repl/utexas/poldracklab/data/selftracking/shared_dataset'
funcfiles=glob.glob(os.path.join(basedir,'sub*/BOLD/resting_run001/bold.nii.gz'))

funcdata={'subcode':[],'func_efc':[],'func_fber':[],'func_fwhm':[],'func_gsr':[],'func_dvars':[],'func_outlier':[],'func_quality':[],'func_mean_fd':[],'func_num_fd':[],'func_perc_fd':[]}
	  
#for funcfile in funcfiles:
func_file=funcfiles[0]
if 1:
	subcode=func_file.split('/')[7]
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

        func_efc		= efc(func_data)
        #func_fber 	= fber(func_data, func_mask)
        #func_fwhm 	= fwhm(func_file, mask_file, out_vox=False)

	print 'running ghost_all'
	_,func_gsr,_=ghost_all(mean_func_data,func_mask)
	print 'running calc_dvars'
	func_dvars	= calc_dvars(func_data, output_all=False)
	print 'running mean_outlier_timepoints'
	func_outlier	= mean_outlier_timepoints(func_file, mask_file, out_fraction=True)
	print 'running compute_fd'
	motpars=numpy.loadtxt(func_file.replace('.nii.gz','_mcf.par'))
	fd=compute_fd(motpars)
	sdf
	
	funcdata['mean_gm'].append(mean_gm)
	funcdata['mean_wm'].append(mean_wm)
	funcdata['std_bg'].append(std_bg)
	funcdata['anat_efc'].append(anat_efc)
	funcdata['anat_fber'].append(anat_fber)
	funcdata['anat_fwhm'].append(anat_fwhm)
	funcdata['anat_qi1'].append(anat_qi1)
	
	

