import os,glob


infile='/corral-repl/utexas/poldracklab/data/selftracking/breathhold_events.tsv'


outdir='/scratch/01329/poldrack/selftracking/ds031/sub-01'

bholdfiles=glob.glob(os.path.join(outdir,'ses*/func/*task-breathhold_acq-MB_run-001_bold*nii.gz'))

for f in bholdfiles:
    outfile=f.replace('_acq-MB','').replace('_bold.nii.gz','_events.tsv')
    print 'cp %s %s'%(infile,outfile)
