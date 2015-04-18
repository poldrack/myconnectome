# -*- coding: utf-8 -*-
"""
Object analysis for myconnectome - 
- first, find maximal response for each voxel
Created on Sat Apr 18 16:26:43 2015

@author: poldrack
"""

import nibabel.gifti.giftiio
import numpy
import os


datadir='/Users/poldrack/data/selftracking/surface_stats_333'
hems=['L','R']
data={}
for h in hems:
    datafile=os.path.join(datadir,'stats.%s.func.gii'%h)
    data[h]=nibabel.gifti.giftiio.read(datafile)
    