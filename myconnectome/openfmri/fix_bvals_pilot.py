# fix b values that were incorrectly copied

import os,sys,glob,shutil
import numpy
import nibabel
import nilearn.input_data

bidsdir='/corral-repl/utexas/poldracklab/data/selftracking/BIDS-1.0/ds031/sub-01'
basedir='/corral-repl/utexas/poldracklab/data/selftracking/diffusion_dicoms'

diffiles=glob.glob(os.path.join(bidsdir,'ses-0*/dwi/sub-01_ses-*_run-*_dwi.nii.gz'))

diffiles.sort()


for f in diffiles:
    sescode=f.split('/')[9]
    subcode=sescode.replace('ses-','sub')
    runcode=int(os.path.basename(f).split('_')[2].replace('run-',''))
    print sescode,runcode
    infile_bval=os.path.join(basedir,'%s_%d.bval'%(sescode,runcode))
    try:
        assert os.path.exists(infile_bval)
    except:
        print 'missing bval for',subcode
        continue
    infile_bvec=os.path.join(basedir,'%s_%d.bvec'%(sescode,runcode))
    try:
        assert os.path.exists(infile_bval)
    except:
        print 'missing bvec for',subcode
        continue
    bval=numpy.loadtxt(infile_bval)

    bvec=numpy.loadtxt(infile_bvec)

    mapper=nilearn.input_data.NiftiMasker()
    d=mapper.fit_transform(nibabel.load(f))
    meandif=numpy.mean(d,1)
    assert numpy.corrcoef(meandif,bval)[0,1]<-0.75
    print numpy.corrcoef(meandif,bval)[0,1]
    out_bval=f.replace('.nii.gz','.bval')
    out_bvec=f.replace('.nii.gz','.bvec')
    shutil.copy(infile_bval,out_bval)
    shutil.copy(infile_bvec,out_bvec)
    
