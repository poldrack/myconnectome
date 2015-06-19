"""
make openfmri distro for myconnectome
"""

import glob,os,shutil
import pickle
import json
import mvpa2.misc.fsl

def makedir(d):
    """ make a directory if it doesn't already exist"""
    if not os.path.exists(d):
        os.makedirs(d)

def get_infodict(type,dcmhdr):
    infodict={}
    for k in dcmhdr.keys():
        h=dcmhdr[k]
        # here we make the assumption that the
        # good resting scan was the last one in the session
        # I *think* that's a good assumption
        if h.SeriesDescription.find(type)==0:
            for hk in h.keys():
                try:
                    # filter out non-ascii entries
                    h[hk].value.decode('ascii')
                    infodict[h[hk].name]=h[hk].value
                except:
                    pass
    return infodict

def get_infodict_by_num(n,dcmhdr):
    infodict={}
    k='%d'%n

    h=dcmhdr[k]
    # here we make the assumption that the
    # good resting scan was the last one in the session
    # I *think* that's a good assumption
 
    for hk in h.keys():
        try:
            # filter out non-ascii entries
            h[hk].value.decode('ascii')
            infodict[h[hk].name]=h[hk].value
        except:
            pass
    return infodict


def logged_copy(infile,outfile,logfile='/scratch/01329/poldrack/selftracking/ds031/file_log.txt'):
    shutil.copy(infile,outfile)
    f=open(logfile,'a')
    f.write('%s\t%s\n'%(infile,outfile))
    f.close()
    
overwrite=False
task_descriptors=['N-','dot','face','super','loc','Breath']

basedir='/corral-repl/utexas/poldracklab/data/selftracking'
outdir='/scratch/01329/poldrack/selftracking/ds031/sub00001'
anatbase='/corral-repl/utexas/poldracklab/data/selftracking/anatomy_dicoms'
subdirs=glob.glob(os.path.join(basedir,'sub[0-1]*'))

subdirs.sort()


