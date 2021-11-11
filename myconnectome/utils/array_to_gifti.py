"""
write array over vertices to gifti file
"""

from __future__ import absolute_import
import nibabel.gifti.giftiio
import numpy
import os
from myconnectome.utils.set_structure import set_structure
from six.moves import range
nvert=32492


def array_to_gifti_32k(data,outfilestem,names=None,datatype=16,intent=11,ordering='F'):
    if len(data.shape)==1:
        data=data[None,:]
        
    assert data.shape[1]==nvert*2
    try:
        names
    except:
        names=['image%04d'%i for i in range(data.shape[0])]
    
    lh=nibabel.gifti.GiftiImage()
    rh=nibabel.gifti.GiftiImage()
    
    for i in range(data.shape[0]):
        darray_lh=data[i,:nvert].astype(numpy.float32)
        lh.add_gifti_data_array(
                nibabel.gifti.GiftiDataArray.from_array(darray_lh,
                intent=11,
                datatype=16,
                ordering='F',
                meta={'AnatomicalStructurePrimary':'CortexLeft',
                'Name':names[i]}))
            
        darray_rh=data[i,nvert:].astype(numpy.float32)
        rh.add_gifti_data_array(
                nibabel.gifti.GiftiDataArray.from_array(darray_rh,
                intent=11,
                datatype=16,
                ordering='F',
                meta={'AnatomicalStructurePrimary':'CortexRight',
                'Name':names[i]}))
    nibabel.gifti.giftiio.write(lh,'%s.LH.func.gii'%outfilestem)
    set_structure('%s.LH.func.gii'%outfilestem,'CORTEX_LEFT')
    nibabel.gifti.giftiio.write(rh,'%s.RH.func.gii'%outfilestem)
    set_structure('%s.RH.func.gii'%outfilestem,'CORTEX_RIGHT')

    