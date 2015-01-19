# -*- coding: utf-8 -*-
"""
assemble qa data for myconnectome data paper
"""

import os,glob
import pickle
import pandas as pd
import numpy

qadatadir='/Users/poldrack/Dropbox/data/selftracking/QA'


# process anat data

if 0:
    anatdatafile=os.path.join(qadatadir,'anat_qa.pkl')
    
    anatdata=pickle.load(open(anatdatafile,'rb'))
    anatdata['anat_fwhm']
    
    subcode=anatdata.pop('subcode')
    s=pd.DataFrame(anatdata)
    
    corr_anat=pd.read_csv('/Users/poldrack/code/myconnectome/quality_assurance/corr_anat.csv')
    
    
    asdf

# process func data

funcdata={}

corr_func=pd.read_csv('/Users/poldrack/code/myconnectome/quality_assurance/corr_func.csv')

funcfiles=glob.glob(os.path.join(qadatadir,'rsfmri/*pkl'))

funcfiles.sort()

# from http://preprocessed-connectomes-project.github.io/quality-assessment-protocol/index.html

#Entopy Focus Criterion [func_efc]: SUses the Shannon entropy of voxel intensities as an indication of ghosting and blurring induced by head motion, lower is better 2. Uses mean functional.
#Foreground to Background Energy Ratio [func_fber]: Mean energy of image values (i.e., mean of squares) within the head relative to outside the head, higher values are better. Uses mean functional.
#Smoothness of Voxels [func_fwhm]: The full-width half maximum (FWHM) of the spatial distribution of the image intensity values in units of voxels, lower values are better. Uses mean functional.
#Ghost to Signal Ratio (GSR) [func_gsr]: A measure of the mean signal in the ‘ghost’ image (signal present outside the brain due to acquisition in the phase encoding direction) relative to mean signal within the brain, lower values are better. Uses mean functional.
#
#Standardized DVARS [func_dvars]: The spatial standard deviation of the temporal derivative of the data, normalized by the temporal standard deviation and temporal autocorrelation, lower values are better 56. Uses functional time-series.
#Outlier Detection [func_outlier]: The mean fraction of outliers found in each volume using 3dTout command in AFNI (http://afni.nimh.nih.gov/afni), lower values are better 7. Uses functional time-series.
#Median Distance Index [func_quality]: The mean distance (1 – spearman’s rho) between each time-point’s volume and the median volume using AFNI’s 3dTqual command (http://afni.nimh.nih.gov/afni), lower values are better 7. Uses functional time-series.
#Mean Fractional Displacement - Jenkinson [func_mean_fd]: A measure of subject head motion, which compares the motion between the current and previous volumes. This is calculated by summing the absolute value of displacement changes in the x, y and z directions and rotational changes about those three axes. The rotational changes are given distance values based on the changes across the surface of a 80mm radius sphere, lower values are better 89. Uses functional time-series.
#Number of volumes with FD greater than 0.2mm [func_num_fd]: Lower values are better Uses functional time-series.
#Percent of volumes with FD greater than 0.2mm [func_perc_fd]: Lower values are better Uses functional time-series.
#

gsr=[]
fber=[]
snr=[]
efc=[]
fwhm=[]
mean_fd=[]
pct_fd=[]
num_fd=[]
quality=[]

exclude_bad_subs=False

subcodes=[i.strip() for i in open('/Users/poldrack/code/myconnectome/rsfmri_analyses/subcodes.txt').readlines()]

for f in funcfiles:
    subcode=f.split('/')[-1].split('_')[0]
    if exclude_bad_subs and not subcode in subcodes:
        continue
    funcdata[subcode]=pickle.load(open(f,'rb'))
    gsr.append(funcdata[subcode]['gsr'])
    fber.append(funcdata[subcode]['fber'])
    snr.append(funcdata[subcode]['snr'])
    fwhm.append(funcdata[subcode]['fwhm'][3])
    efc.append(funcdata[subcode]['efc'])
    quality.append(funcdata[subcode]['func_quality'])
    mean_fd.append(funcdata[subcode]['fd'])
    pct_fd.append(100.0*(funcdata[subcode]['num_fd']/518.0))
    
funcvars={'func_gsr':gsr,'func_fber':fber,'func_snr':snr,'func_fwhm':fwhm,'func_efc':efc,'func_mean_fd':mean_fd,'func_perc_fd':pct_fd,'func_quality':quality}
myc=pd.DataFrame(funcvars)

if exclude_bad_subs:
    myc.to_csv('myconnectome_func_qa_goodsubs.csv')
else:
    myc.to_csv('myconnectome_func_qa_allsubs.csv')



