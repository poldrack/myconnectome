# some utility functions for processing of myconnectome data
# R Poldrack

require(zoo)

get_x_ts=function(xdata,alldays,scale=TRUE,return_ts=TRUE) {
		xdates=xdata$date
		xdata$date=NULL
		
 		#x=as.numeric(as.character(xdata))
 		if (scale) {
 		  for (i in 1:dim(xdata)[2]) {
 				xdata[,i] = (xdata[,i]- mean(xdata[,i],na.rm=TRUE))/sd(xdata[,i],na.rm=TRUE)
 			}
 		}
 		#x = (x - mean(x,na.rm=TRUE))/sd(x,na.rm=TRUE)
 		x_alldays=matrix(NA,nrow=length(alldays),ncol=dim(xdata)[2])
 		for (d in xdates) {
 			dd=as.Date(d)
 			x_alldays[alldays==dd,] = as.matrix(xdata[xdates==dd,])
 			}
 		if (return_ts) {
 			x=as.ts(zoo(x_alldays,alldays))
 		} else {
 			x=zoo(x_alldays,alldays)
 		}
	
	return(x)
	}
	
get_y_ts= function(ydata,alldays,i,scale=TRUE,return_ts=TRUE) {
		ydates=ydata$date
		ydata$date=NULL
 		y=as.numeric(as.character(ydata[,i]))
 		if (scale) {
 			y = (y - mean(y,na.rm=TRUE))/sd(y,na.rm=TRUE)
 		}
 		y_alldays=array(NA,dim=length(alldays))
 		y_alldays[alldays %in% ydates]=y[ydates %in% alldays]
 		if (return_ts) {
 			y=as.ts(zoo(y_alldays,alldays))
 		} else {
 			y=zoo(y_alldays,alldays)
 		}
		return(y)
	}

get_alldays = function(xdata,ydata,spacing='1 day') {
	dates=c(xdata$date,ydata$date)
	ydates=ydata$date
	xdates=xdata$date
	if (spacing=='1 week') {
		if ( weekdays(as.Date(min(ydates))) == "Tuesday") {
			alldays = seq(min(ydates), max(dates), by=spacing)
     	} else {
		alldays = seq(min(xdates), max(dates), by=spacing)
  		}
	} else {
		alldays = seq(min(dates), max(dates), by=spacing)
	}
	return(alldays)	
}