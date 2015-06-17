"""
set up behavioral files for task001 - working memory
"""

import os,glob
import numpy

basedir=os.environ['MYCONNNECTOME_DIR']
datadir=os.path.join(basedir,'task_behavior/task001')
origfilesdir=os.path.join(datadir,'origfiles')

origfiles=glob.glob(os.path.join(origfilesdir,'*pkl'))

origfiles.sort()

