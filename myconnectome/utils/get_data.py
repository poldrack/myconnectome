"""
get_data.py: functions to download data for myconnectome project from cloudfront archive
Options:
    --all: get all basic data needed for analysis
    --rawfunc: get raw fMRI data
    --diffusion: get raw diffusion data
    --anatomy: get raw anatomical data
    -h: print this help message
"""

import os,getopt,sys
import urllib
import re
import datetime
import tempfile

from getmd5sum import getmd5sum
from myconnectome.utils.run_shell_cmd import run_shell_cmd
from myconnectome.utils.download_file import DownloadFile

def timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

#dataurl='http://d2bmty58oscepi.cloudfront.net'
dataurl='http://s3-us-west-2.amazonaws.com/myconnectome/base'

basefileurl=dataurl+'/basefilelist_md5.txt'

basedir=os.environ['MYCONNECTOME_DIR']
basefile=os.path.join(basedir,'basefilelist_md5.txt')

#dataurl='http://web.stanford.edu/group/poldracklab/myconnectome-data'

dirname_listdict={'bct':'https://s3-us-west-2.amazonaws.com/myconnectome/base/bctlist_md5.txt',
                  'david':'https://s3-us-west-2.amazonaws.com/myconnectome/base/davidfilelist_md5.txt'}

def get_list_data(listfileurl,logfile=None,overwrite=False,verbose=False):

    # get base list
    tmpfile=tempfile.mkstemp()
    os.close(tmpfile[0])
    
    DownloadFile(listfileurl,tmpfile[1])
    basefiles=[i.strip().split('\t') for i in open(tmpfile[1]).readlines()]
    os.remove(tmpfile[1])
    
    for b in basefiles:
        if os.path.exists(os.path.join(basedir,b[0])) and not overwrite:
            
            md5sum=getmd5sum(os.path.join(basedir,b[0]))
            if verbose:
                print 'existing file',b[0],md5sum,b[1]
            if md5sum==b[1]:
                if verbose:
                    print 'using existing file:',b[0]
                continue

        print 'downloading',b[0]
        DownloadFile(dataurl+'/'+b[0].replace('+','%2B'),os.path.join(basedir,b[0]))
        ds_md5=getmd5sum(os.path.join(basedir,b[0]))
        if not ds_md5==b[1]:
            print 'md5sum does not match for ',b[0],ds_md5
        if logfile:
            open(logfile,'a').write('%s\n'%'\t'.join(b))

 
def get_directory(d):
    assert dirname_listdict.has_key(d)
    get_list_data(dirname_listdict[d])
    
def get_base_data(overwrite=False):
         
    logdir=os.path.join(basedir,'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logfile=os.path.join(logdir,'data_downloads.log')
    print 'getting data for main analysis...'
    get_list_data(basefileurl,logfile=logfile,overwrite=overwrite)

  
def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)
    
def main(argv):
    
        
        
    try:
        assert os.path.exists(basedir)
    except:
        print 'creating base directory:',basedir
        os.mkdir(basedir)

    overwrite=False
    try:
        # right now only the base option is implemented
        opts, args = getopt.getopt(argv,"bo",['base'])
    except getopt.GetoptError:
        usage()
    if len(opts)==0:
        usage()
    data_to_get=[]
    for opt, arg in opts:
        if opt == '-h':
            usage()
        if opt == '-o':
            overwrite=True
            print 'overwriting older data'
        if opt == '--base':
            data_to_get.append('base')
    
    logdir=os.path.join(basedir,'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logfile=os.path.join(logdir,'data_downloads.log')
    
    if 'base' in data_to_get:
        print 'getting data for main analysis...'
        get_list_data(basefileurl,logfile=logfile,overwrite=overwrite)
        
if __name__ == "__main__":
   main(sys.argv[1:])
