# automatically generated knitr command file
pkgTest <- function(x)
  {
    if (!require(x,character.only = TRUE))
    {
      install.packages(x,dep=TRUE)
        if(!require(x,character.only = TRUE)) stop("Package not found")
    }
  }
pkgTest("knitr")
pkgTest("WGCNA")
pkgTest("DESeq")
pkgTest("RColorBrewer")
pkgTest("vsn")
pkgTest("gplots")
