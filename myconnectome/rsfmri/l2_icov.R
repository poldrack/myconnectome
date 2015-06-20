library(rags2ridges)
args <- commandArgs(trailingOnly = TRUE)
subcode=args[1]

subcode='sub014'


basedir='/scratch/projects/UT/poldracklab/poldrack/selftracking/myconnectome/rsfmri/l2icov'

data_orig=read.table(sprintf('/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/combined_data_scrubbed/%s.txt',subcode))
tmask_orig=read.table(sprintf('/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/tmasks/%s.txt',subcode))$V1


# skip first 50 timepoints
tmask=tmask_orig[51:dim(data_orig)[1]]
data_orig=data_orig[51:dim(data_orig)[1],]

data=data_orig[tmask==1,]

o=optPenalty.aLOOCV(as.matrix(data),lambdaMin=0.0001,lambdaMax=1,step=3,graph=FALSE,verbose=TRUE)

cat(sprintf('%s: optLambda %f\n',subcode,o$optLambda))

pcormtx=pcor(o$optPrec)


outfile=sprintf('%s/%s_pcor.txt',basedir,subcode)

write(pcormtx,file=outfile,sep='\t',ncolumns=dim(pcormtx)[1])
