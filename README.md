# myconnectome

Data analysis code for the [myconnectome project](http://www.myconnectome.org/)

### Dependencies

The code shared here requires a number of dependencies:

##### Binary

[FSL](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/)
[Tophat](http://ccb.jhu.edu/software/tophat/index.shtml)
[Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)
[htseq](http://www-huber.embl.de/users/anders/HTSeq/doc/overview.html)
[samtools](http://samtools.sourceforge.net/)
[Picard](http://picard.sourceforge.net/)
[RNA-SeQC](http://www.broadinstitute.org/cancer/cga/rna-seqc)

##### Python 

Beyond the standard scientific Packages, these packages are required:

[scikit-learn](http://scikit-learn.org/stable/)
[NetworkX](https://networkx.github.io/)
[igraph](http://igraph.org/python/)
[powerlaw](http://pythonhosted.org//powerlaw/)
[nibabel](http://nipy.org/nibabel/)

##### R

[forecast](http://cran.r-project.org/web/packages/forecast/index.html)
[DeSeq](http://bioconductor.org/packages/release/bioc/html/DESeq.html)
[gplots](http://cran.r-project.org/web/packages/gdata/index.html)

### timeseries_analyses

This directory contains code used to run time series analyses comparing different variables.

* est\_bivariate\_arima_model.R - code to run bivariate association analysis
* mk_graph.py - code to generate GEXF file representing the phenome-wide network

### rsfmri_analyses 

This directory contains code used to analyze the resting state fMRI data.

* rsfmri\_get\_network\_stats.py - code to compute graph-theoretic network stats
* circos_selftracking.py - code to generate circos config files for connectograms
* get\_parcel_info.py - code to get info about parcels
* mk\_renumbered_parcel_file.py - renumber parcel file to run consecutively

### taskfmri_analyses 

This directory contains code used to analyze the task fMRI data.

* map\_feats\_to_surface.py - map feat stats onto surface
* map\all\_feats\_to_surface.py - run for all feat analyses

### rnaseq_analyses 

This directory contains code used to analyze the RNA-seq data.

* process\_rnaseq.py - sets up shell scripts to run the RNA-seq analysis pathway
* rnaseq\_setup\_htcount\_data.R - uses DeSEQ to compute variance-stabilized read values
* \*_cmd.sh - examples of the scripts generated for a single session
* sum\_Reactome\_pathways.py - code to generate pathway eigengenes for Reactome pathways

### data

This contains various relevant data files

* parcellation/parcel_data.txt - information about the parcels
* parcellation/all\_selected\_L\_parcel.func.gii - LH parcellation, original numbering
* parcellation/all\_selected\_R\_parcel.func.gii - RH parcellation, original numbering
* parcellation/all\_selected\_L\_parcel_renumbered.func.gii - LH parcellation, renumbered to run consecutively
* parcellation/all\_selected\_R\_parcel_renumbered.func.gii - RH parcellation, renumbered to run consecutively
* parcellation/parcel_L_consensus.func.gii - LH consensus infomap clustering
* parcellation/parcel_R_consensus.func.gii - RH consensus infomap clustering
* rna-seq/varstab_data.txt - variance-stabilized expression values for genes passing thresholding

