# run analysis on specific gene and wincorr variables


basedir=Sys.getenv('MYCONNECTOME_DIR')

library(forecast)
source(sprintf('%s/myconnectome/timeseries/est_bivariate_arima_model.R',basedir))

load_rnaseq_drawdates=function(infile=sprintf('%s/rna-seq/drawdates.txt',basedir)) {
  d=read.table(infile,header=FALSE)$V1
  dates=as.Date(d,'%m/%d/%Y')
  return(dates)
}

drawdates=load_rnaseq_drawdates()

xvars=c('panas.positive','panas.negative','prevevening.Psoriasisseverity')

outdir=sprintf('%s/rna-seq/gwas_wincorr',basedir)

args <- commandArgs(trailingOnly = TRUE)
gene_num=as.integer(args[1])
cat(gene_num)

load(sprintf('%s/rsfmri/wincorr.Rdata',basedir))
genedata=read.table(sprintf('%s/rna-seq/expression_sep_files/expr_snpPCreg_%05d.txt',basedir,gene_num))
genedata$date=drawdates

out.dat.rnaseq=est_bivariate_arima_model(genedata,wincorr,verbose=TRUE,spacing='1 week')

write.table(out.dat.rnaseq,file=sprintf('%s/wincorr_%05d.txt',outdir,gene_num),row.names=FALSE,col.names=FALSE)