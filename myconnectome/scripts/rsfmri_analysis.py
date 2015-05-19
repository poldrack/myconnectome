"""
run processing for rsfmri analysis
"""

from myconnectome.rsfmri import *
from myconnectome.utils.get_data import get_all_data,get_file_from_s3
from myconnectome.utils.run_shell_cmd import run_shell_cmd

import os

try:
    basedir=os.environ['MYCONNECTOME_DIR']
except:
    raise RuntimeError('you must first set the MYCONNECTOME_DIR environment variable')

filepath=os.path.dirname(os.path.abspath(__file__))

get_all_data()

if not os.path.exists(os.path.join(basedir,'rsfmri')):
    os.mkdir(os.path.join(basedir,'rsfmri'))
if not os.path.exists(os.path.join(basedir,'rsfmri/mean_fd.txt')):
    get_file_from_s3('ds031/rsfmri/mean_fd.txt',os.path.join(basedir,'rsfmri/mean_fd.txt'))

# make renumbered parcel file
if not os.path.exists(os.path.join(basedir,'parcellation/all_selected_L_new_parcel_renumbered.func.gii')):
    mk_renumbered_parcel_file.mk_renumbered_parcel_file()

# get parcel info
if not os.path.exists(os.path.join(basedir,'parcellation/parcel_data.txt')):
    get_parcel_info.get_parcel_info()

if not os.path.exists(os.path.join(basedir,'rsfmri/module_assignments.txt')):
    extract_module_assignments.extract_module_assignments()

if not os.path.exists(os.path.join(basedir,'rsfmri/bwmod_corr_labels.txt')):
    extract_module_summary.extract_module_summary()

if not os.path.exists(os.path.join(basedir,'rsfmri/module_within_corr.txt')):
    collapse_module_data.collapse_module_data()

if not os.path.exists(os.path.join(basedir,'rsfmri/corrdata.npy')):
    get_corrdata.get_corrdata()


if not os.path.exists(os.path.join(basedir,'rsfmri/geff_pos.txt')):
  if len(run_shell_cmd('which matlab'))>0:
    cmd='matlab -nodesktop -nosplash <%s/bct_analyses.m'%filepath
    print cmd
    print 'this may take a little while...'
    run_shell_cmd(cmd)
  else:
      print 'MATLAB not available, downloading BCT results from S3'
      get_file_from_s3('ds031/rsfmri/modularity_weighted_louvain_bct.txt',os.path.join(basedir,'rsfmri/modularity_weighted_louvain_bct.txt'))  
      get_file_from_s3('ds031/rsfmri/PIpos_weighted_louvain_bct.txt',os.path.join(basedir,'rsfmri/PIpos_weighted_louvain_bct.txt'))  
      get_file_from_s3('ds031/rsfmri/geff_pos.txt',os.path.join(basedir,'rsfmri/geff_pos.txt'))  
    
if not os.path.exists(os.path.join(basedir,'parcellation/all_selected_L_new_parcel_renumbered_boundaries.func.gii')):
    mk_parcellation_boundaries.mk_parcellation_boundaries()
