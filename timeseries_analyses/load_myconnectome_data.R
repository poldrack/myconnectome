# these functions load the data used for the MyConnectome study


test_load_myconnectome_data = function() {
	# test loading of all data
	# check sums of numeric variables, allowing for some rounding error
	
	print("This tool requires installation of the R.cache package")
	
	require(R.cache)
	
	print("testing all variables against stored checksums, this will take a few moments...")
	print("you can safely ignore warnings about NAs induced by coercion...")
	
    print('testing behavioral data...')
	behav=load_behav_data()
	stopifnot(getChecksum(behav)=="1c26494a2a3da1ac3e00f6a5704b03d4")

    print('testing diary data...')
	diary_data=load_diary_data()
	stopifnot(getChecksum(diary_data)=="2a04da4ac8a0fc6e422e155590a5fe09")
	
    print('testing rnaseq data...')
	rnaseq_data=load_rnaseq_data()
	stopifnot(getChecksum(rnaseq_data)=="9807743db2afa5ce23a432bb30184ba5")
	
    print('testing immport data...')
	immport=load_ImmPort_data()
	stopifnot(getChecksum(immport)=="df979f524c61337058adbff3bdd03d3e")
	
    print('testing metab data...')
	metab=load_metab_data()
	stopifnot( getChecksum(metab) == "eb309f07afca9d0d2a633cdc18b0ce19")
	
    print('testing food data...')
	food=load_food_data()
	stopifnot(getChecksum(food) == "57ecfbdaf43cb586bf653345e18cd28d")
	
    print('testing fd data...')
	fd=load_fd_data()
	stopifnot(getChecksum(fd) == "bc5139aa411e9d2cb7d649f5b01af985")
	
    print('testing wincorr data...')
	wincorr=load_fmri_data('wincorr')
	stopifnot(getChecksum(wincorr) == "29bc5e23e47b46285900a2a1909a8cff")


	print('All checksums confirmed')
	
	}
	
load_behav_data = function (infile="http://s3.amazonaws.com/openfmri/ds031/behavior/trackingdata.txt") {
	
	# load behav data
	behav = read.table(infile, na.strings = '.', header=TRUE)
	
	
	# take mean temp
	behav$"temp.mean"=(behav$'weather.temphi'+behav$'weather.templo')/2.0
	
	behav$day_of_week2 = weekdays(as.Date(behav$date))
	# Create indicator that where tu=0 and th = 1
	behav$tu_th = rep(NA, length(behav$day_of_week2))
	behav$tu_th[behav$day_of_week2 == "Tuesday"] = 0
	behav$tu_th[behav$day_of_week2 == "Thursday"] = 1
	# take mean temp
	behav$"temp.mean"=(behav$'weather.temphi'+behav$'weather.templo')/2.0
	
	behav$prevevening.Timespentoutdoors = as.numeric(as.character(behav$prevevening.Timespentoutdoors))
	
	behav$date=as.Date(behav$date)
	return(behav)

}

load_diary_data=function(infile='http://s3.amazonaws.com/openfmri/ds031/diary/term_date.txt',goodvars=c('allergy','exercise')) {
	termdata=read.table(infile,header=FALSE)
	dates=read.table('http://s3.amazonaws.com/openfmri/ds031/diary/diary_dates.txt')$V1
	terms=as.character(read.table('http://s3.amazonaws.com/openfmri/ds031/diary/diary_terms.txt')$V1)
	names(termdata)=terms
	termdata=subset(termdata,select=goodvars)
	termdata$date=as.Date(dates)
	# remove obvious useless terms
	return(termdata)
	
	}
	
	