for i in range(len(subdirs)):
    subdir=subdirs[i]
    subcode=os.path.basename(subdir)
    sesscode=subcode.replace('sub','ses')
    print subcode,sesscode
    sessdir=os.path.join(outdir,sesscode)
    makedir(sessdir)

    headerpklfile=os.path.join(subdir,'logs/dicom_headers.pkl')
    try:
        dcmhdr=pickle.load(open(headerpklfile,'rb'))
    except:
        dcmhdr={}
    
    orig_boldfile=glob.glob(os.path.join(subdir,'BOLD/Resting*/bold.nii.gz'))
    if not len(orig_boldfile)==1:
        print 'no good bold file for',subcode
    else:                      
        bolddir=os.path.join(sessdir,'functional')
        makedir(bolddir)
        boldfile=os.path.join(bolddir,'sub00001_%s_rest001_run001_bold.nii.gz'%sesscode)
        if not os.path.exists(boldfile) or overwrite:
            print 'copying %s to %s'%(orig_boldfile[0],boldfile)
            logged_copy(orig_boldfile[0],boldfile)

        # dump dicom header to json
        # need to figure out which session it was
        infofile=boldfile.replace('.nii.gz','.json')
        if not os.path.exists(infofile) or overwrite:
            infodict=get_infodict('Resting',dcmhdr)
            f=open(infofile,'w')
            f.write(json.dumps(infodict,indent=4))
            f.close()

    # get anatomies
    if os.path.exists(os.path.join(anatbase,'t1w/%s_t1.nii.gz'%subcode)):
        t1file=os.path.join(anatbase,'t1w/%s_t1.nii.gz'%subcode)
    else:
        t1file=None
    
    if os.path.exists(os.path.join(anatbase,'t2w/%s_t2.nii.gz'%subcode)):
        t2file=os.path.join(anatbase,'t2w/%s_t2.nii.gz'%subcode)
    else:
        t2file=None

    anatsessdir=os.path.join(sessdir,'anatomy')
    t1outfile=os.path.join(anatsessdir,'sub00001_%s_T1w_001.nii.gz'%sesscode)
    t2outfile=os.path.join(anatsessdir,'sub00001_%s_T2w_001.nii.gz'%sesscode)
    if t1file and not os.path.exists(t1outfile):
        makedir(anatsessdir)
        logged_copy(t1file,t1outfile)
    infofile=t1outfile.replace('.nii.gz','.json')
    if t1file and (not os.path.exists(infofile) or overwrite):
            infodict=get_infodict('T1w',dcmhdr)
            f=open(infofile,'w')
            f.write(json.dumps(infodict,indent=4))
            f.close()
        

    if t2file and not os.path.exists(t2outfile):
        makedir(anatsessdir)
        logged_copy(t2file,t2outfile)
    infofile=t2outfile.replace('.nii.gz','.json')
    if t2file and (not os.path.exists(infofile) or overwrite):
            infodict=get_infodict('T2w',dcmhdr)
            f=open(infofile,'w')
            f.write(json.dumps(infodict,indent=4))
            f.close()
        

        
        

    # get diffusion
    diffusion_files=glob.glob(os.path.join(subdir,'DTI/DTI_[1,2].nii.gz'))
    diffusion_files.sort()
    if len(diffusion_files)>0:
        diffdir=os.path.join(sessdir,'diffusion')
        makedir(diffdir)

        # find entries in header pickle
        diffusion_series=[-1,-1]
        for i in dcmhdr.keys():
            if dcmhdr[i].SeriesDescription=='MBEPI with MDDW R-L':
                diffusion_series[0]=int(i)
            elif dcmhdr[i].SeriesDescription=='MBEPI with MDDW L-R':
                diffusion_series[1]=int(i)
        print 'diffusion series',diffusion_series
        assert len(diffusion_series)==2
        
        for i in range(len(diffusion_files)):
            fnum=int(os.path.basename(diffusion_files[i]).split('_')[1].split('.')[0])
            outfile=os.path.join(diffdir,'sub00001_%s_dwi_%03d.nii.gz'%(sesscode,fnum))
            if not os.path.exists(outfile) or overwrite:
                logged_copy(diffusion_files[i],outfile)
                
            outfile=os.path.join(diffdir,'sub00001_%s_dwi_%03d.bval'%(sesscode,fnum))
            if not os.path.exists(outfile) or overwrite:
                logged_copy(diffusion_files[i].replace('.nii.gz','.bval'),outfile)
            outfile=os.path.join(diffdir,'sub00001_%s_dwi_%03d.bvec'%(sesscode,fnum))
            if not os.path.exists(outfile) or overwrite:
                logged_copy(diffusion_files[i].replace('.nii.gz','.bvec'),outfile)
            infofile=os.path.join(diffdir,'sub00001_%s_dwi_%03d.json'%(sesscode,fnum))
            
            if diffusion_series[i]>-1 and (not os.path.exists(infofile) or overwrite):
                infodict=get_infodict_by_num(diffusion_series[i],dcmhdr)
                f=open(infofile,'w')
                f.write(json.dumps(infodict,indent=4))
                f.close()
        
            
    # get task data
    for t in range(len(task_descriptors)):
        td=task_descriptors[t]
        taskfiles=glob.glob(os.path.join(subdir,'BOLD/%s*/bold.nii.gz'%td))
        if len(taskfiles)==0:
            continue
        for tf in range(len(taskfiles)):
            taskfile=taskfiles[tf]
            seriesnum=int(os.path.dirname(taskfile).split('_')[-1])
            infodict=get_infodict_by_num(seriesnum,dcmhdr)
            print infodict['Series Description']
            outfile=os.path.join(outdir,'%s/functional/sub00001_%s_task%03d_run%03d.nii.gz'%(sesscode,sesscode,t+1,tf+1))
            if not os.path.exists(outfile) or overwrite:
                logged_copy(taskfile,outfile)
            infofile=outfile.replace('nii.gz','json')
            if not os.path.exists(infofile) or overwrite:
                f=open(infofile,'w')
                f.write(json.dumps(infodict,indent=4))
                f.close()

            # get onset info from model
            modelfile=os.path.join(subdir,'model/model%03d/task%03d_run%03d_333.feat/design.fsf'%(t+1,t+1,tf+1))
            if os.path.exists(modelfile):
                print 'found modelfile',modelfile
                design=mvpa2.misc.fsl.read_fsl_design(modelfile)
         
    # get field maps
    fmfile_orig=glob.glob(os.path.join(subdir,'fieldmap/fieldmap_mag.nii.gz'))
    if len(fmfile_orig)>0:
        fmdir=os.path.join(sessdir,'fieldmap')
        makedir(fmdir)
        outfile_mag=os.path.join(fmdir,'sub00001_%s_fieldmap_001_magnitude.nii.gz'%sesscode)
        if not os.path.exists(outfile_mag):
            logged_copy(fmfile_orig[0],outfile_mag)
        
        outfile_phase=os.path.join(fmdir,'sub00001_%s_fieldmap_001_phase.nii.gz'%sesscode)
        if not os.path.exists(outfile_phase):
            logged_copy(fmfile_orig[0].replace('mag','phase'),outfile_phase)
        
        infofile=os.path.join(fmdir,'sub00001_%s_fieldmap_001_scan.json'%sesscode)
        if not os.path.exists(infofile):
            fm_series=[]
            for k in dcmhdr.iterkeys():
                if dcmhdr[k].SeriesDescription=='gre_field_mapping':
                    fm_series.append(int(k))
            fm_series.sort()
            infodict=get_infodict_by_num(fm_series[0],dcmhdr)
            f=open(infofile,'w')
            f.write(json.dumps(infodict,indent=4))
            f.close()
            
        
