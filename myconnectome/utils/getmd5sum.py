# -*- coding: utf-8 -*-
"""
Created on Fri Jul  3 09:40:16 2015

@author: poldrack
"""

import hashlib

def getmd5sum(fname, blocksize=65536):
    afile=open(fname,'rb')
    hasher=hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()
