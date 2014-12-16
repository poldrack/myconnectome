"""
extract data from 333 washu space using aparc+aseg from freesurfer

"""

import os,nibabel,numpy,sys


datadir='/corral-repl/utexas/poldracklab/data/selftracking/laumann/FCPROCESS_SCRUBBED_meanfield_LSinterp_333_sub018_reg_FD025_mirpad'

outdir='/corral-repl/utexas/poldracklab/data/selftracking/aseg_data'


subcode=sys.argv[1]
datafile=os.path.join(datadir,'%s_333_zmdt_resid_ntrpl_bpss_zmdt.nii.gz'%subcode)
assert os.path.exists(datafile)

outfile=os.path.join(outdir,'%s_asegmean.txt'%subcode)

try:
    data.shape
except:
    dataimg=nibabel.load(datafile)
    data=dataimg.get_data()

aseg='/corral-repl/utexas/poldracklab/data/selftracking/freesurfer/mri/aparc+aseg_reg2wasu333.nii.gz'

try:
    asegdata
except:
    asegimg=nibabel.load(aseg)
    asegdata=asegimg.get_data()

f=open('/corral-repl/utexas/poldracklab/data/selftracking/code/aseg_fields.txt')
asegfields={}
for l in f.readlines():
    l_s=l.strip().split()
    asegfields[int(l_s[0])]=l_s[1]
f.close()

asegkeys=asegfields.keys()
asegkeys.sort()

roidata=numpy.zeros((data.shape[3],len(asegkeys)))

for k in range(len(asegkeys)):
    kvox=numpy.where(asegdata==asegkeys[k])
    for tp in range(data.shape[3]):
        tmp=data[:,:,:,tp]
        roidata[tp,k]=numpy.mean(tmp[kvox])
        
numpy.savetxt(outfile,roidata)
