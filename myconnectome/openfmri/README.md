Code to convert from original layout to BIDS specification 1.0




1. convert UT data from dicom to nifti using dcmstack

first need to copy dicoms to scratch:
cd /corral-repl/utexas/poldracklab/data/selftracking/dicom
tar cf - * | tar xf - -C /scratch/01329/poldrack/selftracking/dicoms/

python dcmstack_convert.py

launch -s run_dcmstack.sh -r 01:00:00 -n dcmstack -p 120

also need to extract json files from nii.gz files using nitool dump (see dump_json.sh)

2. copy data

python make_dist_dcmstack.py

 launch -s copy_dcmstack_files.sh -r 04:00:00 -e 4way -p 60

3. validate

 /corral-repl/utexas/poldracklab/software_lonestar/node_modules/bids-validator/bin/bids-validator ./ds031 > validator.out

