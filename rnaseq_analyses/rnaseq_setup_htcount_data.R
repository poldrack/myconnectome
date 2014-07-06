# generate variabte-stabilized expression data

#source("http://bioconductor.org/biocLite.R")
#biocLite("DESeq")
library(DESeq)

# load data 
cdsFull=newCountDataSetFromHTSeqCount(read.table('htcount_files.txt'),directory="/Users/poldrack/Dropbox/data/selftracking/rna-seq/htcount_files")
cdsFull = estimateSizeFactors( cdsFull )

# get mean expression for each gene across sesssions
rs = rowMeans ( counts ( cdsFull ))
allgenes=rownames(counts(cdsFull))

# remove genes with 
use = (rs>4 & rs<10000)
cds=cdsFull[use,]
usedgenes=rownames(counts(cds))

# generate variance-stabilized count data and save to file

cdsBlind = estimateDispersions( cds, method="blind" ,fitType='local')
vsd = varianceStabilizingTransformation( cdsBlind )
vsdata=getVarianceStabilizedData(cdsBlind)
write.table(vsdata,'/Users/poldrack/Dropbox/data/selftracking/rna-seq/varstab_data.txt')

# plot some diagnostic figures

plotDispEsts( cdsBlind )

#plot SD vs. count before and after correction
library(vsn)
par(mfrow=c(1,2))
notAllZero = (rowSums(counts(cds))>0)
meanSdPlot(log2(counts(cds)[notAllZero, ] + 1), ylim = c(0,2.5))
meanSdPlot(vsd[notAllZero, ], ylim = c(0,2.5))


# plot clusters of genes/subjects
library("RColorBrewer")
library("gplots")
select = order(rowMeans(counts(cdsBlind)), decreasing=TRUE)[1:30]
hmcol = colorRampPalette(brewer.pal(9, "GnBu"))(100)
heatmap.2(exprs(vsd)[select,], col = hmcol, trace="none", margin=c(10, 6))

# plot clusters of subjects - to look for outliers
dists = dist( t( exprs(vsd) ) )
mat = as.matrix( dists )
heatmap.2(mat, trace="none", col = rev(hmcol), margin=c(13, 13))

