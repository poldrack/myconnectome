"""
run processing for rsfmri analysis
"""

from myconnectome.rsfmri import *
from myconnectome.utils.get_data import get_base_data,get_directory
from myconnectome.utils.run_shell_cmd import run_shell_cmd
from myconnectome.utils.log_time import log_time, get_time

import os

try:
    basedir=os.environ['MYCONNECTOME_DIR']
except:
    raise RuntimeError('you must first set the MYCONNECTOME_DIR environment variable')

logdir=os.path.join(basedir,'logs')
if not os.path.exists(logdir):
    os.mkdir(logdir)
logfile=os.path.join(logdir,'data_downloads.log')

filepath=os.path.dirname(os.path.abspath(__file__))

timefile = os.environ["TIME_LOG_FILE"]

get_base_data(logfile=logfile)

rsdir=os.path.join(basedir,'rsfmri')

if not os.path.exists(rsdir):
    os.mkdir(rsdir)

# make renumbered parcel file
parcel_renumbered_file = os.path.join(basedir,'parcellation/all_selected_L_new_parcel_renumbered.func.gii')
if not os.path.exists(parcel_renumbered_file):
    starttime = get_time()
    mk_renumbered_parcel_file.mk_renumbered_parcel_file()
    endtime = get_time()
    log_time(timefile,starttime,endtime,parcel_renumbered_file)

# get parcel info
if not os.path.exists(os.path.join(basedir,'parcellation/parcel_data.txt')):
    starttime = get_time()
    get_parcel_info.get_parcel_info()
    endtime = get_time()
    log_time(timefile,starttime,endtime,parcel_renumbered_file)

if not os.path.exists(os.path.join(basedir,'rsfmri/module_assignments.txt')):
    starttime = get_time()
    extract_module_assignments.extract_module_assignments()
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(basedir,'rsfmri/module_assignments.txt'))

if not os.path.exists(os.path.join(basedir,'rsfmri/bwmod_corr_labels.txt')):
    starttime = get_time()
    extract_module_summary.extract_module_summary()
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(basedir,'rsfmri/bwmod_corr_labels.txt'))

if not os.path.exists(os.path.join(basedir,'rsfmri/module_within_corr.txt')):
    starttime = get_time()
    collapse_module_data.collapse_module_data()
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(basedir,'rsfmri/module_within_corr.txt'))

if not os.path.exists(os.path.join(basedir,'rsfmri/corrdata.npy')):
    starttime = get_time()
    get_corrdata.get_corrdata()
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(basedir,'rsfmri/corrdata.npy'))


if not os.path.exists(os.path.join(basedir,'rsfmri/geff_pos.txt')):
  if len(run_shell_cmd('which matlab'))>0:
    cmd='matlab -nodesktop -nosplash <%s/bct_analyses.m'%filepath
    print cmd
    print 'this may take a little while...'
    starttime = get_time()
    run_shell_cmd(cmd)
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(basedir,'rsfmri/geff_pos.txt'))

  else:
      print 'MATLAB not available, downloading BCT results from repository'
      starttime = get_time()
      get_directory('bct/',basedir)
      endtime = get_time()
      log_time(timefile,starttime,endtime,os.path.join(basedir,'rsfmri/geff_pos.txt'))
      
if not os.path.exists(os.path.join(basedir,'parcellation/all_selected_L_new_parcel_renumbered_boundaries.func.gii')):
    starttime = get_time()
    mk_parcellation_boundaries.mk_parcellation_boundaries()
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(basedir,'parcellation/all_selected_L_new_parcel_renumbered_boundaries.func.gii'))

if not os.path.exists(os.path.join(basedir,'rsfmri/network_graph_all_0.010.graphml')):
    starttime = get_time()
    for day in ['mon','tues','thurs','all']:
        mk_full_network_graph.mk_full_network_graph(day)
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(basedir,'rsfmri/network_graph_all_0.010.graphml'))

if not os.path.exists(os.path.join(basedir,'diffusion/adjmtx_binarized_sorted_modules.pdf')):
    starttime = get_time()
    mk_sorted_adjmatrices.mk_sorted_adjmatrices()
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(basedir,'diffusion/adjmtx_binarized_sorted_modules.pdf'))

if not os.path.exists(os.path.join(basedir,'diffusion/dti_connectome.pdf')):
    starttime = get_time()
    mk_connectome_figures.mk_connectome_figures()
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(basedir,'diffusion/dti_connectome.pdf'))

if not os.path.exists(os.path.join(basedir,'rsfmri/mean_similarity_plot.pdf')):
    starttime = get_time()
    connectome_similarity_timeseries.connectome_similarity_timeseries()
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(basedir,'rsfmri/mean_similarity_plot.pdf'))
 
# make QA page
if not os.path.exists(os.path.join(rsdir,'QA_summary_rnaseq.html')):
    starttime = get_time()
    f=open(os.path.join(filepath,'knit_rsfmri_qa.R'),'w')
    f.write('# automatically generated knitr command file\n')
    f.write('require(knitr)\n')
    f.write('require(markdown)\n')
    f.write('setwd("%s")\n'%rsdir)
    f.write("knit('%s/QA_summary_rsfmri.Rmd', '%s/QA_summary_rsfmri.md')\n"%
        (filepath.replace('scripts','qa'),rsdir))
    f.write("markdownToHTML('%s/QA_summary_rsfmri.md', '%s/QA_summary_rsfmri.html')\n"%
        (rsdir,rsdir))
    f.close()

    run_shell_cmd('Rscript %s/knit_rsfmri_qa.R'%filepath)
    endtime = get_time()
    log_time(timefile,starttime,endtime,os.path.join(rsdir,'QA_summary_rnaseq.html'))
