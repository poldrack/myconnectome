"""
create basefilelist with md5sums
"""

from __future__ import absolute_import
from __future__ import print_function
import os
from myconnectome.utils.download_file import DownloadFile
import tempfile
from .getmd5sum import getmd5sum


basedir=os.environ['MYCONNECTOME_DIR']

#dataurl='http://d2bmty58oscepi.cloudfront.net'
dataurl='https://s3-us-west-2.amazonaws.com/myconnectome/base'

basefiles=['davidfilelist.txt','bctlist.txt','basefilelist.txt']

for bf in basefiles:
    basefileurl=dataurl+'/%s'%bf
    
    outfile=bf.replace('.txt','_md5.txt')
    
    tmpfile=tempfile.mkstemp()
    os.close(tmpfile[0])
    
    DownloadFile(basefileurl,tmpfile[1])
    
    basefiles=[i.strip() for i in open(tmpfile[1]).readlines()]
    os.remove(tmpfile[1])
    
    flist=[]
    
    for b in basefiles:
        print('downloading',b)
        tmpfile=tempfile.mkstemp()
        os.close(tmpfile[0])
        DownloadFile(dataurl+'/'+b.replace('+','%2B'),tmpfile[1])
        try:
            l=open(tmpfile[1],'r').readlines()
            for ll in l:
                if ll.find('NoSuchKey')>-1:
                    print('bad file download...')
        except:
            pass
        hash=getmd5sum(tmpfile[1])
        print(hash)
        flist.append([b,hash])
        
    f=open(outfile,'w')
    for l in flist:
        f.write('%s\n'%'\t'.join(l))
    f.close()
