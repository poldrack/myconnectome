# by Jeanette Mumford
# uses auto.arima to model behavioral variables against rsfmri data

library(forecast)

##############  Functions ###############
# From: https://stat.ethz.ch/pipermail/r-help/2009-June/202173.html

cwp = function (object){
#
# cwp <--> ``coefficients with p-values''
#
     coef <- coef(object)
     if (length(coef) > 0) {
         mask <- object$mask
         sdev <- sqrt(diag(vcov(object)))
         t.rat <- rep(NA, length(mask))
         t.rat[mask] <- coef[mask]/sdev
         pt <- 2 * pnorm(-abs(t.rat))
         setmp <- rep(NA, length(mask))
         setmp[mask] <- sdev
         sum <- rbind(coef, setmp, t.rat, pt)
         dimnames(sum) <- list(c("coef", "s.e.", "t ratio", "p-value"),
             names(coef))
         return(sum)
     } else return(NA)
}

print_corr_results=function(out,thresh=0.07) {
	print('xvar  yvar r pval-FDRcorr')
for (i in 1:dim(out)[1]) {
	if (is.nan(out$pval_bh[i]) | is.na(out$pval_bh[i])) {
		print('found a nan')
		}
	else if (out$pval_bh[i]<thresh) {
			print(sprintf('%s %s %f %f',out$xvar[i],out$yvar[i],out$cor.val[i], out$pval_bh[i]))
		}
	}
}

#ydata=rnaseq.dat
#xdata=behav
# by RP
est_bivariate_arima_model = function (xdata,ydata,xvars=c(NA),spacing='1 day',verbose=FALSE,skip_ident=FALSE) {
#
# estimate arima model for all combinations of two sets of variables
# xdata: x variable (must have date field)
# ydata: dependent variable (must have date field)
# datadays: dates for samples
# spacing: spacing of time series - will be 1 week for RNA/metab, 1 day for fMRI
#

dates=c(xdata$date,ydata$date)
xdates=xdata$date
ydates=ydata$date
xdata$subcode=NULL
ydata$subcode=NULL

# if we are using rna-seq data then we need to specify 1-week spacing
# since data are only collected on tuesdays, which causes the program 
# to fail if 1 day sampling interval is specified
# - in this case, we need to find which one is a tuesday

if (spacing=='1 week') {
	if ( weekdays(as.Date(min(ydates))) == "Tuesday") {
		alldays = seq(min(ydates), max(dates), by=spacing)
     } else {
	alldays = seq(min(xdates), max(dates), by=spacing)
  }
} else {
	alldays = seq(min(dates), max(dates), by=spacing)
	}

xdata$date=NULL
ydata$date=NULL
	
if (!is.na(xvars[1])) {
	print('using subset of variables:')
	print(xvars)
	xdata=xdata[,xvars]
}
xnames=names(xdata)
ynames=names(ydata)
if (verbose) {
	print(xnames)
	print(ynames)
}
out=c()
for (i in 1:dim(ydata)[2])    {
 	print(i)
 	for (j in 1:dim(xdata)[2]) { 
 		if (skip_ident & i==j) 
 			next
 		print(sprintf('%s %s',xnames[j],ynames[i]))
 		x=as.numeric(as.character(xdata[,j]))
 		x = (x - mean(x,na.rm=TRUE))/sd(x,na.rm=TRUE)
 		x_alldays=array(NA,dim=length(alldays))
 		x_alldays[alldays %in% xdates]=x[xdates %in% alldays]
 		x=as.ts(zoo(x_alldays,alldays))
 		
 		y_alldays=array(NA,dim=length(alldays))
 		y_alldays[alldays %in% ydates]=ydata[ydates %in% alldays,i]
 		y=as.ts(zoo(y_alldays, alldays))
 		
 		fit.loop = auto.arima(y, xreg = x)
        p.vals = data.frame(cwp(fit.loop))
        if (verbose) {
        	print(cwp(fit.loop))
        	print(fit.loop$arma)
		}
        covariate.loc = which(names(p.vals) == "x")
               # you may need to edit that string in the above command
              # just type names(p.vals) and copy and paste it in here
        drift.loc = which(names(p.vals) == "drift")
 	     corrval = cor.test(x, y)$estimate
 	     if (length(covariate.loc) == 1) {
 	     	p.arima = p.vals[4,covariate.loc]
 	     	t.arima=p.vals[3,covariate.loc]
 	     } else {
 	     	p.arima=1
 	     	t.arima=0
 	     } 
 	     if (length(drift.loc) == 1) {
 	     	p.drift = p.vals[4,drift.loc]
 	     	t.drift = p.vals[3,drift.loc]
 	     } else {
 	     	p.drift=1
 	     	t.drift=0
 	     } 
 	     dat.loop = c(xnames[j], ynames[i], corrval,t.arima,p.arima,t.drift,p.drift,fit.loop$arma[1:5])
 	     out = rbind(out, dat.loop)
 	     
      }
}

out.dat = data.frame(out)
# AR, MA, seasonal AR and seasonal MA coefficients, plus the period and the number of non-seasonal and seasonal differences.
names(out.dat)= c("xvar", "yvar", "cor.val","t.arima","arima.p","t.drift","drift.p","AR",'MA','sAR','sMA','period') 		
out.dat$arima.p = as.numeric(as.character(out.dat$arima.p))
out.dat$t.arima = as.numeric(as.character(out.dat$t.arima))
out.dat$drift.p = as.numeric(as.character(out.dat$drift.p))
out.dat$t.drift = as.numeric(as.character(out.dat$t.drift))
out.dat$cor.val = as.numeric(as.character(out.dat$cor.val))
pval_bh=p.adjust(out.dat[,5],method='BH')
out.dat$pval_bh=pval_bh
out.dat[,1]=as.character(out.dat[,1])
out.dat[,2]=as.character(out.dat[,2])
for (var in 3:dim(out.dat)[2]) {
	out.dat[,var]=as.numeric(out.dat[,var])
	}
return(out.dat)
}

