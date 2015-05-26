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

##### R

The packages used here require R 3.0 or greater; I would recommend installing the latest version from [CRAN](http://cran.us.r-project.org/).  The R scripts in the package will attempt to automatically install all necessary packages, so you shouldn't need to install any additional packages yourself.

##### Connectome Workbench

Some of the processing operations require the [Connectome Workbench] (http://www.humanconnectome.org/software/get-connectome-workbench.html), which can also be used to visualize the surface-based results.

