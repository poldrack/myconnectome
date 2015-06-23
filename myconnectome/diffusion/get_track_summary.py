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
	roinum=1
#dirname=sys.argv[2]

basedir='/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/stanford_diffusion/combined_eddy_corrected'

roidir=os.path.join(basedir,'probtrackx_outputs_distcorr_term/probtrackx_distcorr_roi%03d'%roinum)

seeddir=basedir

tracksummary=os.path.join(basedir,'tracksummary')
if not os.path.exists(tracksummary):
	os.mkdir(tracksummary)

seedsizes=[int(i.strip()) for i in open('%s/seedsizes' %seeddir).readlines()]
nsamp=numpy.zeros(630)

waytotal=int(open(os.path.join(roidir,'waytotal')).readline().strip())


if waytotal>0:
  for i in range(1,631):
    targdir=os.path.join(basedir,'probtrackx_outputs_distcorr_term/probtrackx_distcorr_roi%03d'%i)
    waytotal_targ=int(open(os.path.join(targdir,'waytotal')).readline().strip())
    if waytotal_targ==0:
        continue
    if i==roinum:
        continue
    img = nibabel.load(os.path.join(roidir,'seeds_to_parcel%03d.nii.gz'%(i))).get_data()
    nsamp[i-1]=numpy.sum(img)/float((waytotal*seedsizes[i-1]))
                                  
numpy.savetxt('%s/roi%03d.txt'%(tracksummary,roinum),nsamp)
