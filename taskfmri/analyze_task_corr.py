import os,glob
import nibabel
import numpy
from openfmri_utils import *
import matplotlib.pyplot as plt

basedir='/corral-repl/utexas/poldracklab/data/selftracking/analyses/task_data'

data=numpy.load(os.path.join(basedir,'task_contrast_data.npy'))
task=numpy.loadtxt(os.path.join(basedir,'tasknum.txt'))
cope=numpy.loadtxt(os.path.join(basedir,'copenum.txt'))
subs=numpy.loadtxt(os.path.join(basedir,'sessnum.txt'))

task_cope=numpy.vstack((task,cope)).T

idx=numpy.lexsort((cope,task))
task_cope_ordered=task_cope[idx,:]

data_ordered=data[idx,:]

cc=numpy.corrcoef(data_ordered)
plt.imshow(cc,cmap='gray')
plt.show()
