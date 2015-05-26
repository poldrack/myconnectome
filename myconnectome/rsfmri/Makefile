clean:
	rm /corral-repl/utexas/poldracklab/data/selftracking/combined_data/*
	rm /corral-repl/utexas/poldracklab/data/selftracking/subdata/*
	rm /corral-repl/utexas/poldracklab/data/selftracking/combined_data_scrubbed/*
	rm -rf /corral-repl/utexas/poldracklab/data/selftracking/analyses/rsfmri_analyses/*

extract_datafiles:
	matlab -nodesktop < extract_datafiles.m

get_subcortical_data:
	python rsfmri_get_subcortical_data.py

combine_cort_subcort_data:
	python rsfmri_combine_data.py

get_parcel_info:
	python get_parcel_info.py

extract_module_assignments:
	python rsfmri_extract_module_assignments.py

extract_module_summary:
	python rsfmri_extract_module_summary.py

collapse_module_data:
	python rsfmri_collapse_module_data.py

run_all_netstats:
	launch -s run_all_netstats.sh -e 4way -p 636 -r 48:00:00 -n netstats