"""
get_data.py: functions to download data for myconnectome project from cloudfront archive
Options:
    -b/--base: get base data for analysis
    -a/--all: get base data and results from analysis
    -h: print this help message
"""

import os,getopt,sys
import datetime
import tempfile

from getmd5sum import getmd5sum
from myconnectome.utils.download_file import DownloadFile

def timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

dataurl='http://myconnectome.s3.amazonaws.com/base'

basefileurl=dataurl+'/basefilelist_md5.txt'

basedir=os.environ['MYCONNECTOME_DIR']

basefile=os.path.join(basedir,'basefilelist_md5.txt')

dirname_listdict={'bct':'http://myconnectome.s3.amazonaws.com/base/bctlist_md5.txt',
                  'david':'http://myconnectome.s3.amazonaws.com/base/davidfilelist_md5.txt'}

def get_list_data(listfileurl,dataurl,logfile=None,
                  skip=[],overwrite=False,verbose=False):

    if not logfile:
        print 'no logging..'
    # get base list
    tmpfile=tempfile.mkstemp()
    os.close(tmpfile[0])
    
    DownloadFile(listfileurl,tmpfile[1])
    basefiles=[i.strip().split('\t') for i in open(tmpfile[1]).readlines()]
    os.remove(tmpfile[1])
    
    for b in basefiles:
        skipfile=False
        for s in skip:
            if  b[0].find(s)>-1:
                print 'skipping',b[0]
                skipfile=True
        if skipfile:
            continue
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
        try:
            open(logfile,'a').write('%s\n'%'\t'.join(b))
        except:
            print 'problem with logging...'

 
def get_directory(d,dataurl=dataurl,logfile=os.path.join(basedir,'logs'),skip=[],overwrite=False,verbose=False):
    assert dirname_listdict.has_key(d)
    get_list_data(dirname_listdict[d],dataurl,logfile,skip,overwrite,verbose)
    
def get_base_data(overwrite=False):
         
    logdir=os.path.join(basedir,'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logfile=os.path.join(logdir,'data_downloads.log')
    print 'getting data for main analysis...'
    get_list_data(basefileurl,dataurl,logfile)

  
def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)
    
def main(argv):
    
        
    global dataurl
    global basefileurl
    try:
        assert os.path.exists(basedir)
    except:
        print 'creating base directory:',basedir
        os.mkdir(basedir)
    skip=[]
    overwrite=False
    try:
        # right now only the base option is implemented
        opts, args = getopt.getopt(argv,"bao",['base','all','skip-htcount','skip-rsfmri'])
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
        if opt == '--skip-rsfmri':
            skip.append('combined_data_scrubbed')
            print 'skipping rsfmri timeseries data'
        if opt == '--skip-htcount':
            skip.append('htcount')
            print 'skipping htcount data'
        if opt == '--base' or opt == '-b':
            data_to_get.append('base')
        if opt == '--all' or opt=='-a':
            data_to_get.append('all')
    
    logdir=os.path.join(basedir,'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logfile=os.path.join(logdir,'data_downloads.log')
    
    if 'base' in data_to_get:
        print 'getting base starting data for main analysis...'
        get_list_data(basefileurl,dataurl,logfile,skip,overwrite)
        
    if 'all' in data_to_get:
        basefileurl=dataurl+'/myconnectome_md5.txt'
        print 'getting all data and results for main analysis...'
        get_list_data(basefileurl,dataurl,logfile,skip,overwrite)
        
if __name__ == "__main__":
   main(sys.argv[1:])
