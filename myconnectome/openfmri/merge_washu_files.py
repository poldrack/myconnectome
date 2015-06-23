import os,glob
import dicom
import json

outdir='/scratch/01329/poldrack/selftracking/ds031/sub00001/ses106/functional'

basedirs=['vc39556','vc39556_2']
# 20150402_085939RSFC240FramesEO32Slicess025a001_238.nii.gz

for b in range(len(basedirs)):
    basedir=basedirs[b]
    rsfiles=glob.glob(os.path.join(basedir,'*RSFC*_001.nii.gz'))
    rsfiles.sort()

    for r in rsfiles:
        seriesnum=int(r.split('Slicess')[1].split('a')[0])
        cmd='fslmerge -t part%d_series%03d.nii.gz %s'%(b+1,seriesnum,r.replace('_001.','_*.'))
        if not os.path.exists('part%d_series%03d.nii.gz'%(b+1,seriesnum)):
            print cmd
        # get dicom header
        dcmfile=glob.glob('%s/DICOM/VC*.MR.HEAD_LAUMANN.%04d.0001.2015.04.02.*.IMA'%(basedir,seriesnum))[0]
        print dcmfile
        dcmdata=dicom.read_file(dcmfile)
        dcmdict={}
        for k in dcmdata.dir():
            dd=dcmdata.data_element(k)

            try:
                dd.value.decode('ascii')
                dcmdict[dd.name]=dd.value
            except:
                try:
                    dd.value.original_string.decode('ascii')
                    dcmdict[dd.name]=dd.value
                except:
                    pass
        jsonfile='part%d_series%03d.json'%(b+1,seriesnum)
        f=open(jsonfile,'w')
        f.write(json.dumps(dcmdict,indent=4))
        f.close()
        
        
        
                                                  
