"""
get_data.py: functions to download data for myconnectome project from Stanford archive
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
import hashlib
import requests
from myconnectome.utils.run_shell_cmd import run_shell_cmd

def timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

   
basedir=os.environ['MYCONNECTOME_DIR']

dataurl='http://web.stanford.edu/group/poldracklab/myconnectome-data'

def get_base_data(logfile=None,overwrite=None):
    if logfile:
        logcmd='-a %s'%logfile
    else:
        logcmd=''
    if overwrite:
        owcmd=''
    else:
        owcmd='-N'
    cmd='wget -N -r -l inf --no-remove-listing --no-parent -nH --cut-dirs=4 %s %s -R "index.html*","*.gif","robots.txt" -P %s %s/base/'%(owcmd,logcmd,basedir,dataurl)
    run_shell_cmd(cmd)
  
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
