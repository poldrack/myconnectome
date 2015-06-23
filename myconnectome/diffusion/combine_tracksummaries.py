import numpy
import sys
import os

outdir = '/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/stanford_diffusion/combined_eddy_corrected'

summdir = '%s/tracksummary' %(outdir)

summdata=numpy.zeros((630,630))

for i in range(1,631):
    data=numpy.loadtxt(os.path.join(summdir,'roi%03d.txt'%i))
    summdata[:,i-1]=data
    if numpy.max(data)>=1:
        print i,numpy.max(data)

df = pandas.DataFrame(summdata)
outfile = '%s/tracksumm_distcorr.tsv'%(outdir)
df.to_csv(outfile,sep="\t")
print "Output matrix saved as %s" %(outfile)
#numpy.savetxt('%s/tracksumm_distcorr.txt'%(outdir),summdata)
