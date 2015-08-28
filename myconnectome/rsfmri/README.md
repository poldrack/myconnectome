## Resting state fMRI analyses

The code presented here starts with the extracted timecourses from each cortical parcel in each session, along with the volume data used to extract subcortical timeseries.  Preparation of those data was performed by the Petersen lab at Wash U.

The data for these analyses can be obtained using:

  python utils/get_data.py --base

#### Data extraction

* extract_datafiles.m: MATLAB script to extract data from mat files into text files
* rsfmri_get_subcortical_data.py: extract mean timecourse from each of the subcortical regions listed in aseg_fields.txt and save to a text file.  Uses subcortical segmentation from freesurfer.
* rsfmri_combine_data.py: combine cortical and subcortical data, generate both full and scrubbed timeseries
* rsfmri_extract_module_assignments.py: generate file with module assignments for each parcel from parcellation gifti files

### Correlation analysis

* rsfmri_extract_module_summary.py: extract the mean within-module connectivity for each of the 13 modules identified using infomap clustering
* rsfmri_collapse_module_data.py: collapse data from each session into a single file  - these are the data that are loaded by load_fmri_data() for the timeseries analyses.
