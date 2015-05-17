"""
combine module data into single files
"""

import os,sys
import numpy

basedir=os.environ['MYCONNECTOME_DIR']

def collapse_module_data():
    outdir_bwmod=os.path.join(basedir,'analyses/rsfmri_analyses/bwmod_corr_data')
    outdir_winmod=os.path.join(basedir,'analyses/rsfmri_analyses/winmod_corr_data')
    
    
    subcodes=[i.strip() for i in open(os.path.join(basedir,'subcodes.txt')).readlines()]
    
    mmc_win=numpy.zeros((len(subcodes),12))
    mmc_bw=numpy.zeros((len(subcodes),66))
    
    
    subctr=0
    for subcode in subcodes:
        mmc_win[subctr,:]=numpy.loadtxt(os.path.join(outdir_winmod,subcode+'.txt'))
        mmc_bw[subctr,:]=numpy.loadtxt(os.path.join(outdir_bwmod,subcode+'.txt'))
        subctr+=1
    
    numpy.savetxt(os.path.join(basedir,'analyses/rsfmri_analyses/module_within_corr.txt'),mmc_win)
    numpy.savetxt(os.path.join(basedir,'analyses/rsfmri_analyses/module_between_corr.txt'),mmc_bw)
    
if __name__ == "__main__":
    collapse_module_data()