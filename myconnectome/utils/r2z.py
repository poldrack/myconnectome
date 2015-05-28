"""
utils to convert between r and z values
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


