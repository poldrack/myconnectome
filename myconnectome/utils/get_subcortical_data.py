"""
extract data from 333 washu space using aparc+aseg from freesurfer

"""

import os,nibabel,numpy,sys



def get_subcortical_data(datafile,basedir='/corral-repl/utexas/poldracklab/data/selftracking'):    
    dataimg=nibabel.load(datafile)
    
    data=dataimg.get_data()
    
    aseg=os.path.join(basedir,'freesurfer/mri/aparc+aseg_reg2wasu333.nii.gz')
    
    asegimg=nibabel.load(aseg)
    asegdata=asegimg.get_data()
    
    f=open(os.path.join(basedir,'aseg/aseg_fields.txt'))
    asegfields={}
    for l in f.readlines():
        l_s=l.strip().split()
        asegfields[int(l_s[0])]=l_s[1]
    f.close()
    
    asegkeys=asegfields.keys()
    asegkeys.sort()
    if len(data.shape)==3:
        ntp=1
    else:
        ntp=data.shape[3]
    roidata=numpy.zeros((ntp,len(asegkeys)))
    
    for k in range(len(asegkeys)):
        kvox=numpy.where(asegdata==asegkeys[k])
        for tp in range(ntp):
            tmp=data[:,:,:,tp]
            roidata[tp,k]=numpy.mean(tmp[kvox])
            
    return roidata
