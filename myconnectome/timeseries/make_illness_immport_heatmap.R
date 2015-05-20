# cluster MEs and make surface plot
source('http://s3.amazonaws.com/openfmri/ds031/timeseries_analyses/load_myconnectome_data.R')

rnaseq=load_rnaseq_data()
immport=load_ImmPort_data()

dates=immport$date
rnaseq$date=NULL
immport$date=NULL

library(gplots)

day_annot=as.character(read.table('/Users/poldrack/code/selftracking/analysis_metadata/health_by_drawdates.txt')$V1)
day_annot[day_annot=='none']=''

max_sym=c()

for (i in 1:dim(immport)[2]) {
    mv=which(immport[,i]==max(immport[,i]))
    m=array('',dim=dim(immport)[1])
    m[mv]='*'
    max_sym=rbind(max_sym,m)
}

pdf('/Users/poldrack/Dropbox/Documents/Papers/SelfTracking/figures/illness_expression_heatmap.pdf')
h=heatmap.2(t(as.matrix(immport)),trace='none',dendrogram='row',Colv=FALSE,labCol=day_annot,scale='row',cellnote=max_sym,notecex=2,notecol='black')
dev.off()
