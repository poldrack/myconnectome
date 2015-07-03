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
from getmd5sum import getmd5sum
from myconnectome.utils.run_shell_cmd import run_shell_cmd
from myconnectome.utils.download_file import DownloadFile

def timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

dataurl='http://d2bmty58oscepi.cloudfront.net'
basefileurl=dataurl+'/basefilelist_md5.txt'

basedir=os.environ['MYCONNECTOME_DIR']
basefile=os.path.join(basedir,'basefilelist_md5.txt')

#dataurl='http://web.stanford.edu/group/poldracklab/myconnectome-data'



def get_base_data(logfile=None,overwrite=None):
    if logfile:
        logcmd='-a %s'%logfile
    else:
        logcmd=''
    if overwrite:
        owcmd=''
    else:
        owcmd='-N'
    # get base list
    DownloadFile(basefileurl,basefile)
    basefiles=[i.strip().split('\t') for i in open(basefile).readlines()]
    for b in basefiles:
        if os.path.exists(os.path.join(basedir,b[0])):
            md5sum=getmd5sum(os.path.join(basedir,b[0]))
            if md5sum==b[1]:
                print 'using existing file:',b[0]
                continue
        print 'downloading',b[0]
        DownloadFile(dataurl+'/'+b[0],os.path.join(basedir,b[0]))
        try:
            assert getmd5sum(os.path.join(basedir,b))==b[1]
        except:
            print 'md5sum does not match for ',b[0]
  
def get_directory(d,logfile=None,overwrite=None):
    if logfile:
        logcmd='-a %s'%logfile
    else:
        logcmd=''
    if overwrite:
        owcmd=''
    else:
        owcmd='-N'
    cmd='wget -N -r -l inf --no-remove-listing --no-parent -nH --cut-dirs=4 %s %s -R "index.html*","*.gif","robots.txt" -P %s %s/%s/'%(owcmd,logcmd,basedir,dataurl,d)
    run_shell_cmd(cmd)
  
 
  
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
        get_base_data(logfile=logfile,overwrite=overwrite)
        
if __name__ == "__main__":
   main(sys.argv[1:])
