import numpy
import os

exprdata=numpy.loadtxt('/Users/poldrack/Dropbox/data/selftracking/rna-seq/WGCNA/cluster_eigengenes_GOBS.txt')
exprdata=exprdata[:,1:]

f=open('/Users/poldrack/Dropbox/data/connectome-genome/transcripts/subcodes_common.txt')
subcodes=[i.strip() for i in f.readlines()]
f.close()

fd_demog=numpy.loadtxt('/Users/poldrack/Dropbox/data/connectome-genome/transcripts/fd_common.txt')


f=open('/Users/poldrack/Dropbox/data/selftracking/rna-seq/WGCNA/GOBS_nofix_wincorr_expression_solar.txt','w')
wincorr_names=['WC%d'%i for i in range(1,13)]
me_names=['ME%d'%int(i+1) for i in range(exprdata.shape[0])]
nuisance_names=['fd','age','sex']

header=['ID']+nuisance_names+wincorr_names+me_names

f.write('%s\n'%','.join(header))

for i in range(len(subcodes)):
    wincorr=numpy.loadtxt(os.path.join('/Users/poldrack/Dropbox/data/connectome-genome/winmod_corr_data','%s.txt'%subcodes[i]))
    data=[subcodes[i]] + ['%f'%x for x in fd_demog[i,:]] +  ['%f'%x for x in wincorr] +  ['%f'%x for x in exprdata[:,i]]
    f.write('%s\n'%','.join(data))

f.close()
