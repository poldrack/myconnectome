# -*- coding: utf-8 -*-
"""

combine fastqc results into a single file
Created on Mon Jan 19 08:45:12 2015

@author: poldrack
"""

import glob
import os
import numpy
import pandas as pd

datadir='/Users/poldrack/data_unsynced/selftracking/rna-seq/fastqc'

qcfiles=glob.glob(os.path.join(datadir,'*/fastqc_data.txt'))

subcodes={}
data={}

for f in qcfiles:
    subcode=f.split('/')[7].split('_')[0]
    runcode='-'.join(f.split('/')[7].split('_')[1:3])
    if not subcodes.has_key(subcode):
        subcodes[subcode]=0
    subcodes[subcode]+=1
    if not data.has_key(subcode):
        data[subcode]={}
    data[subcode][runcode]={}
    # parse input
    lines=[i.strip() for i in open(f).readlines()]
    # basic statistics
    data[subcode][runcode]['Basic Statistics']={}
    for l in lines[4:10]:
        l_s=l.split('\t')
        data[subcode][runcode]['Basic Statistics'][l_s[0].replace('%','')]=l_s[1]
    
    data[subcode][runcode]['Per base sequence quality']={}
    for i in range(13,len(lines)):
        l=lines[i]
        l_s=l.split('\t')
        if l=='>>END_MODULE':
            next_mod=i+3
            break
        data[subcode][runcode]['Per base sequence quality'][int(l_s[0].split('-')[0])]=[float(j) for j in l_s[1:]]
        
    data[subcode][runcode]['Per sequence quality scores']={}
    for i in range(next_mod,len(lines)):
        l=lines[i]
        l_s=l.split('\t')
        if l=='>>END_MODULE':
            next_mod=i+3
            break
        data[subcode][runcode]['Per sequence quality scores'][int(l_s[0])]=float(l_s[1])
        
    data[subcode][runcode]['Per base sequence content']={}
    for i in range(next_mod,len(lines)):
        l=lines[i]
        l_s=l.split('\t')
        if l=='>>END_MODULE':
            next_mod=i+3
            break
        data[subcode][runcode]['Per base sequence content'][int(l_s[0].split('-')[0])]=[float(j) for j in l_s[1:]]
        
        
    data[subcode][runcode]['Per base GC content']={}
    for i in range(next_mod,len(lines)):
        l=lines[i]
        l_s=l.split('\t')
        if l=='>>END_MODULE':
            next_mod=i+3
            break
        data[subcode][runcode]['Per base GC content'][int(l_s[0].split('-')[0])]=[float(j) for j in l_s[1:]]

    data[subcode][runcode]['Per sequence GC content']={}
    for i in range(next_mod,len(lines)):
        l=lines[i]
        l_s=l.split('\t')
        if l=='>>END_MODULE':
            next_mod=i+3
            break
        data[subcode][runcode]['Per sequence GC content'][l_s[0]]=[float(j) for j in l_s[1:]]

    data[subcode][runcode]['Per base N content']={}
    for i in range(next_mod,len(lines)):
        l=lines[i]
        l_s=l.split('\t')
        if l=='>>END_MODULE':
            next_mod=i+3
            break
        data[subcode][runcode]['Per base N content'][int(l_s[0].split('-')[0])]=[float(j) for j in l_s[1:]]

# combine across lanes/runs within session
basekeys=data['sub064']['L1-R1']['Per base N content'].keys()
basekeys.sort()

for subcode in data.iterkeys():
    PerBaseSeqQuality=[]
    PerBaseGCContent=[]
    PerBaseNContent=[]
    for run in data[subcode].iterkeys():
        PerBaseSeqQuality.append([data[subcode][run]['Per base sequence quality'][i][0] for i in basekeys])
        PerBaseGCContent.append([data[subcode][run]['Per base GC content'][i][0] for i in basekeys])
        PerBaseNContent.append([data[subcode][run]['Per base N content'][i][0] for i in basekeys])
       
    data[subcode]['summary']={}
    data[subcode]['summary']['PerBaseSeqQuality']=numpy.mean(PerBaseSeqQuality,0)
    data[subcode]['summary']['PerBaseGCContent']=numpy.mean(PerBaseGCContent,0)
    data[subcode]['summary']['PerBaseNContent']=numpy.mean(PerBaseNContent,0)
   
subcodes=data.keys()
subcodes.sort()
PerBaseSeqQuality=numpy.zeros((len(subcodes),len(basekeys)))
PerBaseGCContent=numpy.zeros((len(subcodes),len(basekeys)))
PerBaseNContent=numpy.zeros((len(subcodes),len(basekeys)))

for i in range(len(subcodes)):
    subcode=subcodes[i]
    PerBaseSeqQuality[i,:]=data[subcode]['summary']['PerBaseSeqQuality']
    PerBaseGCContent[i,:]=data[subcode]['summary']['PerBaseGCContent']
    PerBaseNContent[i,:]=data[subcode]['summary']['PerBaseNContent']
    
PerBaseSeqQuality_df=pd.DataFrame(PerBaseSeqQuality,index=subcodes,columns=basekeys)
PerBaseGCContent_df=pd.DataFrame(PerBaseGCContent,index=subcodes,columns=basekeys)
PerBaseNContent_df=pd.DataFrame(PerBaseNContent,index=subcodes,columns=basekeys)

PerBaseSeqQuality_df.to_csv('/Users/poldrack/Dropbox/code/myconnectome/quality_assurance/PerBaseSeqQuality.csv')
PerBaseGCContent_df.to_csv('/Users/poldrack/Dropbox/code/myconnectome/quality_assurance/PerBaseGCContent.csv')
PerBaseNContent_df.to_csv('/Users/poldrack/Dropbox/code/myconnectome/quality_assurance/PerBaseNContent.csv')
