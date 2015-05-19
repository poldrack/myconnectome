# these functions load the data used for the MyConnectome study

basedir=Sys.getenv('MYCONNECTOME_DIR')


	
load_behav_data = function (infile=sprintf('%s/behavior/trackingdata.txt',basedir)) {
	
	# load behav data
	behav = read.table(infile, na.strings = '.', header=TRUE)
	
	
	# take mean temp
	behav$"temp.mean"=(behav$'weather.temphi'+behav$'weather.templo')/2.0
	
	behav$day_of_week2 = weekdays(as.Date(behav$date))
	# Create indicator that where tu=0 and th = 1
	behav$TuesThurs = rep(NA, length(behav$day_of_week2))
	behav$TuesThurs[behav$day_of_week2 == "Tuesday"] = 0
	behav$TuesThurs[behav$day_of_week2 == "Thursday"] = 1
	# take mean temp
	behav$"temp.mean"=(behav$'weather.temphi'+behav$'weather.templo')/2.0
	
	behav$prevevening.Timespentoutdoors = as.numeric(as.character(behav$prevevening.Timespentoutdoors))
	
  # remove underscores from names of LIWC variables - to prevent latex problems later
	behav$email.LIWCcdi=behav$email.LIWC_CDI
  behav$email.LIWCnegemo=behav$email.LIWC_negemo
	behav$email.LIWCposemo=behav$email.LIWC_posemo
	behav=subset(behav,select=-c(email.LIWC_CDI,email.LIWC_negemo,email.LIWC_posemo))
	
  behav$date=as.Date(behav$date)
	return(behav)

}

	
load_rnaseq_data = function(use_ME=TRUE,limit_ME_to_enriched=FALSE,scale=FALSE,
                            varstab_file=sprintf('%s/rna-seq/varstab_data_prefiltered_rin_3PC_regressed.txt',basedir),
                            me_file=sprintf('%s/rna-seq/WGCNA/MEs-thr8-prefilt-rinPCreg-48sess.txt',basedir),
                            datefile=sprintf('%s/rna-seq/drawdates.txt',basedir),
                            descfile=sprintf('%s/rna-seq/WGCNA/module_descriptions.txt',basedir)) {
	rnaseq.dat.full= read.table(varstab_file, na.strings='.', header=TRUE)
	rna_subcodes=names(rnaseq.dat.full)
	rna_labels=row.names(rnaseq.dat.full)
	
	rnaseq.dat.me = read.table(me_file, na.strings='.', header=TRUE)
	row.names(rnaseq.dat.me)=rna_subcodes
  ordered_MEs=c()
  for  (i in 1:dim(rnaseq.dat.me)[2]) {
    menum=as.integer(gsub('ME','',names(rnaseq.dat.me)[i]))
    if (menum!=0) {ordered_MEs=cbind(ordered_MEs,menum)}
  }
	sorted_idx=sort(ordered_MEs,index.return=TRUE)$ix
  rnaseq.dat.me=subset(rnaseq.dat.me,select=sorted_idx)
	rna_desc=as.character(read.table(descfile,sep='\t',header=FALSE)$V2)
  module_desc=c()
  enriched=c()
  for (i in 1:length(rna_desc)) {
    if (rna_desc[i]!='no enrichment') {enriched=cbind(enriched,i)}
    module_desc=cbind(module_desc,sprintf('%s:%s',names(rnaseq.dat.me)[i],rna_desc[i]))
  }
  names(rnaseq.dat.me)=module_desc
  if (limit_ME_to_enriched==TRUE) {
    rnaseq.dat.me=subset(rnaseq.dat.me,select=sort(enriched))
  }
	
	if (use_ME) {
		rnaseq.dat=rnaseq.dat.me
		}  else {
		rnaseq.dat=as.data.frame(t(rnaseq.dat.full))
		}
	
	rna_labels=names(rnaseq.dat)
	if (scale) {
		rnaseq.dat=as.data.frame(scale(rnaseq.dat,scale=FALSE))
		names(rnaseq.dat)=rna_labels
	}
	# scale removes labels, so put them back
	d=read.table(datefile)
	rnaseq.dat$date=as.Date(d$V1,'%m/%d/%Y')
	return(rnaseq.dat)

}
	
load_ImmPort_data = function(datefile=sprintf('%s/rna-seq/drawdates.txt',basedir),
                             infile=sprintf('%s/rna-seq/ImmPort/ImmPort_eigengenes_prefilt_rin3PCreg.txt',basedir)) {
	clusterdata.dat= as.data.frame(t(read.table(infile, na.strings='.', header=FALSE,row.names=1)))

	d=read.table(datefile)
	clusterdata.dat$date=as.Date(d$V1,'%m/%d/%Y')
	return(clusterdata.dat)
	}

load_rsfmri_subcodes=function(infile=sprintf('%s/subcodes.txt',basedir)) {
  sc=read.table(infile,header=FALSE)$V1
  return(sc)
}
load_rnaseq_subcodes=function(infile=sprintf('%s/rna-seq/rnaseq-subcodes.txt',basedir)) {
  sc=read.table(infile,header=FALSE)$V1
  return(sc)
}
load_rnaseq_drawdates=function(infile=sprintf('%s/rna-seq/drawdates.txt',basedir)) {
  d=read.table(infile,header=FALSE)$V1
  dates=as.Date(d,'%m/%d/%Y')
  return(dates)
}

