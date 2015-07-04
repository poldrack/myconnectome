# make figure showing assocation of bwmod connectivity and rna-seq

library(gplots)
basedir=Sys.getenv('MYCONNECTOME_DIR')
if (basedir=='') {
  Sys.setenv(MYCONNECTOME_DIR='/Users/poldrack/data_unsynced/myconnectome')
  basedir='/Users/poldrack/data_unsynced/myconnectome'
}


source('/Users/poldrack/code/myconnectome/myconnectome/timeseries/load_myconnectome_data.R')
wgcna=load_rnaseq_data()
modnames=c()
for (i in 1:63) {
  m=gsub(':no enrichment','',names(wgcna)[i])
  modnames=rbind(modnames,m)
}
bwcorr.wgcna.t=read.table(sprintf('%s/timeseries/bwcorr_wgcna_t.txt',basedir),
                        header=FALSE)
bwcorr.wgcna.p=read.table(sprintf('%s/timeseries/bwcorr_wgcna_fdrp.txt',basedir),
                          header=FALSE)


netnames=read.table(sprintf('%s/timeseries/netnames.txt',basedir),
                        header=FALSE)
bwnames=read.table(sprintf('%s/timeseries/bwnames.txt',basedir),
                    header=FALSE)
names(bwcorr.wgcna.t)=modnames
row.names(bwcorr.wgcna.t)=bwnames$V1

pdf(file=sprintf('%s/timeseries/bwmod_wgcna_heatmap.pdf',basedir),
    height=14,width=16)
my_palette <- colorRampPalette(c("blue", "gray","red"))(n = 100)

cellnotes=matrix("",dim(bwcorr.wgcna.p)[1],dim(bwcorr.wgcna.p)[2])
for (i in 1:dim(bwcorr.wgcna.p)[1]) {
  for (j in 1:dim(bwcorr.wgcna.p)[2]) {
    if (bwcorr.wgcna.p[i,j]<0.1) {
      cellnotes[i,j]='+'
    }
  }
}
bwcorr.wgcna.t[bwcorr.wgcna.t > 5]=5
bwcorr.wgcna.t[bwcorr.wgcna.t < -5]=-5

heatmap.2(as.matrix(bwcorr.wgcna.t),margins=c(16,14),key=TRUE,
          trace='none',dendrogram='col', col=my_palette,Rowv='none',
          cellnote=cellnotes,notecol='white',notecex=1.2,density='none',srtCol=45)
          #symm=F,symkey=F,symbreaks=T, scale="none")
dev.off()
