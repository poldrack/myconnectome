# -*- coding: utf-8 -*-
"""
Created on Sat May  2 15:40:44 2015

@author: poldrack
"""

import os,glob
import urllib
import numpy

def dequote_string(l):
    if l.find('"')<0:
        return l
    in_quotes=False
    l_dequoted=[]
    for c in l:
        if c=='"' and in_quotes:
            in_quotes=False
        elif c=='"' and not in_quotes:
            in_quotes=True
        elif in_quotes and c==' ':
            l_dequoted.append('_')
        else:
            l_dequoted.append(c)
    return ''.join(l_dequoted)
        
def load_R_dataframe(filename):
    """ 
    load an R data frame from text file or url or filehandle
    """
    try:
        # check whether it's a urllib handle
        filename.url
        f=filename
    except:
        if filename.find('http')==0:
            f=urllib.urlopen(filename)
        else:
            f=open(filename)
    
    header=f.readline().strip().split()
    lines=f.readlines()
    f.close()
    data=[]
    rowlabels=[]
    
    for l in lines:
        # first need to replace spaces contained within quotes
        l=dequote_string(l)
        l_s=[i.replace('"','') for i in l.strip().split()]
        rowlabels.append(l_s[0])
        data.append([float(i) for i in l_s[1:]])
    data=numpy.array(data)
    return data,rowlabels,header

def load_wgcna_module_assignments(filename):
    """ 
    load module assignment file
    """
    try:
        # check whether it's a urllib handle
        filename.url
        f=filename
    except:
        if filename.find('http')==0:
            f=urllib.urlopen(filename)
        else:
            f=open(filename)
    
    lines=f.readlines()
    f.close()
    data=[]
    rowlabels=[]
    
    for l in lines:
        # first need to replace spaces contained within quotes
        l=dequote_string(l)
        l_s=[i.replace('"','') for i in l.strip().split()]
        rowlabels.append(l_s[0])
        data.append([float(i) for i in l_s[1:]])
    data=numpy.array(data)
    return data,rowlabels



def load_dataframe(filename,thresh=0.1):
    if not filename.find('http')==0:
        f=open(filename)
    else:
        f=urllib.urlopen(filename)
    # return p value, t stat, and correlation
    
    header=f.readline()
    lines=f.readlines()
    f.close()
    data={}
    for l in lines:
        # first need to replace spaces contained within quotes
        l=dequote_string(l)
        l_s=[i.replace('"','') for i in l.strip().split()]
        try:
         if float(l_s[-1])<thresh:
            #print l_s
            data[(l_s[1],l_s[2])]=[float(l_s[-1]),float(l_s[4]),float(l_s[3]),int(l_s[-2])]
        except:
            pass
    return data
