"""
make mean corr data and variance adjmtx
for use in visualization and loading into R
"""

import numpy

def r_to_z(r):
    # fisher transform
    z=0.5*numpy.log((1.0+r)/(1.0-r))
    z[numpy.where(numpy.isinf(z))]=0
    z[numpy.where(numpy.isnan(z))]=0

    return z

def z_to_r(z):
    # inverse transform
    return (numpy.exp(2.0*z) - 1)/(numpy.exp(2.0*z) + 1)


try:
    data
except:
    data=numpy.load('/Users/poldrack/Dropbox/data/selftracking/rsfmri/corrdata.npy')
    
data_z=r_to_z(data)
meancorr_z=numpy.mean(data,0)
varcorr_z=numpy.var(data,0)
meancorr=z_to_r(meancorr_z)

numpy.savetxt('/Users/poldrack/Dropbox/data/selftracking/rsfmri/mean_corrdata.txt', meancorr)

fulldata=numpy.zeros((634,634))
fulldata[numpy.triu_indices(634,1)]=meancorr
numpy.savetxt('/Users/poldrack/Dropbox/data/selftracking/rsfmri/behav_adjmtx/mean_adjmtx.txt', fulldata)

fulldata=numpy.zeros((634,634))
fulldata[numpy.triu_indices(634,1)]=varcorr_z
numpy.savetxt('/Users/poldrack/Dropbox/data/selftracking/rsfmri/behav_adjmtx/var_adjmtx.txt', fulldata)
