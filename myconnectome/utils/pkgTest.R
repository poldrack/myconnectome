# test for package
# if it doesn't exist, first try installing from CRAN
# then from bioconductor

pkgTest <- function(x)
  {
    if (!require(x,character.only = TRUE))
    {
      install.packages(x,dep=TRUE,repos="http://cran.rstudio.com")
    }
    if (!require(x,character.only = TRUE))
    {
	source("http://bioconductor.org/biocLite.R")
	biocLite(x)
    }
        if(!require(x,character.only = TRUE)) stop("Package not available from CRAN or bioconductor - something must be wrong")
  }
