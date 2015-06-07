"""
get_data.py: functions to download data for myconnectome project from Amazon S3
Options:
    --all: get all basic data needed for analysis
    --rawfunc: get raw fMRI data
    --diffusion: get raw diffusion data
    --anatomy: get raw anatomical data
    -h: print this help message
"""

import os,getopt,sys
import boto
import tarfile

basedir=os.environ['MYCONNECTOME_DIR']
try:
    assert os.path.exists(basedir)
except:
    print 'creating base directory:',basedir
    os.mkdir(basedir)
  
  
bucket_name = 'myconnectome'

if bucket_name=='myconnectome':
    dataprefix='data'
else:
    dataprefix='ds031'
    
def get_file_from_s3(fname,outfile,logfile=None):
    
    # connect to the bucket
    conn = boto.connect_s3()
    bucket = conn.get_bucket(bucket_name)
    k=boto.s3.key.Key(bucket=bucket,name=fname)
    print fname
    print outfile
    k.get_contents_to_file(open(outfile,'wb'))
    if logfile:
        open(logfile,'a').write('%s\n'%outfile)
    
    
def extract_tarball(tar_url, extract_path='.'):
    """ from http://stackoverflow.com/questions/6058786/i-want-to-extract-a-tgz-file-and-extract-any-subdirectories-that-have-files-tha"""
    
    print tar_url
    tar = tarfile.open(tar_url, 'r')
    for item in tar:
        tar.extract(item, extract_path)
        if item.name.find(".tgz") != -1 or item.name.find(".tar") != -1:
            extract_tarball(item.name, "./" + item.name[:item.name.rfind('/')])

    
 
def get_s3_directory(dirname,outputdir=None,verbose=True,filestem=None,logfile=None):
    conn = boto.connect_s3()
    bucket = conn.get_bucket(bucket_name)
    if not outputdir:
        outputdir=os.path.join(basedir,dirname)
    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    for f in bucket.list('%s/'%dataprefix+dirname):
        if f.name=='%s/'%dataprefix+dirname+'/':
            continue
        if filestem and not f.name.find(filestem)==0:
            continue
        try:
            if verbose:
                print 'downloading',f.name
            get_file_from_s3(f.name,os.path.join(outputdir,os.path.basename(f.name)),logfile=logfile)
        except:
            print 'problem getting',f.name

def get_all_data(overwrite=False,logfile=None):
    """ 
    grab all necessary data from S3
    note that right now, it doesn't check to make sure all files are there, just the directory
    """
    
    datadirs={'parcellation':'parcellation',
              'rsfmri/combined_data_scrubbed':'combined_data_scrubbed',
              'fsaverage_LR32k':'fsaverage_LR32k',
              'aseg':'aseg',
              'rsfmri/tmasks':'tmasks',
              'surface_taskdata':'surface_taskdata'}
    files={dataprefix+'/rsfmri/subcodes.txt':'subcodes.txt',
           dataprefix+'/rsfmri/daycodes.txt':'daycodes.txt',
           dataprefix+'/parcellation/module_names.txt':'parcellation/module_names.txt'}
           
    for k in datadirs:
        outdir=os.path.join(basedir,datadirs[k])
        if not os.path.exists(outdir) or overwrite:
            get_s3_directory(k,outdir,logfile=logfile)
    for k in files:
        outfile=os.path.join(basedir,files[k])
        if not os.path.exists(outfile) or overwrite:
            get_file_from_s3(k,outfile,logfile=logfile)

def get_raw_func_data(overwrite=False):
    """
    get raw functional data from S3
    """
    outdir=os.path.join(basedir,'rsfmri/raw_nifti')
    print 'putting data in',outdir
    if not os.path.exists(outdir) or overwrite:
            get_s3_directory('rsfmri/raw_nifti',outdir)
    else:
        print 'raw_nifti dir already exists - use -o to overwrite'

    
def usage():
    """Print the docstring and exit with error."""
    sys.stdout.write(__doc__)
    sys.exit(2)
    
def main(argv):
    overwrite=False
    try:
        opts, args = getopt.getopt(argv,"ao",['all','rawfunc','rawdiffusion','anatomy-dicom','anatomy'])
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
        if opt == '--all':
            data_to_get.append('all')
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
    logfile=os.path.join(logdir,'s3_downloads.log')
    
    if 'all' in data_to_get:
        print 'getting data for main analysis...'
        get_all_data(logfile=logfile)
    if 'rawfunc' in data_to_get:
        print 'getting raw functional data - will take a while...'
        get_rawfunc_data(overwrite)
    if 'anatomy-dicom' in data_to_get:
        print 'getting anatomy dicoms'
        if not os.path.exists(os.path.join(basedir,'anatomy')):
            os.mkdir(os.path.join(basedir,'anatomy'))
        if not os.path.exists(os.path.join(basedir,'anatomy/anatomy_dicoms.tgz')) or overwrite:
            
            get_file_from_s3(dataprefix+'/anatomy/anatomy_dicoms.tgz',os.path.join(basedir,'anatomy/anatomy_dicoms.tgz'),logfile=logfile)
    if 'anatomy' in data_to_get:
        print 'getting anatomical images'
        if not os.path.exists(os.path.join(basedir,'anatomy')):
            os.mkdir(os.path.join(basedir,'anatomy'))
        if not os.path.exists(os.path.join(basedir,'anatomy/t1w')) or overwrite:
            get_s3_directory('anatomy/t1w',os.path.join(basedir,'anatomy/t1w'),logfile=logfile)
        if not os.path.exists(os.path.join(basedir,'anatomy/t2w')) or overwrite:
            get_s3_directory('anatomy/t2w',os.path.join(basedir,'anatomy/t2w'),logfile=logfile)
    if 'rawdiffusion' in data_to_get:
        print 'not yet implemented'
        
if __name__ == "__main__":
   main(sys.argv[1:])