# use pre-made cluster description files because these must be done by hand
load_metab_data = function(use_clustered_data=TRUE,
                           clust_file=sprintf('%s/metabolomics/apclust_eigenconcentrations.txt',basedir),
                           exclude_unenriched=FALSE,
                           clust_desc_file='http://s3.amazonaws.com/openfmri/ds031/metabolomics/apclust_descriptions.txt',
                           logtransform=TRUE,exclude_unnamed=TRUE,
                           infile=sprintf('%s/metabolomics/metabolomics.txt',basedir),
                           labelfile=sprintf('%s/metabolomics/metabolomics_labels.txt',basedir)) {
	
	if (use_clustered_data) {
    logtransform=FALSE  # because they were already transformed
		labels=read.table(clust_desc_file,header=FALSE,sep='\t')$V1
		metab.dat=read.table(clust_file)
		names(metab.dat)=as.character(labels)
		if (exclude_unenriched) {
			# exclude those with FDR p>0.1
			metab.dat=subset(metab.dat,select=-c(1,3,6,7,12,14,15))
			}
		} else {
		metab.dat=read.table(infile, na.strings='.', header=FALSE)
		metab.labels=read.table(labelfile, sep='\t',na.strings='.', header=FALSE)
		metab.labels=as.character(metab.labels$V1)
		for (i in 1:length(metab.labels)) {
			metab.labels[i]=gsub(' ','_',metab.labels[i])
			}
		if (exclude_unnamed) {
			metab.dat=metab.dat[,1:106]
			}
		if (logtransform) {# NB: log-transform the metabolomics data
			metab.dat=log(metab.dat)
			}
		if (exclude_unnamed) {
			names(metab.dat)=as.character(metab.labels[1:106])
			} else {
			names(metab.dat)=as.character(metab.labels)
		}
	}
	
	metab.dat$date=load_rnaseq_drawdates()

	row.names(metab.dat)=load_rnaseq_subcodes()

	return(metab.dat)	
	}


load_food_data = function(infile=sprintf('%s/behavior/food_data.txt',basedir)) {
	# laod behav data to get dates
	behav=load_behav_data()
	
	food = read.table(infile, na.strings = '.', header=TRUE)
	food$date=behav$date[behav$subcode %in% food$subcode]

	# combine olive oil and vinegar as they are perfectly correlated
	food$olive_oil_and_vinegar=behav$olive_oil
	food$olive_oil=NULL
	food$vinegar=NULL
	return(food)
	}
	
load_fd_data=function(fdfile=sprintf('%s/rsfmri/mean_fd.txt',basedir)) {
	behav=load_behav_data()
	subcodes=load_rsfmri_subcodes()
	dates=behav$date[behav$subcode %in% subcodes]
	fd=read.table(fdfile,header=FALSE)
	fd$date=dates
	return(fd)
	
	}
	
	
load_fmri_data = function (type='wincorr') {

source('../config.R')
# laod behav data to get dates
behav=load_behav_data()

subcodes=load_rsfmri_subcodes()

dates=behav$date[behav$subcode %in% subcodes]

if (type=='wincorr') {
	fmridatafile=sprintf("%s/rsfmri/module_within_corr.txt",basedir)
	network_names=c('1:Default','2:Visual_2','3:Fronto_Parietal','4.5:Visual_1','5:Dorsal_Attention',
                  '7:Ventral_Attention','8:Salience','9:Cingulo_opercular',
                  '10:Somatomotor','11.5:Fronto_Parietal_2','15:Medial_Parietal',
                  '16:Parieto_Occipital')
  } else if (type=='bwcorr') {
    fmridatafile=sprintf("%s/rsfmri/module_between_corr.txt",basedir)
    namelist=read.table(sprintf('%s/rsfmri/bwmod_corr_labels.txt',basedir),
      sep='\t',header=FALSE)
    network_names=c()
    for (i in 1:dim(namelist)[1]) {
      network_names=rbind(network_names,sprintf("%s-%s",as.character(namelist[i,1]),as.character(namelist[i,2])))
    }
    }	
  else {stop(sprintf('data type %s not found',type))}

data = read.table(fmridatafile, na.strings='.', header=FALSE)

names(data)=network_names
data$date=dates

	return(data)
	}
	
load_network_data=function() {
  source("../config.R")
	behav=load_behav_data()
  modularity=read.table(sprintf('%s/rsfmri/modularity_weighted_louvain_bct.txt',basedir))
  efficiency=read.table(sprintf('%s/rsfmri/geff_pos.txt',basedir))
	subcodes=load_rsfmri_subcodes()
	dates=behav$date[behav$subcode %in% subcodes]
  datamat=cbind(modularity,efficiency)
  names(datamat)=c('modularity_weighted','efficiency_weighted')
	row.names(datamat)=subcodes
	datamat$date=dates
	return(datamat)
	

	}

load_participation_index=function(infile=sprintf('%s/rsfmri/PIpos_weighted_louvain_bct.txt',basedir)){
  behav=load_behav_data()
  datamat=as.data.frame(t(read.table(infile,header=FALSE)))
  subcodes=load_rsfmri_subcodes()
  dates=behav$date[behav$subcode %in% subcodes]
  row.names(datamat)=subcodes
  datamat$date=dates
  return(datamat)
}

