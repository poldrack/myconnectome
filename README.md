# myconnectome

Data analysis code for the [myconnectome project](http://www.myconnectome.org/)

### timeseries_analyses

This directory contains code used to run time series analyses comparing different variables.

* est\_bivariate\_arima_model.R - code to run bivariate association analysis
* mk_graph.py - code to generate GEXF file representing the phenome-wide network

### rsfmri_analyses 

This directory contains code used to analyze the resting state fMRI data.

* rsfmri\_get\_network\_stats.py - code to compute graph-theoretic network stats
* circos_selftracking.py - code to generate circos config files for connectograms
* get_parcel_info.py - code to get info about parcels

### rnaseq_analyses 

This directory contains code used to analyze the RNA-seq data.

* process\_rnaseq.py - sets up shell scripts to run the RNA-seq analysis pathway
* rnaseq\_setup\_htcount\_data.R - uses DeSEQ to compute variance-stabilized read values


### data

This contains various relevant data files

* parcellation/parcel_data.txt - information about the parcels
* parcellation/all\_selected\_L\_parcel.func.gii - LH parcellation, original numbering
* parcellation/all\_selected\_R\_parcel.func.gii - RH parcellation, original numbering
* parcellation/all\_selected\_L\_parcel_renumbered.func.gii - LH parcellation, renumbered to run consecutively
* parcellation/all\_selected\_R\_parcel_renumbered.func.gii - RH parcellation, renumbered to run consecutively
* parcellation/parcel_L_consensus.func.gii - LH consensus infomap clustering
* parcellation/parcel_R_consensus.func.gii - RH consensus infomap clustering
* 
