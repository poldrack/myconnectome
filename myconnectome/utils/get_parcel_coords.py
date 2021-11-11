"""
load parcel data and get coordinates
"""


from __future__ import absolute_import
import os
import numpy
from myconnectome.utils.load_parcel_data import load_parcel_data
from six.moves import range

basedir=os.environ['MYCONNECTOME_DIR']

def get_parcel_coords():
    parceldata=load_parcel_data(os.path.join(basedir,'parcellation/parcel_data.txt'))
    coords=numpy.zeros((len(parceldata),3))
    for i in range(len(parceldata)):
        p=parceldata[i+1]
        coords[i,:]=[p['x'],p['y'],p['z']]
    return coords
    