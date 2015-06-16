
import numpy
import os



summdir='/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/DTI/tracksummary'

summdata=numpy.zeros((634,634))

for i in range(1,635):
    data=numpy.loadtxt(os.path.join(summdir,'roi%03d.txt'%i))
    summdata[:,i-1]=data
    if numpy.max(data)>=1:
        print i,numpy.max(data)

numpy.savetxt('tracksumm_distcorr.txt',summdata)
