# -*- coding: utf-8 -*-
"""
Created on Sat May  2 15:40:44 2015

@author: poldrack
"""

import os,glob

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
        
    
def load_dataframe(filename,thresh=0.1):
    # return p value, t stat, and correlation
    f=open(filename)
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
