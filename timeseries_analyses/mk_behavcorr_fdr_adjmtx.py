"""
load fdr=corrected results from behav_corr analysis
and create adjacency matrices for each variable

use data file copied from stampede

"""

import os
import numpy

def load_dataframe(filename,thresh=0.1):
	# return p value, t stat, and correlation
	f=open(filename)
	header=f.readline()
	lines=f.readlines()
	f.close()
	data={}
	for l in lines:
		l_s=[i.replace('"','') for i in l.strip().split()]
		try:
		 if float(l_s[-1])<thresh:
			#print l_s
			data[(l_s[1],l_s[2])]=[float(l_s[-1]),float(l_s[4]),float(l_s[3])]
		except:
			pass
	return data


infile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/all_behavcorr_fdr.txt'

try:
	data
	print 'using existing data'
except:
	data=load_dataframe(infile)

all_behav_vars=[k[1] for k in data.keys()]
all_behav_vars=list(set(all_behav_vars))

adjmtx={}
trius={}
triu=numpy.triu_indices(634,1)

for v in all_behav_vars:
	trius[v]=numpy.zeros(triu[0].shape[0])
	adjmtx[v]=numpy.zeros((634,634))
	
for k in data.keys():
	mtxnum=int(k[0][1:])
	v=k[1]
	trius[v][mtxnum]=data[k][2]
	
for v in all_behav_vars:
	adjmtx[v][triu]=trius[v]
	outfile='/Users/poldrack/Dropbox/data/selftracking/rsfmri/behav_adjmtx/%s_adjmtx.txt'%v
	numpy.savetxt(outfile,adjmtx[v])
	print v,numpy.sum(adjmtx[v]>0),numpy.sum(adjmtx[v]<0)
