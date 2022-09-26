
An important goal of the MyConnectome Project is to disseminate the data and code so that other researchers can use it to test new hypotheses and techniques.  We are making the data available in a number of different ways.


#### Obtaining the raw data

The entire raw data set is released under the Public Domain Dedication and License v1.0 whose full text can be found at [http://www.opendatacommons.org/licenses/pddl/1.0/](http://www.opendatacommons.org/licenses/pddl/1.0/).  We also ask that researchers follow the [Attribution-ShareAlike community norms](http://opendatacommons.org/norms/odc-by-sa/).  We further request that researchers who discovery any health-relevant findings will contact Dr. Poldrack prior to publicly releasing those results.

The raw data are available from the following locations:

fMRI: [https://openneuro.org/datasets/ds000031](https://openneuro.org/datasets/ds000031)

RNA-seq: [Gene Expression Omnibus (accession #GSE58122)](http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?token=yfqzaooshpijdsn&acc=GSE58122)

Metabolomics: [original raw dataset](http://web.stanford.edu/group/poldracklab/myconnectome-data/metabolomics/metabolomics_raw_data.xlsx)

Behavioral data: [trackingdata.txt](http://web.stanford.edu/group/poldracklab/myconnectome-data/base/behavior/trackingdata.txt)

The entire set of preprocessed data provided through the reproducible workflow can also be downloaded directly using the following command:

wget -N -r -l inf --no-remove-listing -nH --cut-dirs=3 http://web.stanford.edu/group/poldracklab/myconnectome-data/


#### Network visualizations

The network visualizations presented in the paper were generated using the [Cytoscape](http://www.cytoscape.org/) software.  You can visualize them directly by downloading the following files and opening them in Cytoscape:

[Tuesday vs. Thursday connectivity](http://web.stanford.edu/group/poldracklab/myconnectome-data/cytoscape/tuesthurs_connectivity.cys)

[Phenome-wide network](http://web.stanford.edu/group/poldracklab/myconnectome-data/cytoscape/phenome_wide_graph.cys)

A project of the [Poldrack Lab](http://www.poldracklab.org) at  [Stanford University](http://www.stanford.edu)
