# myconnectome

Data analysis code for the [myconnectome project](http://www.myconnectome.org/)

The goal of this project is to demonstrate reproducible analysis for a large and complex dataset.  The package provides a set of scripts that will implement all of the statistical analyses and some of the preprocessing steps for the data from the MyConnectome study, as reported by Poldrack et al. (submitted).  Code is not currently included for the cortical parcellation steps that were performed at Washington University.

Users who wish to use this package in a turnkey fashion should try the [Myconnectome-VM](https://github.com/poldrack/myconnectome-vm) which will automatically set up a virtual machine that will complete the full statistical analysis workflow.

## Getting started

To install the package, first clone it to your local machine:

`git clone https://github.com/poldrack/myconnectome.git`

Then run the setup script:

`cd myconnectome`
`python setup.py install`

### Dependencies

The code shared here requires a number of dependencies:

##### Python 

If you don't already have a scientific Python distribution installed, I would recommend [Anaconda](http://continuum.io/downloads).  Beyond the standard scientific Python stack, a number of additional packages are required, which you can install using the following set of commands (assuming that you have Anaconda already installed):

`pip install setuptools`
`conda install --yes pip numpy scipy nose traits networkx`
`conda install --yes dateutil ipython-notebook matplotlib`
`conda install --yes statsmodels boto  pandas scikit-learn`
`pip install nibabel`
`pip install gtf_to_genes`
`pip install suds`
`pip install mygene`



##### Binary

* [FSL](http://fsl.fmrib.ox.ac.uk/fsl/fslwiki/)
* [Tophat](http://ccb.jhu.edu/software/tophat/index.shtml)
* [Bowtie2](http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)
* [htseq](http://www-huber.embl.de/users/anders/HTSeq/doc/overview.html)
* [samtools](http://samtools.sourceforge.net/)
* [Picard](http://picard.sourceforge.net/)
* [RNA-SeQC](http://www.broadinstitute.org/cancer/cga/rna-seqc)

##### Python 

Beyond the standard scientific Packages, these packages are required:

* [scikit-learn](http://scikit-learn.org/stable/)
* [NetworkX](https://networkx.github.io/)
* [igraph](http://igraph.org/python/)
* [powerlaw](http://pythonhosted.org//powerlaw/)
* [nibabel](http://nipy.org/nibabel/)

##### R

* [forecast](http://cran.r-project.org/web/packages/forecast/index.html)
* [DeSeq](http://bioconductor.org/packages/release/bioc/html/DESeq.html)
* [gplots](http://cran.r-project.org/web/packages/gdata/index.html)

### timeseries_analyses

This directory contains code used to run time series analyses comparing different variables.


### rsfmri_analyses 

This directory contains code used to analyze the resting state fMRI data.


### metabolomic_analyses 

This directory contains code used to analyze the metabolomics data.

### rnaseq_analyses 

This directory contains code used to analyze the RNA-seq data.

