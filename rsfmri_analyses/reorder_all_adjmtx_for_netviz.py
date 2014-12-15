"""
reorder all of the data for visualization using vanessa's tool
"""

import glob,os
from reorder_adjmtx_by_network import *

inputdir='/Users/poldrack/Dropbox/data/selftracking/rsfmri/behav_adjmtx'
outputdir='/Users/poldrack/code/myconnectome-d3/data'

infiles=glob.glob(os.path.join(inputdir,'*txt'))

for i in infiles:
    reorder_adjmtx_by_network(i,os.path.join(outputdir,os.path.basename(i).replace('_adjmtx.txt','')))
    