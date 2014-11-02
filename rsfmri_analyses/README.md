## Resting state fMRI analyses

The code presented here starts with the extracted timecourses from each cortical parcel in each session, along with the volume data used to extract subcortical timeseries.  Preparation of those data was performed by the Petersen lab at Wash U.

These are the data that we started with:

* Timecourses from cortical parcels: https://s3.amazonaws.com/openfmri/ds031/rsfmri/all_selected_sessions_newparcel_timecourses.mat
* Temporal masks (denoting timepoints disrupted by motion, which were replaced and interpolated in the timecourse data and should be removed for most analyses): https://s3.amazonaws.com/openfmri/ds031/rsfmri/all_selected_sessions_tmasks.mat
* Session codes: https://s3.amazonaws.com/openfmri/ds031/rsfmri/all_selected_sessions_names.txt

#### Data extraction

* extract_datafiles.m: MATLAB script to extract data from mat files into text files
* rsfmri_get_subcortical_data.py: extract mean timecourse from each of the subcortical regions listed in aseg_fields.txt and save to a text file.  Uses subcortical segmentation from freesurfer.
* rsfmri_combine_data.py: combine cortical and subcortical data, generate both full and scrubbed timeseries
* rsfmri_extract_module_assignments.py: generate file with module assignments for each parcel from parcellation gifti files

### Correlation analysis

* rsfmri_extract_module_summary.py: extract the mean within-module connectivity for each of the 13 modules identified using infomap clustering
* rsfmri_collapse_module_data.py: collapse data from each session into a single file (https://s3.amazonaws.com/openfmri/ds031/rsfmri/module_within_corr.txt) - these are the data that are loaded by load_fmri_data() for the timeseries analyses.