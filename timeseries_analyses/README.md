## Code for timeseries analyses

The primary analyses for the MyConnectome paper are comparisons of different variables over time, which is the purpose of this code.

#### getting the data

* load_myconnectome_data.R: R code that contains functions to load all of the different data types.  All of the data are located in the cloud, so no additional data files need to be downloaded.
* load_myconnectome_data.py: python code to load data, this one requires that they be downloaded to the local system and that the locations be fixed in the code

#### analysis code


* est_bivariate_arima_model.R: this is the code to perform the timeseries modeling
* data_utilities.R: some utility functions used by other scripts

#### Running the analyses

* timeseries_analyses.Rmd: Rmarkdown code to run the timeseries analyses for all variables.  Results can be viewed at https://s3.amazonaws.com/openfmri/ds031/timeseries_analyses/timeseries_analyses.html
* Make_Timeseries_Heatmaps.Rmd: Rmarkdown code to generate timeseries heatmaps for behavior, connectivity, and RNA-seq variables.  Results can be viewed at https://s3.amazonaws.com/openfmri/ds031/timeseries_analyses/Make_Timeseries_Heatmaps.html
* Make_timeseries_plots.Rmd: Rmarkdown code to generate timeseries plots and trend analyses for each variable.  Results can be viewed at https://s3.amazonaws.com/openfmri/ds031/timeseries_analyses/Make_timeseries_plots.html
* Mediation_analysis.Rmd: Rmarkdown code to run mediation model for fatigue as a mediator between day of week and connectivity.  Results can be viewed at https://s3.amazonaws.com/openfmri/ds031/timeseries_analyses/Mediation_analysis.html
