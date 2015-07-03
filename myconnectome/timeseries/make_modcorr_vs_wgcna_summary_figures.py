# -*- coding: utf-8 -*-
"""
make summary figures for within/between network connectivity vs expression
- ultimately this was not used for the figures, but was used to make the 
inputs to the R program used for the figures (mk_bwcorr_expression_figure.R)
Created on Sun Jun 21 18:03:58 2015

@author: poldrack
"""

import os
import numpy
from myconnectome.utils.load_dataframe import load_dataframe
import matplotlib.pyplot as plt
import matplotlib

basedir=os.environ['MYCONNECTOME_DIR']

wincorr_df=load_dataframe(os.path.join(basedir,'timeseries/out.dat.wgcna_wincorr.txt'),thresh=1.0)
netnames=['DMN','V2','FP1','V1','DA','VA','Sal','CO','SM','FP2','MPar','ParOcc']
netidx={1:0,2:1,3:2,4.5:3,5:4,7:5,8:6,9:7,10:8,11.5:9,15:10,16:11}

f=open(os.path.join(basedir,'timeseries/netnames.txt'),'w')
for i in netnames:
    f.write(i+'\n')
f.close()

wincorr_fdrp=numpy.zeros((12,63))
wincorr_t=numpy.zeros((12,63))

for k in wincorr_df.iterkeys():
    me_num=int(k[0].split(':')[0].replace('ME',''))
    net_num=float(k[1].split(':')[0])
    wincorr_fdrp[netidx[net_num],me_num-1]=wincorr_df[k][0]
    wincorr_t[netidx[net_num],me_num-1]=wincorr_df[k][1]
numpy.savetxt(os.path.join(basedir,'timeseries/wincorr_wgcna_t.txt'),wincorr_t)    
numpy.savetxt(os.path.join(basedir,'timeseries/wincorr_wgcna_fdrp.txt'),wincorr_fdrp)    

bwcorr_fdrp=numpy.zeros((66,63))
bwcorr_t=numpy.zeros((66,63))

bwcorr_df=load_dataframe(os.path.join(basedir,'timeseries/out.dat.wgcna_bwcorr.txt'),thresh=1.0)
allbwkeys={}
bwkeys=bwcorr_df.keys()

for k in bwkeys:
    nets=k[1].split('-')
    netnums=[0,0]
    for i in range(2):
        netnums[i]=netidx[float(nets[i].split('_')[0])]
    allbwkeys[k[1]]=netnums

allbwnetnums={}
ctr=0
for i in range(12):
    for j in range(i+1,12):
        allbwnetnums[(i,j)]=ctr
        ctr+=1
        
for k in bwcorr_df.iterkeys():
    me_num=int(k[0].split(':')[0].replace('ME',''))
    net_num=allbwnetnums[allbwkeys[k[1]][0],allbwkeys[k[1]][1]]
    bwcorr_fdrp[net_num,me_num-1]=bwcorr_df[k][0]
    bwcorr_t[net_num,me_num-1]=bwcorr_df[k][1]
numpy.savetxt(os.path.join(basedir,'timeseries/bwcorr_wgcna_t.txt'),bwcorr_t)    
numpy.savetxt(os.path.join(basedir,'timeseries/bwcorr_wgcna_fdrp.txt'),bwcorr_fdrp)    

matplotlib.rcParams['xtick.major.size'] = 0
matplotlib.rcParams['xtick.minor.size'] = 0
matplotlib.rcParams['ytick.major.size'] = 0
matplotlib.rcParams['ytick.minor.size'] = 0


bwnames=[]
for i in range(len(netnames)):
    for j in range(i,len(netnames)):
        if not i==j:
            bwnames.append(netnames[i]+'-'+netnames[j])
f=open(os.path.join(basedir,'timeseries/bwnames.txt'),'w')
for i in bwnames:
    f.write(i+'\n')
f.close()

ticklocs=numpy.arange(0,66,1)

plt.figure(figsize=[12,14])
plt.imshow(bwcorr_t,interpolation='nearest',aspect='auto')
plt.yticks(ticklocs,bwnames)
#for i in range(bwcorr_t.shape[0]):
#    if bwcorr_[i]<0.1:
#        plt.text(85,ticklocs[i]+0.25,'L',fontsize=14)
#    if bwcorr_stats[i,3]<0.1:
#        plt.text(86,ticklocs[i]+0.25,'P',fontsize=14)
#plt.xticks(range(0,84,9),[dates[i] for i in range(0,84,9)],rotation=45)
plt.colorbar(shrink=0.6)
plt.savefig(os.path.join(basedir,'timeseries/bwcorr_wgcna_heatmap.pdf'))
asdf


ticklocs=numpy.arange(0,12,1)
plt.figure(figsize=[12,5])
plt.imshow(wincorr[0].T,interpolation='nearest',aspect='auto')
plt.yticks(ticklocs,netnames,fontsize=18)
for i in range(wincorr_stats.shape[0]):
    if wincorr_stats[i,2]<0.1:
        plt.text(85,ticklocs[i]+0.1,'L',fontsize=16)
    if wincorr_stats[i,3]<0.1:
        plt.text(86,ticklocs[i]+0.1,'P',fontsize=16)
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom='off',      # ticks along the bottom edge are off
        top='off',         # ticks along the top edge are off
        labelbottom='off') # labels along the bottom edge are off
plt.colorbar(shrink=0.6)
plt.savefig(os.path.join(basedir,'rsfmri/wincorr_timseries_heatmap.pdf'))
