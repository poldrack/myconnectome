# -*- coding: utf-8 -*-
"""
labels_to_gii - convert a set of labels across parcels into gii files

Created on Fri Apr 24 16:53:08 2015

@author: poldrack
"""

import nibabel.gifti.giftiio
import os
import numpy
import unittest



class MyTest(unittest.TestCase):
    def test_output(self):
        testdata=numpy.vstack((numpy.arange(1,621),numpy.ones(620))).T
        varnames=['A','B']
        lhimg,rhimg=labels_to_gii(testdata,varnames,None)
        lhparc,rhparc=load_parcellations()
        
        self.assertEqual(numpy.sum(lhparc.darrays[0].data - lhimg.darrays[0].data),0,'LH darrays do not match')
        self.assertEqual(numpy.sum(rhparc.darrays[0].data - rhimg.darrays[0].data),0,'RH darrays do not match')
        self.assertEqual(lhimg.darrays[0].meta.data[1].value,varnames[0])
        self.assertEqual(lhimg.darrays[1].meta.data[1].value,varnames[1])
        
def load_parcellations(lhparcfile,rhparcfile):
    lh=nibabel.gifti.giftiio.read(lhparcfile)
    rh=nibabel.gifti.giftiio.read(rhparcfile)
    return lh,rh
    
def labels_to_gii(datamat,varnames,filestem,basedir='./',outdir='./'):
    
    assert datamat.shape[0]==620
    try:
       assert len(datamat.shape)==2
    except:
        datamat=datamat[:,None]
        
    nvars=datamat.shape[1]
    lhparcfile=os.path.join(basedir,'parcellation/all_selected_L_new_parcel_renumbered.func.gii')
    rhparcfile=os.path.join(basedir,'parcellation/all_selected_R_new_parcel_renumbered.func.gii')

    lh,rh=load_parcellations(lhparcfile,rhparcfile)
        
    lh_labels=lh.darrays[0].data.copy()
    rh_labels=rh.darrays[0].data.copy()
    
    lhimg=nibabel.gifti.GiftiImage()
    rhimg=nibabel.gifti.GiftiImage()
    
    
    for j in range(nvars):
        darray_l=numpy.zeros(lh.darrays[0].data.shape,dtype=numpy.float32)
        for i in range(1,311):
            darray_l[lh_labels==i]=datamat[i-1,j]

        
        lhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_l,
            intent=lh.darrays[0].intent,datatype=lh.darrays[0].datatype,ordering='F',
            meta={'AnatomicalStructurePrimary':'CortexLeft','Name':varnames[j]}))

    for j in range(nvars):
        darray_r=numpy.zeros(rh.darrays[0].data.shape,dtype=numpy.float32)
        for i in range(311,621):
            darray_r[rh_labels==i]=datamat[i-1,j]

        
        rhimg.add_gifti_data_array(nibabel.gifti.GiftiDataArray.from_array(darray_r,
            intent=rh.darrays[0].intent,datatype=rh.darrays[0].datatype,ordering='F',
            meta={'AnatomicalStructurePrimary':'CortexRight','Name':varnames[j]}))
    
    if filestem:
        nibabel.gifti.giftiio.write(lhimg,os.path.join(outdir,'lh_%s.func.gii'%filestem))
        nibabel.gifti.giftiio.write(rhimg,os.path.join(outdir,'rh_%s.func.gii'%filestem))
    
    return lhimg,rhimg

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(MyTest)
    unittest.TextTestRunner(verbosity=2).run(suite)
    