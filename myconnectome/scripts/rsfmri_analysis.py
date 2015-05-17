"""
run processing for rsfmri analysis
"""

from myconnectome.rsfmri import *
#from myconnectome.rsfmri.get_rsfmri_data import get_all_data

import os

try:
    basedir=os.environ['MYCONNECTOME_DIR']
except:
    raise RuntimeError('you must first set the MYCONNECTOME_DIR environment variable')

get_rsfmri_data.get_all_data()

# make renumbered parcel file
if not os.path.exists(os.path.join(basedir,'parcellation/all_selected_L_new_parcel_renumbered.func.gii')):
    mk_renumbered_parcel_file()

# get parcel info
if not os.path.exists(os.path.join(basedir,'parcellation/parcel_data.txt')):
    get_parcel_info()

if not os.path.exists(os.path.join(basedir,'analyses/rsfmri_analyses/module_assignments.txt')):
    extract_module_assignments()

if not os.path.exists(os.path.join(basedir,'analyses/rsfmri_analyses/bwmod_corr_labels.txt')):
    extract_module_summary()

if not os.path.exists(os.path.join(basedir,'analyses/rsfmri_analyses/module_within_corr.txt')):
    collapse_module_data()

if not os.path.exists(os.path.join(basedir,'analyses/rsfmri_analyses/corrdata.npy')):
    get_corrdata()

