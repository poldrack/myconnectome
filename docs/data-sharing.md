
An important goal of the MyConnectome Project is to disseminate the data and code so that other researchers can use it to test new hypotheses and techniques.  We are making the data available in a number of different ways.

#### Browsing the results

All of the statistical results can be viewed using the [myconnectome-vm virtual machine](https://github.com/poldrack/myconnectome-vm).

#### Reproducing the Analysis Workflow

We have built a system that will allow any researcher to reproduce the statistical analyses reported in Poldrack et al. (submitted) on their own computer.  This is accomplished using the Vagrant virtual machine provisioning system, which will automatically create a virtual machine on any computer, download the necessary preprocessed data, run all of the analyses, and provide a browser for the data.  Code and instructions are available at the [Myconnectome-VM github page](https://github.com/poldrack/myconnectome-vm).

It is also possible to reproduce the analysis workflow on one’s own machine using the [Myconnectome python package](https://github.com/poldrack/myconnectome).  However, this requires substantially more effort to install all of the necessary software dependencies, so in general we recommend the virtual machine route for most users.

#### Obtaining the raw data

The entire raw data set is released under the Public Domain Dedication and License v1.0 whose full text can be found at [http://www.opendatacommons.org/licenses/pddl/1.0/](http://www.opendatacommons.org/licenses/pddl/1.0/).  We also ask that researchers follow the [Attribution-ShareAlike community norms](http://opendatacommons.org/norms/odc-by-sa/).  We further request that researchers who discovery any health-relevant findings will contact Dr. Poldrack prior to publicly releasing those results.

The raw data are available from the following locations:

fMRI: [http://openfmri.org/dataset/ds000031](http://openfmri.org/dataset/ds000031)

The raw fMRI data can also be downloaded directly from here (each of the main files is about 8 GB compressed):

*   Production Sessions
    *   Sessions 13-24: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_set01.tar](https://s3.amazonaws.com/openfmri/tarballs/ds031_set01.tar)
    *   Sessions 25-36: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_set02.tar](https://s3.amazonaws.com/openfmri/tarballs/ds031_set02.tar)
    *   Sessions 37-48: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_set03.tar](https://s3.amazonaws.com/openfmri/tarballs/ds031_set03.tar)
    *   Sessions 49-60: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_set04.tar](https://s3.amazonaws.com/openfmri/tarballs/ds031_set04.tar)
    *   Sessions 61-72: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_set05.tar](https://s3.amazonaws.com/openfmri/tarballs/ds031_set05.tar)
    *   Sessions 73-84: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_set06.tar](https://s3.amazonaws.com/openfmri/tarballs/ds031_set06.tar)
    *   Sessions 85-97: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_set07.tar](https://s3.amazonaws.com/openfmri/tarballs/ds031_set07.tar)
    *   Sessions 98- 104: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_set08.tar](https://s3.amazonaws.com/openfmri/tarballs/ds031_set08.tar)
    *   Retinotopy session: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_retinotopy.tgz](https://s3.amazonaws.com/openfmri/tarballs/ds031_retinotopy.tgz)
*   Followup sessions:
    *   Session 105 (resting state at Wash U): [https://s3.amazonaws.com/openfmri/tarballs/ds031\_ses105.tgz](https://s3.amazonaws.com/openfmri/tarballs/ds031_ses105.tgz)
    *   Session 106 (diffusion at Stanford): [https://s3.amazonaws.com/openfmri/tarballs/ds031\_ses106.tgz](https://s3.amazonaws.com/openfmri/tarballs/ds031_ses106.tgz)
*   Pilot sessions
    *   [https://s3.amazonaws.com/openfmri/tarballs/ds031\_pilot\_set.tar](https://s3.amazonaws.com/openfmri/tarballs/ds031_pilot_set.tar)

RNA-seq: [Gene Expression Omnibus (accession #GSE58122)](http://www.ncbi.nlm.nih.gov/geo/query/acc.cgi?token=yfqzaooshpijdsn&acc=GSE58122)

Metabolomics: [original raw dataset](http://web.stanford.edu/group/poldracklab/myconnectome-data/metabolomics/metabolomics_raw_data.xlsx)

Behavioral data: [trackingdata.txt](http://web.stanford.edu/group/poldracklab/myconnectome-data/base/behavior/trackingdata.txt)

The entire set of preprocessed data provided through the reproducible workflow can also be downloaded directly using the following command:

wget -N -r -l inf --no-remove-listing -nH --cut-dirs=3 http://web.stanford.edu/group/poldracklab/myconnectome-data/

#### Processed data

Processed data (including volume-registered, surface-registered, and parcel timeseries data) are available from these links:

*   Sessions 14-25: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_processed\_set01.tgz](https://s3.amazonaws.com/openfmri/tarballs/ds031_processed_set01.tgz)
*   Sessions 26-40: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_processed\_set02.tgz](https://s3.amazonaws.com/openfmri/tarballs/ds031_processed_set02.tgz)
*   Sessions 41-53: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_processed\_set03.tgz](https://s3.amazonaws.com/openfmri/tarballs/ds031_processed_set03.tgz)
*   Sessions 54-66: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_processed\_set04.tgz](https://s3.amazonaws.com/openfmri/tarballs/ds031_processed_set04.tgz)
*   Sessions 67-78: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_processed\_set05.tgz](https://s3.amazonaws.com/openfmri/tarballs/ds031_processed_set05.tgz)
*   Sessions 79-91: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_processed\_set06.tgz](https://s3.amazonaws.com/openfmri/tarballs/ds031_processed_set06.tgz)
*   Sessions 92-104: [https://s3.amazonaws.com/openfmri/tarballs/ds031\_processed\_set07.tgz](https://s3.amazonaws.com/openfmri/tarballs/ds031_processed_set07.tgz)

#### Surface fMRI data

The processed surface-based fMRI data can be accessed using the [Connectome Workbench](http://www.humanconnectome.org/software/connectome-workbench.html) software from the Human Connectome Project.

To view the data using the Connectome Workbench:

1.  Download the software from the link above and install.
2.  Launch the software, and click “skip” if it asks you whether you want to open a file.
3.  Select File->Open Location.  Click “Custom” and choose “Specification” from the Type menu.
4.  In the URL window, enter the following URL and then click “OK”: https://s3-us-west-2.amazonaws.com/myconnectome/data/workbench/myconnectome\_web.32k\_fs\_LR.wb.spec
5.  When the “Open Spec File” window appears, click Load at the bottom. You may get asked for a password – just click OK since these files don’t require a password.
6.  The data are now loaded into the viewer.  To view stored scenes from several of the figures, click on the scene button at the top right of the viewer and then choose the scene you want to view.

#### Network visualizations

The network visualizations presented in the paper were generated using the [Cytoscape](http://www.cytoscape.org/) software.  You can visualize them directly by downloading the following files and opening them in Cytoscape:

[Tuesday vs. Thursday connectivity](http://web.stanford.edu/group/poldracklab/myconnectome-data/cytoscape/tuesthurs_connectivity.cys)

[Phenome-wide network](http://web.stanford.edu/group/poldracklab/myconnectome-data/cytoscape/phenome_wide_graph.cys)

A project of the [Poldrack Lab](http://www.poldracklab.org) at  [Stanford University](http://www.stanford.edu)