load_rnaseq_data = function(use_ME=TRUE,limit_ME_to_enriched=FALSE,scale=FALSE,varstab_file='http://s3.amazonaws.com/openfmri/ds031/RNA-seq/varstab_data_rinregressed.txt',me_file='http://s3.amazonaws.com/openfmri/ds031/RNA-seq/MEs-thr8-rinreg-48sess.txt',datefile='http://s3.amazonaws.com/openfmri/ds031/RNA-seq/drawdates.txt') {
	rnaseq.dat.full= read.table(varstab_file, na.strings='.', header=TRUE)
	rna_subcodes=names(rnaseq.dat.full)
	rna_labels=row.names(rnaseq.dat.full)
	
	rnaseq.dat.me = read.table(me_file, na.strings='.', header=TRUE)
	row.names(rnaseq.dat.me)=rna_subcodes
	# these are the modules that are not enriched for at least one pathway at benjamini p < 0.1
	unenriched=c('ME3','ME6','ME8','ME9','ME10','ME15','ME16','ME17','ME19','ME20','ME23','ME24','ME25','ME26','ME27','ME28','ME31','ME32','ME36','ME38')
	MEsubset=c()
	for (i in 1:38) {
		MEname=sprintf('ME%d',i)
		if (limit_ME_to_enriched)  {
			if (!(MEname %in% unenriched)) {
				MEsubset=c(MEsubset,MEname)
				}
			} else {
				MEsubset=c(MEsubset,MEname)
		
				}
		}
	rnaseq.dat.me=subset(rnaseq.dat.me,select=MEsubset)
	
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
	
load_ImmPort_data = function(datefile='http://s3.amazonaws.com/openfmri/ds031/RNA-seq/drawdates.txt',infile='http://s3.amazonaws.com/openfmri/ds031/RNA-seq/ImmPort_eigengenes_rinregressed.txt') {
	clusterdata.dat= as.data.frame(t(read.table(infile, na.strings='.', header=FALSE,row.names=1)))

	d=read.table(datefile)
	clusterdata.dat$date=as.Date(d$V1,'%m/%d/%Y')
	return(clusterdata.dat)
	}

load_metab_data = function(use_clustered_data=TRUE,clust_file='http://s3.amazonaws.com/openfmri/ds031/metabolomics/apclust_eigenconcentrations.txt',exclude_unenriched=TRUE,clust_desc_file='http://s3.amazonaws.com/openfmri/ds031/metabolomics/apclust_descriptions.txt',logtransform=TRUE,exclude_unnamed=TRUE,infile='http://s3.amazonaws.com/openfmri/ds031/metabolomics/metabolomics.txt',labelfile='http://s3.amazonaws.com/openfmri/ds031/metabolomics/metabolomics_labels.txt',datefile='http://s3.amazonaws.com/openfmri/ds031/RNA-seq/drawdates.txt',subcodes='http://s3.amazonaws.com/openfmri/ds031/RNA-seq/pathsubs.txt') {
	
	if (use_clustered_data) {
		labels=read.table(clust_desc_file,header=FALSE,sep='\t')$V1
		metab.dat=read.table(clust_file)
		names(metab.dat)=as.character(labels)
		if (exclude_unenriched) {
			# exclude those with FDR p<0.1
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
	
	d=read.table(datefile)
	metab.dat$date=as.Date(d$V1,'%m/%d/%Y')

	row.names(metab.dat)=read.table(subcodes)$V1

	return(metab.dat)	
	}


load_food_data = function() {
	# laod behav data to get dates
	behav=load_behav_data()
	
	food = read.table("http://s3.amazonaws.com/openfmri/ds031/behavior/food_data.txt", na.strings = '.', header=TRUE)
	food$date=behav$date[behav$subcode %in% food$subcode]

	# combine olive oil and vinegar as they are perfectly correlated
	food$olive_oil_and_vinegar=behav$olive_oil
	food$olive_oil=NULL
	food$vinegar=NULL
	return(food)
	}
	
load_fd_data=function() {
	behav=load_behav_data()
	subcodes=read.table("http://s3.amazonaws.com/openfmri/ds031/rsfmri/subcodes.txt",header=FALSE)
	dates=behav$date[behav$subcode %in% subcodes$V1]
	fd=read.table('http://s3.amazonaws.com/openfmri/ds031/rsfmri/mean_fd.txt',header=FALSE)
	fd$date=dates
	return(fd)
	
	}
	
load_autocorr_data = function(infile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/autocorr_data.txt') {
	# laod behav data to get dates
	behav=load_behav_data()
	subcodes=read.table("http://s3.amazonaws.com/openfmri/ds031/rsfmri/subcodes.txt",header=FALSE)
	dates=behav$date[behav$subcode %in% subcodes$V1]
	data = read.table(infile)
	data$date=dates
	return(data)
	}
	
load_fmri_data = function (type='wincorr',log_winvar=TRUE) {
	
# laod behav data to get dates
behav=load_behav_data()

subcodes=read.table("http://s3.amazonaws.com/openfmri/ds031/rsfmri/subcodes.txt",header=FALSE)
dates=behav$date[behav$subcode %in% subcodes$V1]

if (type=='wincorr') {
	fmridatafile="http://s3.amazonaws.com/openfmri/ds031/rsfmri/module_within_corr.txt"
	network_names=c('1_Default','2_Second_Visual','3_Frontal-Parietal','4.5_First_Visual_V1plus','5_First_Dorsal_Attention','6_Second_Dorsal_Attention','7_Ventral_Attention-Language','8_Salience','9_Cingulo-opercular','10_Somatomotor','11.5_Frontal-Parietal_Other','15_Parietal_Episodic_Retrieval','16_Parieto-Occipital')
  } else if (type=='bwcorr') {
    fmridatafile="http://s3.amazonaws.com/openfmri/ds031/rsfmri/module_between_corr.txt"
    network_names=as.character(read.table("http://s3.amazonaws.com/openfmri/ds031/rsfmri/bwmod_corr_labels_joined.txt",sep='\t',header=FALSE)$V1)
    }else if (type == 'winvar') {
  	fmridatafile="http://s3.amazonaws.com/openfmri/ds031/rsfmri/network_variance_allses_fixed.txt"
  	network_names=c('1_Default','2_Second_Visual','3_Frontal-Parietal','4.5_First_Visual_V1plus','5_First_Dorsal_Attention','6_Second_Dorsal_Attention','7_Ventral_Attention-Language','8_Salience','9_Cingulo-opercular','10_Somatomotor','11.5_Frontal-Parietal_Other','15_Parietal_Episodic_Retrieval','16_Parieto-Occipital')
  	} else {
	fmridatafile="http://s3.amazonaws.com/openfmri/ds031/rsfmri/module_falff.txt"
	network_names=c('1_Default','2_Second_Visual','3_Frontal-Parietal','4.5_First_Visual_V1plus','5_First_Dorsal_Attention','6_Second_Dorsal_Attention','7_Ventral_Attention-Language','8_Salience','9_Cingulo-opercular','10_Somatomotor','11.5_Frontal-Parietal_Other','15_Parietal_Episodic_Retrieval','16_Parieto-Occipital')
	} 		

data = read.table(fmridatafile, na.strings='.', header=FALSE)
if (type == 'winvar' & log_winvar==TRUE) {
	data=log(data)
}

names(data)=network_names
data$date=dates

	return(data)
	}
	
load_network_data=function(mean_over_thresh=FALSE) {
	behav=load_behav_data()
	data=read.table('http://s3.amazonaws.com/openfmri/ds031/rsfmri/netstats_all.txt',header=TRUE)
	if (mean_over_thresh) {
		vars=c('EFFg','EFFl','Clust','modularity_infomap',
		  "modularity_multi","PowerExp","RCC",
		  "mean_cc","mean_bc","mean_pi","gcsize","APL")
		  meandata=matrix(data=0,nrow=dim(data)[1],ncol=length(vars))
		  for (measure in 1:length(vars)) {
				d=subset(data,select=seq(measure,60,12))
				meandata[,measure]=apply(d,1,mean)
			
			}
		data=as.data.frame(meandata)
		names(data)=vars
		data$MOD=(data$modularity_infomap + data$modularity_multi)/2.0
		data$modularity_infomap=NULL
		data$modularity_multi=NULL
		data$mean_pi=NULL
		data$mean_cc=NULL
		data$mean_bc=NULL
		data$gcsize=NULL
		}
	subcodes=read.table("http://s3.amazonaws.com/openfmri/ds031/rsfmri/subcodes.txt",header=FALSE)
	dates=behav$date[behav$subcode %in% subcodes$V1]
	row.names(data)=subcodes$V1
	data$date=dates
	return(data)
	

	}
