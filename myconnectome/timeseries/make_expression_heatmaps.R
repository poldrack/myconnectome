# cluster networks and netdat measures based on their genetic associations

basedir=Sys.getenv('MYCONNECTOME_DIR')
basedir='/Users/poldrack/data_unsynced/myconnectome'

source('/Users/poldrack/code/myconnectome/myconnectome/timeseries/load_myconnectome_data.R')
wincorr=load_fmri_data('wincorr')
wincorr$date=NULL
rnaseq_wgcna=load_rnaseq_data()
rnaseq_wgcna$date=NULL
OUTPUT_DIR='/Users/poldrack/Dropbox/Documents/Papers/SelfTracking/figures'
if (!exists('OUTPUT_DIR')) {
	print('To save results to a specific directory, set OUTPUT_DIR variable to target directory')
	OUTPUT_DIR=NULL 
} else{
	print(c('Saving results to:',OUTPUT_DIR))
}
	
if (is.null(OUTPUT_DIR)) {
	OUTPUT_DIR='.'
	print('saving output to current directory')
	}

wincorr.wgcna=read.table('/Users/poldrack/data_unsynced/myconnectome/timeseries/out.dat.wgcna_wincorr.txt')
cluster_terms=as.character(read.table('/Users/poldrack/Dropbox/data/selftracking/rna-seq/WGCNA/module_descriptions.txt',header=FALSE,sep='\t')$V2)

data=matrix(data=0,nrow= dim(rnaseq_wgcna)[2],ncol=12)
pval=matrix(data=0,nrow= dim(rnaseq_wgcna)[2],ncol=12)

for (geneclust in 1:dim(rnaseq_wgcna)[2]) {
	for (network in 1:12) {
		idx=(geneclust-1)*12 + network
		data[geneclust,network]=wincorr.wgcna[idx,4]
		pval[geneclust,network]=wincorr.wgcna[idx,11]  # bh corrected
	}
	}


library(gplots)
labels=c('Default','Visual-II','FrontoParietal','Visual-I','DorsalAttn','VentralAttn','Salience','CinguloOpercular','Somatomotor','FrontoParietal-II','MedialParietal','ParietoOccipital')

wardclust=function(d) {
	hclust(d,method='ward')
	}
corrdist=function(d) {
	c=1 - cor(t(d))
	return(as.dist(c))
	}

# make pvalue symbols
thresh=0.1
pval_marks=matrix(data='',dim(data)[1],dim(data)[2])
marksize=matrix(data=0,dim(data)[1],dim(data)[2])
for (i in 1:dim(data)[1]) {
  for (j in 1:dim(data)[2]) {
    if (pval[i,j] < thresh) {
      pval_marks[i,j]='*'
      if (pval[i,j] < 0.1) {pval_marks[i,j]='-'}
      if (pval[i,j] < 0.05) {pval_marks[i,j]='+'}
      if (pval[i,j] < 0.01) {pval_marks[i,j]='*'}
    }
  }
}


pdf(file=paste(OUTPUT_DIR,'wincorr_expression_heatmap.pdf',sep='/'),width=16,height=10)
hm=heatmap.2(t(data),dendrogram='both',scale='none',trace='none',
             labRow=labels,labCol=cluster_terms,margins=c(16,10),key=FALSE,
             cellnote=t(pval_marks),notecol='black',notecex=1.5)
#dev.copy(pdf,paste(OUTPUT_DIR,'wincorr_expression_heatmap.pdf',sep='/'))
dev.off()

