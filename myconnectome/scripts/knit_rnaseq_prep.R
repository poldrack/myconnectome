# knit rmarkdown for RNAseq analyses

require(knitr) # required for knitting from rmd to md
require(markdown) # required for md to html 
knit('RNAseq_data_preparation.Rmd', 'RNAseq_data_preparation.md') # creates md file
markdownToHTML('RNAseq_data_preparation.md', 'RNAseq_data_preparation.html') # creates html file
browseURL(paste('file://', file.path(getwd(),'RNAseq_data_preparation.html'), sep='')) # open file in browser 