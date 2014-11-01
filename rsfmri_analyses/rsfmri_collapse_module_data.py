"""
combine module data into single files
"""

import os,sys
import numpy

outdir_modeig='/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/modeig_data'
outdir_bwmod='/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/bwmod_corr_data'
outdir_winmod='/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/winmod_corr_data'
outdir_alff='/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/module_alff'

subcodes=[i.strip() for i in open('/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/subcodes.txt').readlines()]

mmc_win=numpy.zeros((len(subcodes),13))
mmc_bw=numpy.zeros((len(subcodes),78))
mod_alff=numpy.zeros((len(subcodes),13))

subctr=0
for subcode in subcodes:
    mmc_win[subctr,:]=numpy.loadtxt(os.path.join(outdir_winmod,subcode+'.txt'))
    mmc_bw[subctr,:]=numpy.loadtxt(os.path.join(outdir_bwmod,subcode+'.txt'))
    mod_alff[subctr,:]=numpy.loadtxt(os.path.join(outdir_alff,subcode+'.txt'))
    subctr+=1

numpy.savetxt('/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/module_within_corr.txt',mmc_win)
numpy.savetxt('/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/module_between_corr.txt',mmc_bw)
numpy.savetxt('/corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/module_falff.txt',mod_alff)
