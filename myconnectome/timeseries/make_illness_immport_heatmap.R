# cluster MEs and make surface plot

rnaseq=load_rnaseq_data(varstab_file='/Users/poldrack/Dropbox/data/selftracking/rna-seq/varstab_data_rinregressed.txt',me_file='/Users/poldrack/Dropbox/data/selftracking/rna-seq/WGCNA/MEs-thr8-rinreg-48sess.txt',datefile='/Users/poldrack/Dropbox/data/selftracking/rna-seq/drawdates.txt')
immport=load_ImmPort_data(infile='/Users/poldrack/Dropbox/data/selftracking/rna-seq/ImmPort/ImmPort_eigengenes_rinregressed.txt',datefile='/Users/poldrack/Dropbox/data/selftracking/rna-seq/drawdates.txt')

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

h=heatmap.2(t(as.matrix(immport)),trace='none',dendrogram='row',Colv=FALSE,labCol=day_annot,scale='row',cellnote=max_sym,notecex=2,notecol='black')