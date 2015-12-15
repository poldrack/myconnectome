"""
convert myconnectome data to nifti
using dcmstack with embedded dicom header
"""

import os
import glob
import nibabel

import dicom
import numpy as np

def slice_timing_and_multiband(dcm_file):
    dcmobj = dicom.read_file(dcm_file)
    if ("0019", "1029") in dcmobj:
        slice_timing = dcmobj[("0019", "1029")].value
        slice_timing = np.around(np.array(slice_timing)/1000.0, 3).tolist()
        zero_slices_count = (np.array(slice_timing) == 0).sum()
        if zero_slices_count > 1:
            return slice_timing, zero_slices_count
        else:
            return slice_timing, None
    else:
        return None, None


dicomdir='/corral-repl/utexas/poldracklab/data/selftracking/dicom'
outdir='/scratch/01329/poldrack/selftracking/dcmstack'

dicomdirs=glob.glob(os.path.join(dicomdir,'s*'))
f=open('run_dcmstack.sh','w')

slicetiming = {}

for d in dicomdirs:
    sc=os.path.basename(d).replace('-','_').split('_')[-1]
 
    try:
        sessnum=int(sc)
        sesscode='ses%03d'%sessnum
        bidscode='ses-%03d'%sessnum
        print sesscode
    except:
        print 'skipping',sc
        continue
    if d.find('retinotopy')>0:
        sesscode='sesret'
    slicetiming[bidscode]={}
        
    sessdir=os.path.join(outdir,sesscode)
    if not os.path.exists(sessdir):
        os.mkdir(sessdir)

    
    subdicomdirs=glob.glob(os.path.join(d,'SCANS/*'))
    for sd in subdicomdirs:
        seriesnum=int(os.path.basename(sd))
        sdd=os.path.join(sd,'DICOM')
        dicomfiles=glob.glob(os.path.join(sdd,'*.dcm'))
        if len(dicomfiles)==0:
            continue
        try:
            slicetiming[bidscode][seriesnum]=slice_timing_and_multiband(dicomfiles[0])
        except:
            pass
        cmd='dcmstack --embed-meta --dest-dir %s %s'%(sessdir,sdd)
        #print cmd
        niifiles=glob.glob(os.path.join(sessdir,'%03d-*nii.gz'%seriesnum))
        runcmd=True

        if len(niifiles)>1:
            print 'somethign wrong here, too many nii files:',niifiles
            runcmd=False

        elif len(niifiles)==1:
            try:
                nii=nibabel.load(niifiles[0])
            except:
                print 'problem opening', niifiles[0]
                nii=None
            if nii:
                shp=nii.get_shape()
                if len(shp)==3:
                    ntp=1
                else:
                    ntp=nii.get_shape()[3]
                if not len(dicomfiles)==ntp:
                    print 'shape mismatch',sd
                    runcmd=True
                else:
                    runcmd=False
        if runcmd:
            f.write(cmd+'\n')
        else:
            print 'EXISTS:',niifiles[0]

f.close()

import pickle
pickle.dump(slicetiming,open('/corral-repl/utexas/poldracklab/data/selftracking/slicetiming.pkl','wb'))
