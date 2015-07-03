"""
create basefilelist with md5sums
"""

import os
from myconnectome.utils.download_file import DownloadFile
import tempfile
from getmd5sum import getmd5sum


basedir=os.environ['MYCONNECTOME_DIR']

dataurl='http://d2bmty58oscepi.cloudfront.net'
basefileurl=dataurl+'/basefilelist.txt'

outfile='basefilelist_md5.txt'

tmpfile=tempfile.mkstemp()
os.close(tmpfile[0])

DownloadFile(basefileurl,tmpfile[1])

basefiles=[i.strip() for i in open(tmpfile[1]).readlines()]
os.remove(tmpfile[1])

flist=[]

for b in basefiles:
    print 'downloading',b
    tmpfile=tempfile.mkstemp()
    os.close(tmpfile[0])
    DownloadFile(dataurl+'/'+b,tmpfile[1])
    hash=getmd5sum(open(tmpfile[1],'rb'),hashlib.md5())
    print hash
    flist.append([b,hash])
    
f=open(outfile,'w')
for l in flist:
    f.write('%s\n'%'\t'.join(l))
f.close()
