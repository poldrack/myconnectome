"""
load results from ptx and summarize
connectivity across all ROIs
"""

import os,sys
import numpy
import nibabel

try:
    roinum=int(sys.argv[1])
except:
    roinum=13

distcorr=True

if distcorr:
    dc=''
else:
    dc='no'

roidir='/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/DTI/probtrackx_outputs_%sdistcorr_term/probtrackx_%sdistcorr_roi%03d'%(dc,dc,roinum)
seeddir='/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/DTI/parcels_dtispace'

seedsizes=[int(i.strip()) for i in open('seedsizes').readlines()]
nsamp=numpy.zeros(634)

if roinum<311:
        seedhemis='L'
elif roinum>620:
    seedhemis='S'
else:
        seedhemis='R'

waytotal=int(open(os.path.join(roidir,'waytotal')).readline().strip())


if waytotal>0:
  for i in range(1,635):
    targdir='/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/DTI/probtrackx_outputs_%sdistcorr/probtrackx_%sdistcorr_roi%03d'%(dc,dc,i)
    waytotal_targ=int(open(os.path.join(targdir,'waytotal')).readline().strip())
    if waytotal_targ==0:
        continue
    if i<311:
        hemis='L'
    elif i>620:
        hemis='S'
    else:
        hemis='R'
    if i==roinum:
        continue

    img=nibabel.load(os.path.join(roidir,'seeds_to_parcels.%s.bin.clean.%03d.nii.gz'%(hemis,i))).get_data()
    nsamp[i-1]=numpy.sum(img)/float((waytotal*seedsizes[i-1]))
    
                                  
numpy.savetxt('tracksummary/roi%03d.txt'%roinum,nsamp)
