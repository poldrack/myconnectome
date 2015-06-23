# -*- coding: utf-8 -*-
"""
compute task connnectome using MACM approach

Created on Sat Jun 20 11:18:48 2015

@author: poldrack
"""

import os
import numpy

basedir=os.environ['MYCONNECTOME_DIR']

taskdata=numpy.loadtxt(os.path.join(basedir,'taskfmri/zstat_parcel_data.txt'))

cc=numpy.corrcoef(taskdata.T)

numpy.savetxt(os.path.join(basedir,'taskfmri/task_connectome.txt'),cc)