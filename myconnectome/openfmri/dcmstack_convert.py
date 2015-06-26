"""
convert myconnectome data to nifti
using dcmstack with embedded dicom header
"""

import os
import glob
import nibabel


dicomdir='/scratch/01329/poldrack/dicoms'
outdir='/scratch/01329/poldrack/selftracking/dcmstack'

dicomdirs=glob.glob(os.path.join(dicomdir,'s*'))
f=open('run_dcmstack.sh','w')

for d in dicomdirs:
    sc=os.path.basename(d).replace('-','_').split('_')[-1]
    try:
        sessnum=int(sc)
        sesscode='ses%03d'%sessnum
        print sesscode
    except:
        print 'skipping',sc
        continue
    if d.find('retinotopy')>0:
        sesscode='sesret'
        
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
