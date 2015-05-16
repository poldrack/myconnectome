"""
combine data from cortical and subcortical rois
- right now just use full hippocampus rather than subfields

"""

import os,glob,numpy

datadir_surface='/corral-repl/utexas/poldracklab/data/selftracking/subdata'
tmaskdir='/corral-repl/utexas/poldracklab/data/selftracking/analyses/tmasks'
datadir_aseg='/corral-repl/utexas/poldracklab/data/selftracking/aseg_data'
datadir_mtl='/corral-repl/utexas/poldracklab/data/selftracking/mtl_data'
outdir='/corral-repl/utexas/poldracklab/data/selftracking/combined_data_scrubbed'


datafiles_surface=glob.glob(os.path.join(datadir_surface,'sub*txt'))

subcodes=[i.split('/')[-1].replace('.txt','') for i in datafiles_surface]

for s in subcodes:
    outfile=os.path.join(outdir,'%s.txt'%s)
    print s
    data_surface=numpy.loadtxt(os.path.join(datadir_surface,'%s.txt'%s))
    data_aseg=numpy.loadtxt(os.path.join(datadir_aseg,'%s_asegmean.txt'%s))
    
    data=numpy.hstack((data_surface,data_aseg))
    numpy.savetxt(outfile,data)
#    tmask=numpy.loadtxt(os.path.join(tmaskdir,'%s.txt'%s))
#    data_scrubbed=data[tmask==1,:]
#    outfile_scrubbed=os.path.join(outdir_scrubbed,'%s.txt'%s)
#    numpy.savetxt(outfile_scrubbed,data_scrubbed)
    
