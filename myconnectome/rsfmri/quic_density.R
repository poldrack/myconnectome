library(QUIC)
args <- commandArgs(trailingOnly = TRUE)
subcode=args[1]
density=args[2]

basedir='/scratch/projects/UT/poldracklab/poldrack/selftracking/myconnectome/rsfmri/quic'

data_orig=read.table(sprintf('/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/combined_data_scrubbed/%s.txt',subcode))
tmask_orig=read.table(sprintf('/scratch/projects/UT/poldracklab/poldrack/selftracking/MRI/tmasks/%s.txt',subcode))$V1

# skip first 50 timepoints
tmask=tmask_orig[51:dim(data_orig)[1]]
data_orig=data_orig[51:dim(data_orig)[1],]

data=data_orig[tmask==1,]

outfile=sprintf('%s/quic_precision_%s/%s_precision.txt',basedir,density,subcode)

datacov=cor(data)

target_density=as.numeric(density)

quicdensity <- function(datacov,x) {
	
		quic.result=QUIC(datacov,x)
		adj=quic.result$X>0
		adj[lower.tri(adj,diag=TRUE)]=0
		vars=list()
		vars$density=sum(adj)/sum(upper.tri(adj))
		vars$quic.result=quic.result
		return(vars)
	
	
	}
	
	
get_best_rho <- function(datacov,path,target_density) {
	
	densities=array(data=0,dim=length(path))

	ctr=1
	for (x in path) {
		densities[ctr]=quicdensity(datacov,x)
		ctr=ctr+1
		}
		
	mindiff=which(densities-target_density ==min(abs(densities-target_density)))
	bestrho=path[mindiff]
	vars=list()
	vars$bestrho=bestrho
	vars$densities=densities
	return(vars)
}

# first get it at 0.5 - should never be less than this
rho=0.5
print(c('start at',rho))
q=quicdensity(datacov,rho)
d=q$density
print(d)

# now do a greedy search
delta=0.5
d_new=d
while (d_new > target_density) {
	rho=rho+delta
	print(c('trying',rho))
	q=quicdensity(datacov,rho)
	d_new=q$density
	print(d_new)
	}

# now backtrack and use a finer grid	
rho=rho-delta
delta=0.1
d_new=1
while (d_new > target_density) {
	rho=rho+delta
	print(c('trying',rho))
	q=quicdensity(datacov,rho)
	d_new=q$density
	print(d_new)
	}

# now backtrack and use an even finer grid	
rho=rho-delta
delta=0.01
d_new=1
while (d_new > target_density) {
	rho=rho+delta
	print(c('trying',rho))
	q=quicdensity(datacov,rho)
	d_new=q$density
	print(d_new)
	}

print(c(subcode,'best rho:',rho))
print(c('density:',d_new))

write(q$quic.result$X,file=outfile,sep='\t',ncolumns=dim(q$quic.result$X)[1])
