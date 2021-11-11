# -*- coding: utf-8 -*-
"""
Created on Sun May  3 15:10:44 2015

@author: poldrack
"""

from __future__ import absolute_import
import numpy

def get_hubs(degree,P):
    """
    hub definition based on:
     http://www.plosone.org/article/info%3Adoi%2F10.1371%2Fjournal.pone.0001049
    'Considering only high-degree vertices (i.e. vertices with a degree at least
 one standard deviation above the network mean) we classify vertices with a part
icipation coefficient P<0.3 as provincial hubs, and nodes with P>0.3 as connecto
r hubs.'
    """
    meandeg=numpy.mean(degree)
    stddeg=numpy.std(degree)
    cutoff=meandeg+stddeg
    hubs=numpy.zeros(len(degree))
    hubs[(degree>cutoff)*(P<0.3)]=1  # provincial hub
    hubs[(degree>cutoff)*(P>0.3)]=2  # connector hub
    return hubs
