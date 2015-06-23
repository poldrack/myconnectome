# make l2-regularized task connectome

basedir='/Users/poldrack/data_unsynced/myconnectome'
taskdata=read.table(sprintf("%s/taskfmri/zstat_parcel_data.txt",basedir),header=FALSE)

library(rags2ridges)
covmtx=covML(as.matrix(taskdata))
taskdata_l2=ridgeS(covmtx,0.0001)
pc=pcor(symm(taskdata_l2))
write.table(pc,sprintf("%s/taskfmri/taskdata_pcorrmtx.txt",basedir),sep='\t',
            col.names=FALSE,row.names=FALSE)