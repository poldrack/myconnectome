import os,glob
import nibabel
import numpy
from openfmri_utils import *

basedir='/corral-repl/utexas/poldracklab/data/selftracking/'
outdir='/corral-repl/utexas/poldracklab/data/selftracking/analyses/task_data'

try:
    confiles
except:
    confiles=[i for i in glob.glob(os.path.join(basedir,'sub*/model/model*/task*.feat/design.con')) if i.find('_333')>0]

for c in confiles:
    con=load_fsl_design_con(c)
    
