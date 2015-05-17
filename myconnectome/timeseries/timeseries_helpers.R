# helper functions for timeseries analyses

require(knitr)
source('../config.R')

kable_latex = function(data,varname,tabledir=sprintf('%s/timeseries/tables',basedir)) {
  if (nrow(data) > 30) {lt=TRUE} else {lt=FALSE}
  k=kable(data,format='latex',longtable=lt,digits=3,row.names=FALSE)
  write(k,file=sprintf('%s/%s_timeseries_stats.tex',tabledir,varname))
}

kable_wrap = function(data,fdr_thresh=thresh) {
  data = data[data$pval_bh<=fdr_thresh,]
  if (nrow(data)>0) {kable(data)} else {print('no significant results')}
}

output_results=function(d,vnames,fdr_thresh=thresh,save_latex=TRUE,save_table=TRUE,OUTPUT_DIR='/tmp') {
  vname=sprintf('%s_%s',vnames[1],vnames[2])
  ds=d[d$pval_bh<=fdr_thresh,]
  ds=subset(ds,select=c(xvar,yvar,cor.val,t.arima,pval_bh,nobs))
  names(ds)=c(sprintf("X:%s",vnames[1]),sprintf("Y:%s",vnames[2]),'r','t','p (BH)','N')
  if (save_table) {
    write.table(d,file=paste(OUTPUT_DIR,sprintf('out.dat.%s.txt',vname),sep='/'))
  }
  if (save_latex) {
    kable_latex(ds,vname)
  }
}
