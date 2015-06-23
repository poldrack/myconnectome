

import os,glob
import numpy

basedir='/scratch/projects/UT/poldracklab/poldrack/selftracking/myconnectome/rsfmri/quic'

utr=numpy.triu_indices(630,1)

densities=['0.005','0.01','0.025','0.05','0.075']

for d in densities:

    datadir=os.path.join(basedir,'quic_precision_%s'%d)
    dfiles=glob.glob(os.path.join(datadir,'*.txt'))
    dfiles.sort()
    alldata=numpy.zeros((len(dfiles),utr[0].shape[0]))

    for i in range(len(dfiles)):
        data=numpy.loadtxt(dfiles[i])
        alldata[i,:]=data[utr]
    numpy.save(os.path.join(basedir,'quic_utr_data_%s.npy'%d),alldata)
        
