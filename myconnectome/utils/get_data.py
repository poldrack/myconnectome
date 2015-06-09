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

def timestamp():
    return datetime.datetime.now().strftime('%Y-%m-%d-%H:%M:%S')

# from  http://stackoverflow.com/questions/3431825/generating-a-md5-checksum-of-a-file
def hashfile(fname, blocksize=65536):
    afile=open(fname,'rb')
    buf = afile.read(blocksize)
    hasher=hashlib.md5()
    while len(buf) > 0:
        hasher.update(buf)
        buf = afile.read(blocksize)
    return hasher.hexdigest()

   
basedir=os.environ['MYCONNECTOME_DIR']

dataurl='http://web.stanford.edu/group/poldracklab/myconnectome-data/'


# my kludgey code requires the base dir to end in a slash
if not basedir[-1]=='/':
    basedir=basedir+'/'
    
try:
    assert os.path.exists(basedir)
except:
    print 'creating base directory:',basedir
    os.mkdir(basedir)
  
 
def get_children(url,verbose=False):
    children=[]
    if not url[-1]=='/':
        return [url]
    for i in re.findall('''href=["'](.[^"']+)["']''', urllib.urlopen(url).read(), re.I):
            if i.find('?')==0 or i.find('/')==0:
                continue
            if verbose:
                print url+i
            c=get_children(url+i)
            if c:
                children=children+c
    return children

def get_file(f,dataurl,outdir,logfile=None,overwrite=False,verbose=False):
    outfile=f.replace(dataurl,outdir)
    if not os.path.exists(os.path.dirname(outfile)):
        os.makedirs(os.path.dirname(outfile))
    if os.path.exists(outfile):
        print 'file exists:',outfile
    if not os.path.exists(outfile) or overwrite:
        data=[]
        tries=0
        while not data and tries<6:
            data=urllib.urlopen(f).read()
            tries+=1
        if not data:
            print 'problem downloading:',f
            return
        open(outfile,'wb').write(data)
        hash=hashfile(outfile)
        if logfile:
            open(logfile,'a').write('%s\t%s\t%s\n'%(outfile,timestamp(),hash))

def get_directory(dir,outdir,dataurl=dataurl,overwrite=False,logfile=None,verbose=False):
    if not outdir[-1]=='/':
        outdir=outdir+'/'
    if verbose:
        print 'checking:',dataurl+dir
    c=get_children(dataurl+dir,verbose=verbose)
    for file in c:
        if verbose:
            print 'getting',file
        get_file(file,dataurl+dir,outdir,logfile=logfile,overwrite=overwrite,verbose=verbose)
        
def get_base_data(overwrite=False,logfile=None):
    """ 
    grab all necessary data from S3
    note that right now, it doesn't check to make sure all files are there, just the directory
    """
    print 'getting base data, logging to',logfile
    get_directory('base/',basedir,dataurl,logfile=logfile,overwrite=overwrite)         

def get_raw_func_data(overwrite=False,logfile=None):
    """
    get raw functional data from S3
    """
    print 'getting raw rsfmri data, logging to',logfile
    get_directory('raw_rsfmri/',basedir,dataurl,logfile=logfile,overwrite=overwrite)         

    
def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)
    
def main(argv):
    overwrite=False
    try:
        opts, args = getopt.getopt(argv,"bo",['base','rawfunc','rawdiffusion','anatomy-dicom','anatomy'])
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
        if opt == '--rawfunc':
            data_to_get.append('rawfunc')
        if opt == '--anatomy-dicom':
            data_to_get.append('anatomy-dicom')
        if opt == '--anatomy':
            data_to_get.append('anatomy')
        if opt == '--rawdiffusion':
            data_to_get.append('raw_diffusion')
    
    logdir=os.path.join(basedir,'logs')
    if not os.path.exists(logdir):
        os.mkdir(logdir)
    logfile=os.path.join(logdir,'data_downloads.log')
    
    if 'base' in data_to_get:
        print 'getting data for main analysis...'
        get_base_data(logfile=logfile,overwrite=overwrite)
    if 'rawfunc' in data_to_get:
        print 'getting raw functional data - will take a while...'
        get_raw_func_data(overwrite)
    if 'anatomy-dicom' in data_to_get:
        print 'getting anatomy dicoms'
        if not os.path.exists(os.path.join(basedir,'anatomy')):
            os.mkdir(os.path.join(basedir,'anatomy'))
        if not os.path.exists(os.path.join(basedir,'anatomy/anatomy_dicoms.tgz')) or overwrite:
            
            get_file('/anatomy/anatomy_dicoms.tgz',os.path.join(basedir,'anatomy/anatomy_dicoms.tgz'),logfile=logfile)
    if 'anatomy' in data_to_get:
        print 'getting anatomical images'
        if not os.path.exists(os.path.join(basedir,'anatomy')):
            os.mkdir(os.path.join(basedir,'anatomy'))
        if not os.path.exists(os.path.join(basedir,'anatomy/t1w')) or overwrite:
            get_directory('anatomy/t1w',os.path.join(basedir,'anatomy/t1w'),logfile=logfile)
        if not os.path.exists(os.path.join(basedir,'anatomy/t2w')) or overwrite:
            get_directory('anatomy/t2w',os.path.join(basedir,'anatomy/t2w'),logfile=logfile)
    if 'rawdiffusion' in data_to_get:
        print 'not yet implemented'
        
if __name__ == "__main__":
   main(sys.argv[1:])
